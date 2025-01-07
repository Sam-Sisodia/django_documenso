from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader 
import io
import os
from reportlab.pdfgen import canvas
import base64
import re

def checkvalue_type(string):
    try:
        base64.b64decode(string)
        return bool(re.match(r'^[A-Za-z0-9+/=]+$', string))
    except Exception:
        return False
    
    
    
def update_pdf_add_values(pdf_bytes, completed_field_details):
    pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
    pdf_writer = PdfWriter()

    # Group fields by page number
    fields_by_page = {}
    for value in completed_field_details:
        page_number = int(value.get('page_no'))
        if page_number not in fields_by_page:
            fields_by_page[page_number] = []
        fields_by_page[page_number].append(value)

    # Loop through each page
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)

        # If there are fields for this page, create an overlay
        if page_num + 1 in fields_by_page:
            for value in fields_by_page[page_num + 1]:
                value_text = value.get("value")
                positionX = float(value.get("position_x"))
                positionY = float(value.get("position_y"))
                height = float(value.get("height"))
                width = float(value.get("width"))
                

                # Check if the field value is an image (Base64 encoded)
                is_image = False
                if checkvalue_type(value_text):
                    value_text = base64.b64decode(value_text)
                    is_image = True

                # Add image or text depending on the type
                if is_image:
                    image = Image.open(io.BytesIO(value_text))
                    image_stream = io.BytesIO()
                    image.save(image_stream, format="PNG")
                    image_stream.seek(0)
                    image_reader = ImageReader(image_stream)
                    c.drawImage(image_reader, positionX, positionY, width, height)
                else:
                    # c.setFont("Helvetica", 20)
                    # c.drawString(int(positionX), int(positionY), value_text)
                    
                    
                    font_size = int(height * 0.8)  # Scale font size based on height
                    c.setFont("Helvetica", font_size)

                    # Truncate text to fit within the width
                    max_chars = int(width / (font_size * 0.6))  # Estimate max characters based on width
                    truncated_text = value_text[:max_chars]

                    # Center the text vertically within the height
                    adjusted_positionY = positionY + (height - font_size) / 2

                    # Draw the text
                    c.drawString(positionX, adjusted_positionY, truncated_text)

            c.save()
            packet.seek(0)

            # Read the overlay content
            temp_pdf_reader = PdfReader(packet)
            overlay_page = temp_pdf_reader.pages[0]
            page.merge_page(overlay_page)

        # Add the (modified or unmodified) page to the writer
        pdf_writer.add_page(page)
        
    
  
   
    #     output_path = os.path.join(os.getcwd(), 'sajal_signed.pdf')
    #     with open(output_path, "wb") as output_file:
    #         pdf_writer.write(output_file)
    #     print("Document updated and saved successfully.")
    #     return {"message": "Document updated successfully", "file_path": output_path}
   
    output_stream = io.BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)
    pdf_base64 = base64.b64encode(output_stream.read()).decode('utf-8')
    print("Document updated and returned as Base64.")
    return {"message": "Document updated successfully", "data": pdf_base64}

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


# def update_pdf_add_values(pdf_bytes, completed_field_details):
#     pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
#     pdf_writer = PdfWriter()

#     # Group fields by page number
#     fields_by_page = {}
    
#     for value in completed_field_details:
#         page_number = int(value.get('page_no'))
#         if page_number not in fields_by_page:
#             fields_by_page[page_number] = []
#         fields_by_page[page_number].append(value)

#     # Loop through each page
#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]
#         packet = io.BytesIO()
#         c = canvas.Canvas(packet, pagesize=letter)

#         # If there are fields for this page, create an overlay
#         if page_num + 1 in fields_by_page:
    
#             for value in fields_by_page[page_num + 1]:
#                 value_text = value.get("value")
#                 positionX = float(value.get("position_x"))
#                 positionY = float(value.get("position_y"))
#                 height = float(value.get("height"))  # )Correct key for height
#                 width = float(value.get("width"))

#              # Check if the field value is an image (Base64 encoded)
#                 is_image = False
#                 if checkvalue_type(value_text):
#                     value_text = base64.b64decode(value_text)
#                     is_image = True

#                 # Add image or text depending on the type
#                 if is_image:
#                     image = Image.open(io.BytesIO(value_text))
#                     image_stream = io.BytesIO()
#                     image.save(image_stream, format="PNG")
#                     image_stream.seek(0)
#                     image_reader = ImageReader(image_stream)
#                     c.drawImage(image_reader, positionX, positionY, width, height)
#                 else:
#                     c.setFont("Helvetica", 20)
#                     c.drawString(int(positionX), int(positionY), value_text)

#         c.save()

#         # Reset packet and read the content to overlay
#         packet.seek(0)
#         temp_pdf_reader = PdfReader(packet)
#         overlay_page = temp_pdf_reader.pages[0]
#         page.merge_page(overlay_page)  # Merge overlay content to this page

#         # Add the page to the writer (whether modified or not)
#         pdf_writer.add_page(page)

#     # Save the updated PDF to a file
#     # if os.getenv("IS_DOWNLOAD") == True:
#         print("Download the documnet sign")
    
#         output_path = os.path.join(os.getcwd(), 'sajal_signed.pdf')
#         with open(output_path, "wb") as output_file:
#             pdf_writer.write(output_file)

#         return {"message": "Document updated successfully"}
#     # else:
        
    
#     #     output_stream = io.BytesIO()
#     #     pdf_writer.write(output_stream)
#     #     output_stream.seek(0)
#     #     pdf_base64 = base64.b64encode(output_stream.read()).decode('utf-8')
#     #     return {"message": "Document updated successfully", "data": pdf_base64}

