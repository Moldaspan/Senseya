from django.urls import path

from .views import GoogleLoginApi, GoogleLoginRedirectApi
app_name = 'google_auth'
urlpatterns = [
    path("callback/", GoogleLoginApi.as_view(), name="callback-raw"),
    path("redirect/", GoogleLoginRedirectApi.as_view(), name="redirect-raw"),

]
