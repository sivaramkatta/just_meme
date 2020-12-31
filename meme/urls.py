from django.urls import path
from .views import HomePage, SearchPage, CreateMeme, like_meme, MemeDetail, comment_meme, CreatedMemes, \
    LikedMemes, delete_meme, CategoriesPage, CategoryMemesList, search_tag, TagMemesList

urlpatterns = [path("", HomePage.as_view()),
               path("search/", SearchPage.as_view()),
               path("categories/", CategoriesPage.as_view()),
               path("meme/<int:id>", MemeDetail.as_view()),
               path("user/<str:username>/created/", CreatedMemes.as_view()),
               path("user/<str:username>/liked/", LikedMemes.as_view()),
               path("upload/", CreateMeme.as_view()),
               path("category/<str:category>/", CategoryMemesList.as_view()),
               path("tag/<str:tag_name>/", TagMemesList.as_view()),
               path("meme/<int:meme_id>/comment/", comment_meme),
               path("like", like_meme),
               path("meme/<int:meme_id>/delete/", delete_meme),
               path("search/tags/", search_tag)]
