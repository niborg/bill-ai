import re
import pdb
import string
from enum import Enum
from .content_type import ContentType
from .casing import Casing
from .content_group import ContentGroup
from .content_descriptors import CONTENT_TYPES, HEADINGS, POSSIBLE_HEADINGS, IGNORABLE, CONTENT, HEADING_HIERARCHY

# TODO:Fix duplicative parenthetical, e.g., ECONOMIC DEVELOPMENT ASSISTANCE PROGRAMS (INCLUDING (INCLUDING TRANSFERS OF FUNDS)
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
        self.index_of_suspect_heading_word = None

    def is_heading_complete(self):
        return self.status == self.Status.HEADING_COMPLETE

    def is_not_heading(self):
        return self.status == self.Status.NOT_HEADING

    def text(self):
        return " ".join([word['text'] for word in self.heading_words()])

    def heading_words(self):
        return self.words[:self.index_of_suspect_heading_word]

    @property
    def tier(self):
        if self.status == self.Status.NOT_HEADING:
            return None

        if self.status != self.Status.HEADING_COMPLETE:
            raise self.BadStateError(f'HeadingAccumulator must be in complete state to determine tier {self.status}, got {self.text()}')

        if ContentGroup(self.words[0]).is_enumeration():
            # Enumerations tend to be small sections that, and also require more
            # complication hierarchy handling if we treat them as tiered headings.
            return None

        for index, content_type in enumerate(HEADING_HIERARCHY):
            if all(
                CONTENT_TYPES[content_type].characteristics_consistent(ContentGroup(word)) for word in self.heading_words()
            ):
                return index + 1
        return None

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
                # Case 1: We are a heading and the next candidate is a punctuation that
                # matches main content. Signals end of the heading.
                self.status = self.Status.HEADING_COMPLETE
                return False
            elif (
                self._matches(candidate)
                and not (candidate.is_enumeration() and self._word_is_on_new_line(word))
            ):
                # Case 2: We are a heading and the next candidate matches, so
                # we add it to the accumulator after some housekeeping.
                if self.casing == Casing.SMALL_CAPS:
                    # Edge case handling for small-caps heading. If we have a
                    # small-caps heading accumulated, and the next word on a
                    # different line with all-caps lowercase letters, it could
                    # be either part of the heading or its own heading.
                    if (
                        candidate.casing == Casing.ALL_CAPS and
                        self._is_approximately_small_caps_size(word['chars'][0]['size'])
                    ):
                        if self._word_is_on_new_line(word):
                            if self.index_of_suspect_heading_word is None:
                                self.index_of_suspect_heading_word = len(self.words)
                            else:
                                # Now we have a second line of a potentially new heading.
                                # We can assume we have been accumulating a new heading.
                                # Add the word so that it can be returned easily for reprocessing.
                                self.words.append(word)
                                self.status = self.Status.HEADING_COMPLETE
                                return False
                    else:
                        # We can remove any suspicion that we are accumulating a new heading.
                        self.index_of_suspect_heading_word = None
                elif self.casing == Casing.UNKNOWN and candidate.casing != Casing.UNKNOWN:
                    # Set the casing if we have a new word with known casing.
                    self.casing = candidate.casing

                self.words.append(word)
                return True
            else:
                # Case 3: We are a heading and the next candidate does not match,
                # so we mark the accumulator as complete.
                self.status = self.Status.HEADING_COMPLETE
                return False
        elif not self.words:
            if candidate.is_punctuation() or candidate.starts_with_forbidden_punctuation():
                # Case 4: We have no words accumulated yet, but received a punctuation
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
                    # Case 5: We have no words accumulated yet, but received an
                    # all-caps or parenthetical enumeration word. Unknown if
                    # this is a heading at this point.
                    self.words.append(word)
                    return True
                elif candidate.casing == Casing.SMALL_CAPS:
                    # Case 6: We have no words accumulated yet, but received a
                    # a small-caps word. This is a heading.
                    self.words.append(word)
                    self.status = self.Status.HEADING
                    self.casing = Casing.SMALL_CAPS
                    self.content_type = self._resolve_heading_content_type(candidate)
                    return True
                elif any(c in string.punctuation for c in candidate.text):
                    # Case 7: We have no words accumulated yet, but received a
                    # word with punctuation and we already know it is not an
                    # enumeration or acronym. This is not a heading.
                    self.status = self.Status.NOT_HEADING
                    return False
                else:
                    # Case 8: We have no words accumulated yet, but received a
                    # normal-cased word. This is not a heading.
                    self.status = self.Status.NOT_HEADING
                    self.casing = Casing.NORMAL
                    return False
            elif self._has_heading_characteristics(candidate):
                # Case 9: We have no words accumulated yet, but received a word
                # that matches one of the definitive heading content types.
                self.words.append(word)
                if candidate.casing in {Casing.NORMAL, Casing.SMALL_CAPS}:
                    # With all-caps words, unclear if that is the casing just yet.
                    self.casing = candidate.casing
                self.status = self.Status.HEADING
                self.content_type = self._resolve_heading_content_type(candidate)
                return True
            elif self._has_ambiguous_heading_characteristics(candidate):
                # Case 10: We have no words accumulated yet, but received a word
                # that is ambiguous about whether it could be a heading.
                self.words.append(word)
                return True
            else:
                # Case 11: We have no words accumulated yet, and received a word
                # that does not match any known content types. This is not a heading.
                self.status = self.Status.NOT_HEADING
                return False
        else:
            # We have words accumulated, but we don't know if this is a heading yet.
            # This means we have word(s) that are all-caps or numbers so far that
            # matches main content font, thus potential all-caps or small-caps heading.
            if candidate.is_enumeration():
                # Case 12: We have an ambiguous heading word, but we get an enumeration.
                # Enumerations should start headings, so this can't be a heading.
                self.status = self.Status.NOT_HEADING
                return False
            elif candidate.same_line_as(ContentGroup(self.words[-1])) and self._is_main_content(candidate):
                # Case 13: We have an ambiguous heading word accumulated, but got a main
                # content word on same line that has lowercase letters in it. Not a heading.
                self.status = self.Status.NOT_HEADING
                self.casing = Casing.NORMAL
                return False
            elif candidate.same_line_as(ContentGroup(self.words[-1])) and self._matches(candidate):
                # Case 14: We have an upper-case/number word accumulated, and the next word
                # is on the same line and is also ambiguous. Should keep same status.
                self.words.append(word)
                if self._has_two_or_more_all_caps():
                    self.status = self.Status.HEADING
                    self.casing = Casing.ALL_CAPS
                    self.content_type = self._resolve_heading_content_type(candidate)
                elif candidate.casing == Casing.SMALL_CAPS:
                    self.status = self.Status.HEADING
                    self.casing = Casing.SMALL_CAPS
                    self.content_type = self._resolve_heading_content_type(candidate)
                return True
            elif (
                candidate.same_line_as(ContentGroup(self.words[-1]))
                and self._matches(candidate, accept_casing=Casing.SMALL_CAPS)
            ):
                # Case 15: We have an upper-case/number word accumulated, and the next word is
                # on the same line and is small-caps. Should be small-caps heading.
                self.words.append(word)
                self.status = self.Status.HEADING
                self.casing = Casing.SMALL_CAPS
                self.content_type = self._resolve_heading_content_type(candidate)
                return True
            elif candidate.same_line_as(ContentGroup(self.words[-1])):
                # Case 16: We have an upper-case/number word accumulated, and the next word is
                # on the same line and is not upper-case. This is not a heading.
                self.status = self.Status.NOT_HEADING
                self.casing = Casing.NORMAL
                return False
            elif len(self.words) == 1 and ContentGroup(self.words[-1]).is_enumeration():
                # Case 17: We have an enumeration word accumulated, but the next word is
                # on a different line. This is not a heading.
                self.status = self.Status.NOT_HEADING
                return False
            elif self._matches(candidate) and candidate.casing == Casing.ALL_CAPS:
                # Case 18: We have an upper-case/number word accumulated, but the next word is
                # on a different line and is all-caps. This is treated as a continued heading.
                self.words.append(word)
                self.status = self.Status.HEADING
                self.casing = Casing.ALL_CAPS
                self.content_type = self._resolve_heading_content_type(candidate)
                return True
            else:
                # Case 19: We have ambiguous word set accumulated, but the next word is
                # on a different line and not matching. The heading is complete but
                # the next word is not part of the heading.
                self.status = self.Status.HEADING_COMPLETE
                self.casing = Casing.ALL_CAPS
                self.content_type = self._resolve_heading_content_type(ContentGroup(self.words[-1]))
                return False

    def accumulated_subheading_words(self):
        if self.index_of_suspect_heading_word is None:
            return []

        return self.words[self.index_of_suspect_heading_word:]

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

    def _resolve_heading_content_type(self, candidate):
        for content_type in HEADINGS:
            if CONTENT_TYPES[content_type].characteristics_match(candidate):
                return content_type
        return None

    def _has_punctuation(self, text):
        return any(p in text for p in string.punctuation)

    def _small_caps_size(self):
        size = self.words[0]['chars'][0]['size']
        for word in self.words:
            for char in word['chars']:
                if char['size'] < size:
                    return char['size']
        return None

    def _is_approximately_small_caps_size(self, size):
        return abs(size - self._small_caps_size()) < 0.1

    def _word_is_on_new_line(self, word):
        return abs(word['bottom'] - self.words[-1]['bottom']) > 2
