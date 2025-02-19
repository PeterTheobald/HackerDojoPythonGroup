# Merge two PDFs into one
import PyPDF2

merger = PyPDF2.PdfMerger()
pdfs = ['file1.pdf', 'file2.pdf']

for pdf in pdfs:
    merger.append(pdf)

merger.write('merged.pdf')
merger.close()
