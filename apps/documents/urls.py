from django.urls import path
from . import views  # Ensure views are correctly imported

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("add-fields", views.DocumentFieldAPI, basename="add-fields")
router.register("upload-documents", views.DocumentGroupViewSet, basename="upload-documents")


urlpatterns = [
    # path('', views.LoginView.as_view(), name='login'),
    # path('register/', views.RegisterView.as_view(), name='register'),
]+ router.urls