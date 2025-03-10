import pdfplumber
import pdb
from lib import ContentType
from lib import ContentCharacteristics, ContentGroup
from lib import HeadingAccumulator
from lib import Document
import copy

pdf_path = 'fixtures/sample3.pdf'

heading_sentences = []
with pdfplumber.open(pdf_path) as pdf:
    document = Document()

    for page in pdf.pages:
        document.add_page(page)

for heading in document.headings:
    print("----")
    print(heading.text())

document.print_headings()
