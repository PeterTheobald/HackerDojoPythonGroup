from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

# Create a document template

doc = SimpleDocTemplate("platypus-document.pdf", pagesize=letter)
styles = getSampleStyleSheet()
flowables = []

# Add a title and paragraph
flowables.append(Paragraph("Using ReportLab Platypus", styles['Title']))
flowables.append(Spacer(1, 12))
flowables.append(Paragraph("This is an example paragraph using ReportLab's Platypus module.", styles['BodyText']))
flowables.append(Spacer(1, 12))

# Create a table with headers and data rows
data = [
    ['Header 1', 'Header 2', 'Header 3'],
    ['Row 1, Col 1', 'Row 1, Col 2', 'Row 1, Col 3'],
    ['Row 2, Col 1', 'Row 2, Col 2', 'Row 2, Col 3']
]
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
flowables.append(table)

doc.build(flowables)
