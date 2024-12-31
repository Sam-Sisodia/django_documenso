


from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.documents.models import Field

@receiver(post_migrate)
def create_default_fields(sender, **kwargs):
    # List of default field names
    default_fields = [
        'SIGNATURE',
        'NAME',
        'INITIALS',
        'EMAIL',
        'NUMBER',
        'RADIO',
        'CHECKBOX',
        'DROPDOWN',
        'DATE',
        'TEXT',
        'FREE_SIGNATURE',
    ]
    
    # Only insert the default values if they don't already exist
    for field_name in default_fields:
   
        # Check if the field already exists
        if not Field.objects.filter(name=field_name).exists():
            # Create the field if it does not exist
            Field.objects.create(name=field_name)
