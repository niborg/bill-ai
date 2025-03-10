import string
import re
from .casing import Casing
import pdb

class ContentCharacteristics:
    TOLERANCE = 0.1
    FORBIDDEN_START_CHARS = "‘"

    def __init__(self, font, size, casing=Casing.UNKNOWN):
        self.font = font
        self.size = float(size)
        self.casing = casing

    def __repr__(self):
        return f'Content(font={self.font}, size={self.size})'

    def characteristics_match(self, other, accept_casing=[], accept_size_diff=False):
        if self.casing == Casing.SMALL_CAPS:
            return (
                self.font == other.font
                and (self.casing == other.casing or other.casing in accept_casing)
                and (
                    accept_size_diff
                    or abs(self.size - other.size) < self.TOLERANCE
                    or (other.casing == Casing.ALL_CAPS and other.size < self.size)
                )
            )
        else:
            return (
                self.font == other.font
                and (self.casing == other.casing or other.casing in accept_casing)
                and (accept_size_diff or abs(self.size - other.size) < self.TOLERANCE)
            )

    def characteristics_consistent(self, other):
        return self.characteristics_match(other, accept_casing=[Casing.ALL_CAPS, Casing.UNKNOWN])

class ContentGroup(ContentCharacteristics):
    def __init__(self, word, casing=None):
        self.chars = word['chars']
        self.text = ''.join(item['text'] for item in self.chars)
        if not casing:
            if any(c in string.ascii_lowercase for c in self.text):
                casing = Casing.NORMAL
            elif any(c in string.digits for c in self.text):
                casing = Casing.UNKNOWN
            elif self.is_acronym():
                casing = Casing.UNKNOWN
            elif all(c['size'] == self.chars[0]['size'] for c in self.chars):
                casing = Casing.ALL_CAPS
            else:
                casing = Casing.SMALL_CAPS
        self.y_bottom = word['bottom']
        size = self.chars[0]['size']
        super().__init__(word['fontname'], size, casing=casing)


    def __repr__(self):
        return f'Content(text={self.text}, font={self.font}, size={self.size})'

    def as_characteristics(self):
        return ContentCharacteristics(self.font, self.size)

    def same_line_as(self, other):
        return abs(self.y_bottom - other.y_bottom) < 2

    def is_acronym(self):
        return bool(re.fullmatch(r'([A-Z]\.)+', self.text))

    def is_number(self):
        return bool(re.search(r'^\d+$', self.text))

    def is_punctuation(self):
        return len(self.text) == 1 and not self.text[0].isalnum()

    def starts_with_forbidden_punctuation(self):
        return self.text[0] in self.FORBIDDEN_START_CHARS

    def is_enumeration(self):
        return (
            bool(re.search(r'^\(([a-zA-Z]|\d+)\)$', self.text))
            or bool(re.search(r'^\([iIvVxXlLcCdDmM]+\)$', self.text)) # lowercase roman numerals
            or bool(re.search(r'^([a-zA-Z]|\d+)\.$', self.text))
        )
