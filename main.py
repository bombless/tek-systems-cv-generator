from docxtpl import DocxTemplate
from jobs.parser import Parser
import os, io

doc = DocxTemplate("templ-CV.docx")

if not os.path.exists('jobs/jobs.txt'):
    raise Exception('please fill jobs/jobs.txt')
jobs_desc = io.open('jobs/jobs.txt', mode="r", encoding="utf-8")
jobs = Parser(jobs_desc.read())

context = {'jobs': []}
while True:
    ok, entry = jobs.parse_item()
    if not ok:
        break
    context['jobs'].append({
        'company': entry[0],
        'time': entry[2],
        'title': entry[1]
    })
doc.render(context)
doc.save("generated_doc.docx")
