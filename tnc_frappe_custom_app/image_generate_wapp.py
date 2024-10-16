import requests
import os
from PIL import Image, ImageDraw, ImageFont
import frappe
from frappe.utils.file_manager import save_file, get_files_path

@frappe.whitelist()
def send_whatsapp_message(docname, mobile, message):
    # Fetch the doc to get the student_name and mobile
    doc = frappe.get_doc('Testing Doctype', docname)
    student_name = doc.student_name
    mobile = doc.mobile_number

    # Generate an image with student_name and mobile
    image_path = generate_student_image(student_name, mobile)

    # Save the image to Frappe's file system
    saved_file = save_file(f'{student_name}_image.jpg', open(image_path, 'rb').read(), doc.doctype, docname, is_private=0)

    # Get the absolute path of the saved file
    file_path = os.path.join(get_files_path(), os.path.basename(saved_file.file_url))

    # Check if the file exists at the file_path
    if not os.path.exists(file_path):
        frappe.throw(('File not found at path {0}').format(file_path))

    # Send the image via WhatsApp API
    api_url = 'https://wts.vision360solutions.co.in/api/sendFileWithCaption'
    params = {
        'token': 'clvos5bjd5v7qm51e3l9s0cib',  # Your API token
        'phone': mobile,  # Mobile number
        'message': message  # Message from the dialog
    }

    # Open the saved file and pass it as a file parameter
    with open(file_path, 'rb') as image_file:
        files = {
            'file': image_file
        }

        # Send the request to the WhatsApp API
        response = requests.post(api_url, params=params, files=files)

    # Return the response from the API
    if response.status_code == 201:
        return True
    else:
        frappe.throw(('Failed to send WhatsApp message'))

# def generate_student_image(student_name, mobile):
#     # Set up image properties
#     width, height = 400, 400
#     image = Image.new('RGB', (width, height), color=(255, 255, 255))
#     draw = ImageDraw.Draw(image)

#     # Specify the font and font size
#     # You need to provide a valid font file path (e.g., .ttf file)
#     # "arial.ttf" is a common font, but you can change it to any available font
#     font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Path to a TrueType font file
#     font_size = 24  # Set the desired font size
#     font = ImageFont.truetype(font_path, font_size)

#     # Add student_name and mobile to the image
#     text = f"Student: {student_name}\nMobile: {mobile}"
#     draw.text((50, 100), text, font=font, fill=(0, 0, 0))

#     # Save the image to a temporary path
#     image_path = f"/tmp/{student_name}_image.jpg"
#     image.save(image_path)

#     return image_path

def generate_student_image(student_name, mobile):
    # Set up image properties
    width, height = 400, 400
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Load the logo image
    logo_path = os.path.join(get_files_path(), 'TNC 1.png')  # Adjust if necessary
    logo = Image.open(logo_path)

    # Resize the logo if necessary
    logo_size = (50, 50)  # Set the desired size for the logo
    logo.thumbnail(logo_size)  # Remove ANTIALIAS argument

    # Paste the logo onto the main image at the top left corner
    image.paste(logo, (10, 10))  # (x, y) position

    # Specify the font and font size
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Path to a TrueType font file
    font_size = 24  # Set the desired font size
    font = ImageFont.truetype(font_path, font_size)

    # Add student_name and mobile to the image
    text = f"Student: {student_name}\nMobile: {mobile}"
    draw.text((70, 100), text, font=font, fill=(0, 0, 0))  # Adjust position to avoid logo

    # Save the image to a temporary path
    image_path = f"/tmp/{student_name}_image.jpg"
    image.save(image_path)

    return image_path

