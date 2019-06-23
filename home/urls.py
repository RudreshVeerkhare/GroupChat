from django.urls import path
from . import views


app_name = "home"
urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:grp_name>", views.group, name="group"),
    path("profile/<slug:user_name>", views.profile, name="profile"),
    path("group_profile/<slug:grp_name>", views.group_profile, name="group_profile"),
    path("search_user/", views.search_user, name="search_user"),
    path("<slug:grp_name>/add_members", views.add_member, name="add_members"),
]
