from apps.documents.models import Recipient
from apps.documents.enum import DocumentValidity


from datetime import date, timedelta

def recipients_response(document_group):
    if not document_group.otp:
        return {"message": "Otp required click on generate OTP .", "status":100}
    
    if not document_group.otp_verified:
        return {"message": "Please verify your OTP first .", "status":103}
    
    
    if document_group.document_group.validity == DocumentValidity.DATE.name and date.today() > document_group.document_group.expire_date:
        return {"message": "The document group has expired.", "status":101}
    
    # if Recipient.objects.filter(id =document_group=document_group.document_group,is_recipient_sign=True):
    #     return {"message": "You already sign That documenet", "status":102}
    
    return {"message": "Document is Vaild you can  sign", "status":200}
