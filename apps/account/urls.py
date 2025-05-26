from django.urls import path
from .views import MyProfileView


urlpatterns = [
    path('my/', MyProfileView.as_view(), name='my_profile'),
]