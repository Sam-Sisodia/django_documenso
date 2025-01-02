from django.urls import path
from . import views  # Ensure views are correctly imported

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("add-fields", views.DocumentFieldAPI, basename="add-fields")
router.register("upload-documents", views.DocumentGroupViewSet, basename="upload-documents")
router.register("assign-recipients", views.DocumentsAssignRecipientAPI, basename="assign-recipients")


urlpatterns = [
    path('get-group-documents/<int:document_group_id>/', views.GetRecipientsDocuments.as_view(), name='get_recipients_documents'),
    path('get-single-document/<int:document_id>/', views.SingleDocumentAPI.as_view(), name='get-single-document'),
    path('add-document-fields/', views.DocumentFieldCreateAPIView.as_view(), name='add-document-fields'),
    path('remove-recipient/<int:grp_id>/<int:rec_id>/', views.RemoveRecipientsAPI.as_view(), name='remove-recipient'),
    path('recipient-updated-document/', views.RecipientUpdatedDocumentAPI.as_view(), name='recipient-updated-document'),
    
]+ router.urls