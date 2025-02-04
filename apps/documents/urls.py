from django.urls import path
from . import views  # Ensure views are correctly imported

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("add-fields", views.DocumentFieldAPI, basename="add-fields")
router.register("upload-documents", views.DocumentGroupViewSet, basename="upload-documents")
router.register("assign-recipients", views.DocumentsAssignRecipientAPI, basename="assign-recipients")


urlpatterns = [
    path('get-group-documents/<int:document_group_id>/', views.GetRecipientsDocuments.as_view(), name='get_recipients_documents'),
    path('add-document-fields/', views.DocumentFieldCreateAPIView.as_view(), name='add-document-fields'),
    path('remove-recipient/<int:grp_id>/<int:rec_id>/', views.RemoveRecipientsAPI.as_view(), name='remove-recipient'),
    path('recipient-updated-document/', views.RecipientUpdatedDocumentAPI.as_view(), name='recipient-updated-document'),
    path('send-documents/', views.SendDocumentToRecipient.as_view(), name='send-documents'),
    path('generate-otp/<str:token>/', views.GenerateOTPAPI.as_view(), name='generate-otp'),
    path('verify-otp/<str:token>', views.VerifyOTPAPI.as_view(), name='verify-otp'),
    path('get-sign-recipient-document/<str:token>/', views.RecipientSignGetProgressDocumentAPI.as_view(), name='sign-recipient'),
    path('sign-recipient-document/', views.SignUpdateRecipientsFieldValueAPI.as_view(), name='sign-recipient-document'),
  
]+ router.urls