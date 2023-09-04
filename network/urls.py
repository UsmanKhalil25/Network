
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost",views.newPost,name ="newPost"),
    path("profile/<str:username>",views.displayProfile,name = "profile"),
    path("follow/<int:id>",views.follow,name ="follow"),
    path("unfollow/<int:id>",views.unfollow,name ="unfollow"),
    path("following",views.displayFollowing,name = "following"),
    path("edit/<int:id>",views.edit,name = "edit"),
    path("updateLike/<int:id>",views.updateLike,name = "updateLike")

    
]
