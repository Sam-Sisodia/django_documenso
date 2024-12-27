



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
 
 
 
 

# export const FieldType= {
#     "SIGNATURE":"SIGNATURE",
#     "NAME":"NAME",
#     "INITIALS":"INITIALS",
#     "EMAIL":"EMAIL",
#     "NUMBER":"NUMBER",
#     "RADIO":"RADIO",
#     "CHECKBOX":"CHECKBOX",
#     "DROPDOWN":"DROPDOWN",
#     "DATE":"DATE",
#     "TEXT":"TEXT",
#     "FREE_SIGNATURE":"FREE_SIGNATURE"
# }
 


 