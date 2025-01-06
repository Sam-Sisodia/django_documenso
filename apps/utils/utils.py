from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader 
import io
import os
from reportlab.pdfgen import canvas

def modify_pdf(positionX, positionY, page_number, pdf_bytes, is_image, value):
    pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
    pdf_writer = PdfWriter()
    packet = io.BytesIO()

    if is_image:
        packet = io.BytesIO()
        c = canvas.Canvas(packet)
        image = Image.open(io.BytesIO(value))
                    # Convert image to an in-memory image object
        image_stream = io.BytesIO()
        image.save(image_stream, format="PNG")
        image_stream.seek(0)
        image_reader = ImageReader(image_stream)
       
        c.drawImage(image_reader, positionX, positionY, width=image.width / 2, height=image.height / 2)  # Adjust size as needed
        c.save()
     
    else:
        # Create a canvas for adding text
        c = canvas.Canvas(packet, pagesize=letter)
        c.setFont("Helvetica", 20)
        c.drawString(positionX, positionY, value)
        c.save()

    packet.seek(0)
    temp_pdf_reader = PdfReader(packet)

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        if page_num == page_number - 1:  # page_number is 1-indexed
            overlay_page = temp_pdf_reader.pages[0]
            page.merge_page(overlay_page)  

        pdf_writer.add_page(page)


    output_path = os.path.join(os.getcwd(), 'sajal_signed.pdf')
    with open(output_path, "wb") as output_file:
        pdf_writer.write(output_file)

    return {"message": "Document updated successfully"}



