from django.urls import path
from .views import profile_view, profile_list_view

urlpatterns = [
    # path("", home_view, name="home"),
    path("<str:username>/", profile_view, name="profile"),
    path("", profile_list_view, name="profile-list"),
]
