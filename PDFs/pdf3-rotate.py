# Rotating Pages
import PyPDF2

with open('sample.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    writer = PyPDF2.PdfWriter()

    # Rotate first page 90 degrees clockwise
    page = reader.pages[0].rotate(90)
    writer.add_page(page)

    # Add remaining pages as is
    for page in reader.pages[1:]:
        writer.add_page(page)

with open('rotated.pdf', 'wb') as output_file:
    writer.write(output_file)
