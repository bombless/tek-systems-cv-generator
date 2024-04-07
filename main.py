import io
import os

from configparser import ConfigParser

from docxtpl import DocxTemplate

from jobs.parser import Parser

doc = DocxTemplate("templ-CV.docx")

if not os.path.exists('config/misc.ini'):
    raise Exception('please fill config/misc.ini')
ini = ConfigParser()
ini.read('config/misc.ini', encoding='utf-8')

if not os.path.exists('config/jobs.txt'):
    raise Exception('please fill config/jobs.txt')
jobs_desc = io.open('config/jobs.txt', mode="r", encoding="utf-8")
jobs = Parser(jobs_desc.read())

context = {
    'jobs': []
}
for section in ini.sections():
    for k in ini[section]:
        context[k] = ini[section][k]
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
