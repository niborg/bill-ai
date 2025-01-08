import string
import re
from .casing import Casing

class ContentCharacteristics:
    TOLERANCE = 0.1

    def __init__(self, font, size, casing=Casing.UNKNOWN):
        self.font = font
        self.size = float(size)
        self.casing = casing

    def __repr__(self):
        return f'Content(font={self.font}, size={self.size})'

    def characteristics_match(self, other, accept_casing=[], accept_size_diff=False):
        return (
            self.font == other.font
            and (self.casing == other.casing or other.casing in accept_casing)
            and (accept_size_diff or abs(self.size - other.size) < self.TOLERANCE)
        )

class ContentGroup(ContentCharacteristics):
    def __init__(self, word, casing=None):
        self.chars = word['chars']
        self.text = ''.join(item['text'] for item in self.chars)
        if not casing:
            if any(c in string.ascii_lowercase for c in self.text):
                casing = Casing.NORMAL
            elif any(c in string.digits for c in self.text):
                casing = Casing.UNKNOWN
            elif self._is_acronym(self.text):
                casing = Casing.UNKNOWN
            elif all(c['size'] == self.chars[0]['size'] for c in self.chars):
                casing = Casing.ALL_CAPS
            else:
                casing = Casing.SMALL_CAPS
        self.y_bottom = self.chars[0]['y1']
        size = self.chars[0]['size']
        super().__init__(word['fontname'], size, casing=casing)


    def __repr__(self):
        return f'Content(text={self.text}, font={self.font}, size={self.size})'

    def as_characteristics(self):
        return ContentCharacteristics(self.font, self.size)

    def same_line_as(self, other):
        return self.y_bottom == other.y_bottom

    def _is_acronym(self, word):
        return bool(re.fullmatch(r'([A-Z]\.)+', word))
