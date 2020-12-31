from django.views.generic import CreateView, ListView, DetailView, TemplateView
from .forms import MemeUploadForm
from .models import Meme, Comments, Category
from rest_framework import decorators, permissions
from rest_framework.response import Response
from rest_framework import exceptions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
import cloudinary
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


@method_decorator([never_cache], name='dispatch')
class HomePage(ListView):
    template_name = "meme_list.html"
    model = Meme
    context_object_name = "memes"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        obj = super(HomePage, self).get_context_data(**kwargs)
        for meme in obj['memes']:
            meme.has_liked = self.request.user in meme.liked_by.all()
            meme.likes = meme.liked_by.count()
            meme.comments = meme.commented_by.count()
        return obj


@method_decorator([never_cache], name='dispatch')
class CreatedMemes(LoginRequiredMixin, HomePage):
    def get_queryset(self):
        return Meme.objects.filter(posted_by__username=self.kwargs.get("username"))


@method_decorator([never_cache], name='dispatch')
class LikedMemes(LoginRequiredMixin, HomePage):
    def get_queryset(self):
        return Meme.objects.filter(liked_by__username=self.kwargs.get("username"))


@method_decorator([never_cache], name='dispatch')
class CategoryMemesList(HomePage):
    def get_queryset(self):
        return Meme.objects.filter(category__slug=self.kwargs["category"])


@method_decorator([never_cache], name='dispatch')
class TagMemesList(HomePage):
    def get_queryset(self):
        return Meme.objects.filter(tags__contains=[self.kwargs["tag_name"]])


class SearchPage(TemplateView):
    template_name = "search.html"


class CategoriesPage(ListView):
    template_name = "categories_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.all()


class CreateMeme(LoginRequiredMixin, CreateView):
    template_name = "meme_upload.html"
    form_class = MemeUploadForm
    success_url = "/"

    def get_form_kwargs(self):
        kw = super(CreateMeme, self).get_form_kwargs()
        kw['request'] = self.request
        return kw


@method_decorator([never_cache], name='dispatch')
class MemeDetail(DetailView):
    template_name = "meme_detail.html"
    model = Meme
    pk_url_kwarg = "id"
    context_object_name = "meme"

    def get_object(self, queryset=None):
        q = self.get_queryset()
        meme_object = q.get(id=self.kwargs.get("id"))
        meme_object.has_liked = self.request.user in meme_object.liked_by.all()
        meme_object.likes = meme_object.liked_by.count()
        meme_object.comments = meme_object.commented_by.count()
        meme_object.comments_list = meme_object.comments_set.all()
        return meme_object


@decorators.api_view(http_method_names=['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
def like_meme(request):
    meme_id = request.data.get('id')
    user = request.user
    meme = Meme.objects.get(id=meme_id)
    try:
        meme.liked_by.get(id=user.id)
        meme.liked_by.remove(user)
    except:
        meme.liked_by.add(user)
    return Response({'success': True})


@decorators.api_view(http_method_names=["POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
def comment_meme(request, meme_id):
    if not request.data.get("comment"):
        raise exceptions.ValidationError("Comment can't be empty")
    try:
        meme = Meme.objects.get(id=meme_id)
    except:
        raise exceptions.ValidationError("Provide valid meme ID")
    Comments.objects.create(user=request.user, meme=meme, comment=request.data.get("comment"))
    return Response({'success': True})


@decorators.api_view(http_method_names=["DELETE"])
@decorators.permission_classes([permissions.IsAuthenticated])
def delete_meme(request, meme_id):
    meme = get_object_or_404(Meme, id=meme_id)
    if request.user.id == meme.posted_by.id:
        try:
            cloudinary.uploader.destroy(meme.image.name, invalidate=True)
        except:
            print("can't delete from Cloudinary", meme.image)
        meme.delete()
    else:
        raise PermissionError("Permission denied")
    return Response({"success": True})


@decorators.api_view(http_method_names=["get"])
def search_tag(request):
    search_term = request.query_params.get("q")
    res = list()
    if search_term:
        tags = Meme.objects.filter(tags__icontains=search_term).values_list("tags", flat=True)
        tags_set = set(item for sublist in tags for item in sublist if search_term.lower() in item.lower())
        res = list(tags_set)
    return Response({"tags": res})
