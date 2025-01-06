from enum import Enum
class DocumentStatus(str, Enum):
    SIGNED = "SIGNED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    DRAFT = "DRAFT"  # 
    
    @classmethod
    def choices(cls):
     
        return tuple((i.name, i.value) for i in cls)

class RecipientRole(str, Enum):
    SIGNER= "SIGNER"
    APPROVER = "APPROVER"
    CC="CC"
    VIEWER= "VIEWER"
    @classmethod
    def choices(cls):
     
        return tuple((i.name, i.value) for i in cls)
    
    

class SigningType(str, Enum):
    PARALLEL= "PARALLEL"
    SEQUENTIAL = "SEQUENTIAL"
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
 
 
class DocumentType(str, Enum):
    DOCUMENT= "DOCUMENT"
    TEMPLATE = "TEMPLATE"
    @classmethod
    def choices(cls):
     
        return tuple((i.name, i.value) for i in cls)
 
 
 
 
class DocumentValidity(str, Enum):
    NO_EXPIRY = "NO_EXPIRY"
    DATE = "DATE"
    

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)



class RecipientAuthType(str,Enum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    OTP = "OTP"
    NONE = "NONE"
    
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


# {   "token_group_time": "15 days",
#     "token not found": "invaild token",
#     "already_sign": "",
#     "sign_order",
#     "auth tytpe= NONE,
#     "otp", (INPU JWT) -HEADER COMEING,
     
 
    
# }
 


 