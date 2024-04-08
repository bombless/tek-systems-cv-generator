import io
import os

from configparser import ConfigParser

from docxtpl import DocxTemplate

from parser.parser import Parser

doc = DocxTemplate("templ-CV.docx")

if not os.path.exists('config/misc.ini'):
    raise Exception('please fill config/misc.ini')
ini = ConfigParser()
ini.read('config/misc.ini', encoding='utf-8')

if not os.path.exists('config/jobs.txt'):
    raise Exception('please fill config/jobs.txt')
jobs_desc = io.open('config/jobs.txt', mode="r", encoding="utf-8")
jobs = Parser(jobs_desc.read())

if not os.path.exists('config/education.txt'):
    raise Exception('please fill config/education.txt')
education_desc = io.open('config/education.txt', mode="r", encoding="utf-8")
education = Parser(education_desc.read())

if not os.path.exists('config/accomplishment.txt'):
    raise Exception('please fill config/accomplishment.txt')
accomplishment_desc = io.open('config/accomplishment.txt', mode="r", encoding="utf-8")
accomplishment = Parser(accomplishment_desc.read())

context = {
    'jobs': [],
    'education': [],
    'accomplishment': [],
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
while True:
    ok, entry = education.parse_item()
    if not ok:
        break
    context['education'].append([entry[2], entry[1]])
    context['education'].append(['', entry[0] + entry[3]])
while True:
    ok, entry = accomplishment.parse_item()
    if not ok:
        break
    context['accomplishment'].append({
        'time': entry[1],
        'company': entry[2],
        'introduction': entry[3],
        'report_to': '',
        'subordinates': '',
        'responsibilities': ['foobar'],
        'technologies': entry[4],
    })
doc.render(context)
doc.save("generated_doc.docx")
