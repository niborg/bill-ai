import pdfplumber
from lib import ContentType
from lib import ContentCharacteristics, ContentGroup
from lib import HeadingAccumulator


pdf_path = 'fixtures/sample3.pdf'

heading_sentences = []
with pdfplumber.open(pdf_path) as pdf:
    headings = []
    current_heading = None
    word_count = 0

    for page in pdf.pages:
        line_skip = None
        all_words = page.extract_words(extra_attrs=['fontname'], return_chars=True, split_at_punctuation='–—')
        for index, word in enumerate(all_words):
            word_count += 1

            if line_skip:
                if word['bottom'] == line_skip:
                    continue
                else:
                    line_skip = None

            if current_heading is None: current_heading = HeadingAccumulator(width=page.width)

            current_heading.add(word)

            if current_heading.is_heading_complete():
                headings.append(current_heading)
                current_heading = None
            elif current_heading.is_not_heading():
                current_heading = None
                line_skip = word['bottom']

    for heading in headings:
        print("----")
        print(heading.result())
    print(f'Headings: {len(headings)}/{word_count}')
