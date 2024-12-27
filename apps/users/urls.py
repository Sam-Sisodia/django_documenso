from django.urls import path
from . import views  # Ensure views are correctly imported

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="api-login"),
    # path('', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]