import pdfplumber
import pdb
from lib import ContentType
from lib import ContentCharacteristics, ContentGroup
from lib import HeadingAccumulator
import copy


pdf_path = 'fixtures/sample3.pdf'

heading_sentences = []
with pdfplumber.open(pdf_path) as pdf:
    headings = []
    current_heading = None
    word_count = 0

    for page in pdf.pages:
        line_skip = None
        all_words = page.extract_words(extra_attrs=['fontname'], return_chars=True, split_at_punctuation="—")
        for index, word in enumerate(all_words):
            if line_skip:
                if word['bottom'] == line_skip:
                    continue
                else:
                    line_skip = None

            word_count += 1
            while True:
                if current_heading is None:
                    current_heading = HeadingAccumulator(width=page.width)

                if current_heading.add(word):
                    break

                if current_heading.is_heading_complete():
                    headings.append(current_heading)
                    current_heading = None
                    continue # Retry current word with new heading accumulator

                if current_heading.is_not_heading():
                    if len(current_heading.words) > 0:
                        line_skip = current_heading.words[-1]['bottom']
                        current_heading = None
                        continue
                    current_heading = None
                    line_skip = word['bottom']
                    break

                # Must be undetermined status or a heading that came across
                # something to be ignored.
                break

    for heading in headings:
        print("----")
        print(heading.result())
    print(f'Headings: {len(headings)}/{word_count}')
