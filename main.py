from docxtpl import DocxTemplate

doc = DocxTemplate("templ-CV.docx")
context = {'jobs': [
    {'time': '2022', 'company': 'ds', 'title': 'engineer'}
]}
doc.render(context)
doc.save("generated_doc.docx")
