from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("canvas-drawing.pdf", pagesize=letter)
width, height = letter

# Draw text at coordinates (x, y)
c.drawString(100, 750, "Hello, ReportLab!")

# Draw a line
c.line(50, 700, 500, 700)

# Draw a rectangle (x, y, width, height) with fill
c.rect(100, 600, 200, 50, fill=1)

# Draw a circle (center x, center y, radius)
c.circle(300, 650, 40)

c.save()
