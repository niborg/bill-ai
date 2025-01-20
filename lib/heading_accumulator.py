import re
import pdb
import string
from enum import Enum
from .content_type import ContentType
from .casing import Casing
from .content_descriptors import ContentGroup, ContentCharacteristics

CONTENT_TYPES = {
    ContentType.CONTENT: ContentCharacteristics("JJGECB+DeVinne", 14.0, casing=Casing.NORMAL),
    ContentType.CONTENT_ALT_1: ContentCharacteristics("JJGECE+DeVinne-Italic", 14.0, casing=Casing.NORMAL),
    ContentType.INTRODUCTORY_SECTION: ContentCharacteristics("JJGECG+NewCenturySchlbk-Bold", 10.0, casing=Casing.NORMAL),
    ContentType.LINE_NUMBER: ContentCharacteristics("JJGECF+Times-Roman", 14.0, casing=Casing.UNKNOWN),
    ContentType.PREAMBLE: ContentCharacteristics("JJGECE+DeVinne-Italic", 14.0, casing=Casing.NORMAL),
    ContentType.TOC_ITEM: ContentCharacteristics("JJGECB+DeVinne", 10.0, casing=Casing.NORMAL),
    ContentType.TOC_HEADING: ContentCharacteristics("JJGECB+DeVinne", 10.0, casing=Casing.ALL_CAPS),
    ContentType.PAGE_NUMBER: ContentCharacteristics("JJGECB+DeVinne", 14.0, casing=Casing.NORMAL),
    ContentType.FILE_PATH: ContentCharacteristics("JJGECF+Times-Roman", 10.0, casing=Casing.NORMAL),
    ContentType.DIVISION_HEADING_1: ContentCharacteristics("JJGECG+NewCenturySchlbk-Bold", 14.0, casing=Casing.ALL_CAPS),
    ContentType.DIVISION_HEADING_2: ContentCharacteristics("JJGECG+NewCenturySchlbk-Bold", 18.0, casing=Casing.ALL_CAPS),
    ContentType.DIVISION_SUBHEADING_1: ContentCharacteristics("JJGECB+DeVinne", 14.0, casing=Casing.ALL_CAPS),
    ContentType.DIVISION_SUBHEADING_2: ContentCharacteristics("JJGECB+DeVinne", 14.0, casing=Casing.SMALL_CAPS),
    ContentType.LAW_SECTION: ContentCharacteristics("JJGECG+NewCenturySchlbk-Bold", 10.0, casing=Casing.ALL_CAPS)
}
HEADINGS = [
    ContentType.DIVISION_HEADING_1,
    ContentType.DIVISION_HEADING_2,
    ContentType.DIVISION_SUBHEADING_2,
    ContentType.LAW_SECTION
]
POSSIBLE_HEADINGS = [
    ContentType.DIVISION_SUBHEADING_1
]
IGNORABLE = [
    ContentType.LINE_NUMBER
]
CONTENT = [
    ContentType.CONTENT,
    ContentType.CONTENT_ALT_1,
    ContentType.PREAMBLE,
    ContentType.INTRODUCTORY_SECTION,
    ContentType.TOC_ITEM,
    ContentType.TOC_HEADING
]

class HeadingAccumulator:
    class BadStateError(Exception): pass

    class Status(Enum):
        UNDETERMINED = 1
        HEADING = 2
        HEADING_COMPLETE = 3
        NOT_HEADING = 4

    FILE_PATH_REGEX = re.compile(r'^[A-Za-z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$')
    POSITION_TOLERANCE = 5.0

    def __init__(self, *, width):
        self.words = []
        self.width = width
        self.status = self.Status.UNDETERMINED
        self.casing = Casing.UNKNOWN

    def is_heading_complete(self):
        return self.status == self.Status.HEADING_COMPLETE

    def is_not_heading(self):
        return self.status == self.Status.NOT_HEADING

    def result(self):
        return " ".join([word['text'] for word in self.words])

    def add(self, word):
        """
          Adds a word to the accumulator. Will determine if whether the word
          matches the current heading, or, if nothing has accumulated yet, whether
          it satisfies the criteria for a heading.

          NOTE: If accumulator is new, it is assumed that the word passed is the
          first word in a document line.
        """
        if self.status in {self.Status.NOT_HEADING, self.Status.HEADING_COMPLETE}:
            raise self.BadStateError('HeadingAccumulator in completed state')

        candidate = ContentGroup(word)
        if self._is_ignorable(word) or self._is_ignorable_by_font(candidate): return False

        if self.status == self.Status.HEADING:
            if candidate.is_punctuation() and self._has_main_content_font_and_size(candidate):
                self.status = self.Status.HEADING_COMPLETE
                return False
            elif self._matches(candidate):
                # Case 1: We are a heading and the next candidate matches, so
                # we add it to the accumulator.
                self.words.append(word)
                if self.casing == Casing.UNKNOWN and candidate.casing != Casing.UNKNOWN:
                    self.casing = candidate.casing
                return True
            else:
                # Case 2: We are a heading and the next candidate does not match,
                # so we mark the accumulator as complete.
                self.status = self.Status.HEADING_COMPLETE
                return False
            # TODO: When small caps heading accumulated, but next word is on new line
            # and is all-caps lowercase – should still be part of the heading.
        elif not self.words:
            if candidate.is_punctuation() or candidate.starts_with_forbidden_punctuation():
                # Case 3: We have no words accumulated yet, but received a punctuation
                # word. This is not a heading.
                self.status = self.Status.NOT_HEADING
                return False
            elif self._has_main_content_characteristics(candidate):
                if (
                    candidate.casing == Casing.ALL_CAPS
                    or candidate.is_enumeration()
                    or candidate.is_number()
                    or candidate.is_acronym()
                ):
                    # Case 4: We have no words accumulated yet, but received an
                    # all-caps or parenthetical enumeration word. Unknown if
                    # this is a heading at this point.
                    self.words.append(word)
                    return True
                elif candidate.casing == Casing.SMALL_CAPS:
                    # Case 5: We have no words accumulated yet, but received a
                    # a small-caps word. This is a heading.
                    self.words.append(word)
                    self.status = self.Status.HEADING
                    self.casing = Casing.SMALL_CAPS
                    return True
                elif any(c in string.punctuation for c in candidate.text):
                    # Case 6: We have no words accumulated yet, but received a
                    # word with punctuation and we already know it is not an
                    # enumeration or acronym. This is not a heading.
                    self.status = self.Status.NOT_HEADING
                    return False
                else:
                    # Case 7: We have no words accumulated yet, but received a
                    # normal-cased word. This is not a heading.
                    self.status = self.Status.NOT_HEADING
                    self.casing = Casing.NORMAL
                    return False
            elif self._has_heading_characteristics(candidate):
                # Case 8: We have no words accumulated yet, but received a word
                # that matches one of the definitive heading content types.
                self.words.append(word)
                if candidate.casing in {Casing.NORMAL, Casing.SMALL_CAPS}:
                    # With all-caps words, unclear if that is the casing just yet.
                    self.casing = candidate.casing
                self.status = self.Status.HEADING
                return True
            elif self._has_ambiguous_heading_characteristics(candidate):
                # Case 9: We have no words accumulated yet, but received a word
                # that is ambiguous about whether it could be a heading.
                self.words.append(word)
                return True
            else:
                # Case 10: We have no words accumulated yet, and received a word
                # that does not match any known content types. This is not a heading.
                self.status = self.Status.NOT_HEADING
                return False
        else:
            # We have words accumulated, but we don't know if this is a heading yet.
            # This means we have word(s) that are all-caps or numbers so far that
            # matches main content font, thus potential all-caps or small-caps heading.
            if candidate.is_enumeration():
                # Case 11: We have an ambiguous heading word, but we get an enumeration.
                # Enumerations should start headings, so this can't be a heading.
                self.status = self.Status.NOT_HEADING
                return False
            elif candidate.same_line_as(ContentGroup(self.words[-1])) and self._is_main_content(candidate):
                # Case 12: We have an ambiguous heading word accumulated, but got a main
                # content word on same line that has lowercase letters in it. Not a heading.
                self.status = self.Status.NOT_HEADING
                self.casing = Casing.NORMAL
                return False
            elif candidate.same_line_as(ContentGroup(self.words[-1])) and self._matches(candidate):
                # Case 13: We have an upper-case/number word accumulated, and the next word
                # is on the same line and is also ambiguous. Should keep same status.
                self.words.append(word)
                if self._has_two_or_more_all_caps():
                    self.status = self.Status.HEADING
                    self.casing = Casing.ALL_CAPS
                elif candidate.casing == Casing.SMALL_CAPS:
                    self.status = self.Status.HEADING
                    self.casing = Casing.SMALL_CAPS
                return True
            elif (
                candidate.same_line_as(ContentGroup(self.words[-1]))
                and self._matches(candidate, accept_casing=Casing.SMALL_CAPS)
            ):
                # TODO: this might be covered by the case above now. Can remove.
                # Case 14: We have an upper-case/number word accumulated, and the next word is
                # on the same line and is small-caps. Should be small-caps heading.
                self.words.append(word)
                self.status = self.Status.HEADING
                self.casing = Casing.SMALL_CAPS
                return True
            elif candidate.same_line_as(ContentGroup(self.words[-1])):
                # Case 15: We have an upper-case/number word accumulated, and the next word is
                # on the same line and is not upper-case. This is not a heading.
                self.status = self.Status.NOT_HEADING
                self.casing = Casing.NORMAL
                return False
            elif len(self.words) == 1 and ContentGroup(self.words[-1]).is_enumeration():
                # Case 16: We have an enumeration word accumulated, but the next word is
                # on a different line. This is not a heading.
                self.status = self.Status.NOT_HEADING
                return False
            elif self._matches(candidate) and candidate.casing == Casing.ALL_CAPS:
                # Case 17: We have an upper-case/number word accumulated, but the next word is
                # on a different line and is all-caps. This is treated as a continued heading.
                self.words.append(word)
                self.status = self.Status.HEADING
                self.casing = Casing.ALL_CAPS
                return True
            else:
                # Case 18: We have ambiguous word set accumulated, but the next word is
                # on a different line and not matching. The heading is complete but
                # the next word is not part of the heading.
                self.status = self.Status.HEADING_COMPLETE
                self.casing = Casing.ALL_CAPS
                return False

    def _is_page_number(self, word):
        if not word['text'].isdigit():
            return False
        if len(self.words) > 0 and self.words[-1]['bottom'] == word['bottom']:
            return False

        word_center = (word['x0'] + word['x1']) / 2.0
        return abs(word_center - self.width / 2.0) < self.POSITION_TOLERANCE


    def _is_ignorable(self, word):
        return self._is_page_number(word) or bool(self.FILE_PATH_REGEX.match(word['text']))

    def _is_ignorable_by_font(self, candidate):
         return any(CONTENT_TYPES[content_type].characteristics_match(candidate) for content_type in IGNORABLE)

    def _has_heading_characteristics(self, candidate):
        return any(CONTENT_TYPES[content_type].characteristics_match(candidate) for content_type in HEADINGS)

    def _has_ambiguous_heading_characteristics(self, candidate):
        return any(CONTENT_TYPES[content_type].characteristics_match(candidate) for content_type in POSSIBLE_HEADINGS)

    def _has_main_content_characteristics(self, candidate):
        return (
            any(CONTENT_TYPES[content_type].characteristics_match(candidate, accept_casing=[Casing.UNKNOWN]) for content_type in CONTENT)
        )

    def _is_main_content(self, candidate):
        return self._has_main_content_characteristics(candidate) and any(c in string.ascii_lowercase for c in candidate.text)

    def _matches(self, candidate, accept_casing=None):
            # TODO: handle comparison of size when small caps encountered
            # Probably should not be comparing every word, but memoize a
            # characteristic state of the heading as we accumulate.
        allowable_casing = [Casing.ALL_CAPS, Casing.UNKNOWN]
        if accept_casing: allowable_casing.append(accept_casing)

        if self.casing != Casing.UNKNOWN:
            allowable_casing.append(self.casing)
        else:
            allowable_casing += [Casing.NORMAL, Casing.SMALL_CAPS]

        if self.casing in {Casing.SMALL_CAPS, Casing.UNKNOWN}:
            accept_size_diff = True
        else:
            accept_size_diff = False

        return ContentGroup(self.words[0]).characteristics_match(candidate, accept_casing=allowable_casing, accept_size_diff=accept_size_diff)

    def _has_two_or_more_all_caps(self):
        count = 0
        for word in self.words:
            if ContentGroup(word).casing == Casing.ALL_CAPS:
                count += 1

        return count >= 2

    def _has_main_content_font_and_size(self, candidate):
        return (
            CONTENT_TYPES[ContentType.CONTENT].size == candidate.size and
            CONTENT_TYPES[ContentType.CONTENT].font == candidate.font
        )
