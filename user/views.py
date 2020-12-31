from django.views.generic import CreateView, FormView, RedirectView, DetailView, UpdateView
from .forms import SignUPForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from .models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin


class UserSignUp(CreateView):
    form_class = SignUPForm
    template_name = "user-signup.html"

    def get_form_kwargs(self):
        kw = super(UserSignUp, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

    def get_success_url(self):
        if self.request.get("next"):
            return self.request.GET["next"]
        else:
            return "/"

    def get(self, request, *args, **kwargs):
        if isinstance(self.request.user, AnonymousUser):
            return super(UserSignUp, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/")


class UserSignin(FormView):
    form_class = AuthenticationForm
    template_name = "user-signin.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(UserSignin, self).form_valid(form)

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET["next"]
        else:
            return "/"

    def get(self, request, *args, **kwargs):
        if isinstance(self.request.user, AnonymousUser):
            return super(UserSignin, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/")


class UserSignOut(RedirectView):
    url = "/"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(UserSignOut, self).get(request, *args, **kwargs)


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user-profile.html"
    context_object_name = "user_details"

    def get_object(self, queryset=None):
        user = self.request.user
        user.total_liked = user.memes_liked.count()
        user.total_commented = user.memes_commented.count()
        user.total_memes = user.posts.count()
        return user


class UserEditProfile(LoginRequiredMixin, UpdateView):
    template_name = "user-profile-edit.html"
    form_class = EditProfileForm
    success_url = "/profile"
    model = User

    def get_object(self, queryset=None):
        return self.request.user


class OthersProfileView(DetailView):
    model = User
    template_name = "user-profile.html"
    context_object_name = "user_details"

    def get_object(self):
        q = self.get_queryset()
        res = q.get(username=self.kwargs.get("username"))
        res.total_liked = res.memes_liked.count()
        res.total_commented = res.memes_commented.count()
        res.total_memes = res.posts.count()
        if not self.request.user.id == res.id:
            res.is_others_profile = True
        return res
