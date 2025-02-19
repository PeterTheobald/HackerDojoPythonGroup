from reportlab.pdfgen import canvas

c = canvas.Canvas("canvas-hello.pdf")
c.drawString(100, 750, "Hello, PDF!")
c.save()
