from django.urls import path
from . import views  # Ensure views are correctly imported

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    # path('register/', views.RegisterView.as_view(), name='register'),
]