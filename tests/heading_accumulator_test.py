import pytest
import pdb
from lib import HeadingAccumulator, Casing

@pytest.fixture
def accumulator():
    return HeadingAccumulator(width=612)

class TestAccumulatorFromInitialState:
    def test_initial_state(self, accumulator):
        assert not accumulator.words
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert not accumulator.is_not_heading()

    def test_adding_content_word(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'Hi',
            'bottom': 10,
            'chars': [
                {'text': 'H', 'size': 14, 'y1': 19},
                {'text': 'i', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == False
        assert accumulator.words == []
        assert accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert accumulator.casing == Casing.NORMAL
        assert not accumulator.is_heading_complete()
        assert accumulator.is_not_heading()

    def test_adding_file_path(self, accumulator):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'text': 'L:\\v7\\12.xml',
            'bottom': 10,
            'chars': [
                {'text': 'L', 'size': 14, 'y1': 19},
                {'text': ':', 'size': 14, 'y1': 19},
                {'text': '\\', 'size': 14, 'y1': 19},
                {'text': 'v', 'size': 14, 'y1': 19},
                {'text': '7', 'size': 14, 'y1': 19},
                {'text': '\\', 'size': 14, 'y1': 19},
                {'text': '1', 'size': 14, 'y1': 19},
                {'text': '2', 'size': 14, 'y1': 19},
                {'text': '.', 'size': 14, 'y1': 19},
                {'text': 'x', 'size': 14, 'y1': 19},
                {'text': 'm', 'size': 14, 'y1': 19},
                {'text': 'l', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == False
        assert accumulator.words == []
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN

    def test_adding_bold_heading_word(self, accumulator):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'text': 'HI',
            'bottom': 10,
            'chars': [
                {'text': 'H', 'size': 14, 'y1': 19},
                {'text': 'I', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.HEADING
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

    def test_adding_all_caps_heading_word(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'HI',
            'bottom': 10,
            'chars': [
                {'text': 'H', 'size': 14, 'y1': 19},
                {'text': 'I', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

    def test_adding_number_enumeration(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '(4)',
            'bottom': 10,
            'chars': [
                {'text': '(', 'size': 14, 'y1': 19},
                {'text': '4', 'size': 14, 'y1': 19},
                {'text': ')', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

    def test_adding_lowercase_letter_enumeration(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '(d)',
            'bottom': 10,
            'chars': [
                {'text': '(', 'size': 14, 'y1': 19},
                {'text': 'd', 'size': 14, 'y1': 19},
                {'text': ')', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

    def test_adding_uppercase_letter_enumeration(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '(D)',
            'bottom': 10,
            'chars': [
                {'text': '(', 'size': 14, 'y1': 19},
                {'text': 'D', 'size': 14, 'y1': 19},
                {'text': ')', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

    def test_parenthetical_word(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '(foo)',
            'bottom': 10,
            'chars': [
                {'text': '(', 'size': 14, 'y1': 19},
                {'text': 'f', 'size': 14, 'y1': 19},
                {'text': 'o', 'size': 14, 'y1': 19},
                {'text': 'o', 'size': 14, 'y1': 19},
                {'text': ')', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == False
        assert accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert accumulator.casing == Casing.NORMAL
        assert accumulator.is_not_heading()
        assert accumulator.words == []

    def test_adding_small_caps_heading_word(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'HI',
            'bottom': 10,
            'chars': [
                {'text': 'H', 'size': 14, 'y1': 19},
                {'text': 'I', 'size': 10, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.HEADING
        assert accumulator.casing == Casing.SMALL_CAPS
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

    def test_adding_number(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '1609',
            'bottom': 10,
            'x0': 500.0,
            'x1': 520.0,
            'chars': [
                {'text': '1', 'size': 14, 'y1': 19},
                {'text': '6', 'size': 14, 'y1': 19},
                {'text': '0', 'size': 14, 'y1': 19},
                {'text': '9', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

    def test_adding_number_with_parenthesis(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '(1)',
            'bottom': 10,
            'x0': 50.0,
            'x1': 65.0,
            'chars': [
                {'text': '(', 'size': 14, 'y1': 19},
                {'text': '1', 'size': 14, 'y1': 19},
                {'text': ')', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

    def test_adding_number_with_punctuation(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '2025’’.',
            'bottom': 10,
            'x0': 500.0,
            'x1': 520.0,
            'chars': [
                {'text': '2', 'size': 14, 'y1': 19},
                {'text': '0', 'size': 14, 'y1': 19},
                {'text': '2', 'size': 14, 'y1': 19},
                {'text': '5', 'size': 14, 'y1': 19},
                {'text': '’', 'size': 14, 'y1': 19},
                {'text': '’', 'size': 14, 'y1': 19},
                {'text': '.', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

class TestAccumulatorFromNotHeadingState:
    @pytest.fixture
    def not_heading_state_accumulator(self, accumulator):
        accumulator.add(
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'Hi',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 19},
                    {'text': 'i', 'size': 14, 'y1': 19}
                ]
            }
        )
        return accumulator

    def test_adding_heading_word(self, not_heading_state_accumulator):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'text': 'Hi',
            'bottom': 10,
            'chars': [
                {'text': 'H', 'size': 18, 'y1': 19},
                {'text': 'I', 'size': 18, 'y1': 19}
            ]
        }
        assert not_heading_state_accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        with pytest.raises(HeadingAccumulator.BadStateError):
            not_heading_state_accumulator.add(word)

class TestAccumulatorFromHeadingCompleteState:
    @pytest.fixture
    def heading_complete_state_accumulator(self, accumulator):
        accumulator.add(
            {
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 18, 'y1': 19},
                    {'text': 'I', 'size': 18, 'y1': 19}
                ]
            }
        )
        accumulator.add(
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'there',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 25},
                    {'text': 'i', 'size': 14, 'y1': 25}
                ]
            }
        )
        return accumulator

    def test_adding_content_word(self, heading_complete_state_accumulator):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'text': 'Hi',
            'bottom': 10,
            'chars': [
                {'text': 'H', 'size': 18, 'y1': 21},
                {'text': 'i', 'size': 18, 'y1': 21}
            ]
        }
        assert heading_complete_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        with pytest.raises(HeadingAccumulator.BadStateError):
            heading_complete_state_accumulator.add(word)

class TestAccumulatorFromAllCapsHeadingState:
    @pytest.fixture
    def initial_word(self):
        return {
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 14, 'y1': 10}
                ]
        }

    @pytest.fixture
    def heading_state_accumulator(self, accumulator, initial_word):
        accumulator.add(initial_word)
        return accumulator

    def test_adding_content_word_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'you',
            'bottom': 10,
            'x0': 50.0,
            'x1': 70.0,
            'chars': [
                {'text': 'y', 'size': 14, 'y1': 10},
                {'text': 'o', 'size': 14, 'y1': 10},
                {'text': 'u', 'size': 14, 'y1': 10}
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_content_word_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'you',
            'bottom': 10,
            'x0': 50.0,
            'x1': 70.0,
            'chars': [
                {'text': 'y', 'size': 14, 'y1': 15},
                {'text': 'o', 'size': 14, 'y1': 15},
                {'text': 'u', 'size': 14, 'y1': 15}
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_page_number_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '20',
            'bottom': 5,
            'x0': 303.0,
            'x1': 312.0,
            'chars': [
                {'text': '2', 'size': 14, 'y1': 5},
                {'text': '0', 'size': 14, 'y1': 5},
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_page_number_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '20',
            'bottom': 10,
            'x0': 303.0,
            'x1': 312.0,
            'chars': [
                {'text': '2', 'size': 14, 'y1': 10},
                {'text': '0', 'size': 14, 'y1': 10},
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_heading_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'text': 'THERE',
            'bottom': 10,
            'chars': [
                {'text': 'T', 'size': 18, 'y1': 10},
                {'text': 'H', 'size': 18, 'y1': 10},
                {'text': 'E', 'size': 18, 'y1': 10},
                {'text': 'R', 'size': 18, 'y1': 10},
                {'text': 'E', 'size': 18, 'y1': 10},
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_heading_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'text': 'THERE',
            'bottom': 5,
            'chars': [
                {'text': 'T', 'size': 18, 'y1': 15},
                {'text': 'H', 'size': 18, 'y1': 15},
                {'text': 'E', 'size': 18, 'y1': 15},
                {'text': 'R', 'size': 18, 'y1': 15},
                {'text': 'E', 'size': 18, 'y1': 15},
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

class TestAccumulatorFromSmallCapsHeadingState:
    @pytest.fixture
    def initial_word(self):
        return {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 12, 'y1': 10}
                ]
        }

    @pytest.fixture
    def heading_state_accumulator(self, accumulator, initial_word):
        accumulator.add(initial_word)
        return accumulator

    def test_adding_content_word_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'you',
            'bottom': 10,
            'x0': 50.0,
            'x1': 70.0,
            'chars': [
                {'text': 'y', 'size': 14, 'y1': 10},
                {'text': 'o', 'size': 14, 'y1': 10},
                {'text': 'u', 'size': 14, 'y1': 10}
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.casing == Casing.SMALL_CAPS
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_content_word_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'you',
            'bottom': 10,
            'x0': 50.0,
            'x1': 70.0,
            'chars': [
                {'text': 'y', 'size': 14, 'y1': 15},
                {'text': 'o', 'size': 14, 'y1': 15},
                {'text': 'u', 'size': 14, 'y1': 15}
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_page_number_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '20',
            'bottom': 5,
            'x0': 303.0,
            'x1': 312.0,
            'chars': [
                {'text': '2', 'size': 14, 'y1': 5},
                {'text': '0', 'size': 14, 'y1': 5},
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_page_number_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '20',
            'bottom': 10,
            'x0': 303.0,
            'x1': 312.0,
            'chars': [
                {'text': '2', 'size': 14, 'y1': 10},
                {'text': '0', 'size': 14, 'y1': 10},
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_heading_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'THERE',
            'bottom': 10,
            'chars': [
                {'text': 'T', 'size': 14, 'y1': 10},
                {'text': 'H', 'size': 12, 'y1': 10},
                {'text': 'E', 'size': 12, 'y1': 10},
                {'text': 'R', 'size': 12, 'y1': 10},
                {'text': 'E', 'size': 12, 'y1': 10},
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_heading_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'THERE',
            'bottom': 5,
            'chars': [
                {'text': 'T', 'size': 14, 'y1': 15},
                {'text': 'H', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
                {'text': 'R', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_lower_caps_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'THERE',
            'bottom': 5,
            'chars': [
                {'text': 'T', 'size': 12, 'y1': 15},
                {'text': 'H', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
                {'text': 'R', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_all_caps_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'ABC',
            'bottom': 10,
            'chars': [
                {'text': 'A', 'size': 14, 'y1': 10},
                {'text': 'B', 'size': 14, 'y1': 10},
                {'text': 'C', 'size': 14, 'y1': 10}
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_all_caps_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'ABC',
            'bottom': 15,
            'chars': [
                {'text': 'A', 'size': 14, 'y1': 15},
                {'text': 'B', 'size': 14, 'y1': 15},
                {'text': 'C', 'size': 14, 'y1': 15}
            ]
        }
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    class TestAccumulationFromNumberListing:
        @pytest.fixture
        def initial_words(self):
            return [
                {
                    'fontname': 'JJGECB+DeVinne',
                    'text': '(1)',
                    'bottom': 10,
                    'chars': [
                        {'text': '(', 'size': 14, 'y1': 10},
                        {'text': '1', 'size': 14, 'y1': 10},
                        {'text': ')', 'size': 14, 'y1': 10}
                    ]
                },
                {
                    'fontname': 'JJGECB+DeVinne',
                    'text': 'IN',
                    'bottom': 10,
                    'chars': [
                        {'text': 'I', 'size': 14, 'y1': 10},
                        {'text': 'N', 'size': 12, 'y1': 10},
                    ]
                }
            ]

        @pytest.fixture
        def heading_state_accumulator(self, accumulator, initial_words):
            for word in initial_words:
                accumulator.add(word)
            return accumulator

        def test_adding_small_caps_word(self, heading_state_accumulator, initial_words):
            word = {
                'fontname': 'JJGECB+DeVinne',
                'text': 'GEN',
                'bottom': 15,
                'chars': [
                    {'text': 'G', 'size': 12, 'y1': 15},
                    {'text': 'E', 'size': 12, 'y1': 15},
                    {'text': 'N', 'size': 12, 'y1': 15},
                ]
            }
            assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
            assert heading_state_accumulator.casing == Casing.SMALL_CAPS
            assert heading_state_accumulator.add(word) == True
            assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
            assert not heading_state_accumulator.is_heading_complete()
            assert len(heading_state_accumulator.words) == 3
            assert heading_state_accumulator.words == initial_words + [word]

class TestAccumulatorFromAllCapsUndeterminedState:
    @pytest.fixture
    def initial_word(self):
        return {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 14, 'y1': 10}
                ]
        }

    @pytest.fixture
    def undetermined_state_accumulator(self, accumulator, initial_word):
        accumulator.add(initial_word)
        return accumulator

    def test_state(self, undetermined_state_accumulator, initial_word):
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert undetermined_state_accumulator.casing == Casing.UNKNOWN
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word]

    def test_adding_all_caps_word_on_same_line(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'YOU',
            'bottom': 10,
            'chars': [
                {'text': 'Y', 'size': 14, 'y1': 10},
                {'text': 'O', 'size': 14, 'y1': 10},
                {'text': 'U', 'size': 14, 'y1': 10},
            ]
        }
        assert undetermined_state_accumulator.add(word) == True
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert undetermined_state_accumulator.casing == Casing.ALL_CAPS
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word, word]

    def test_adding_small_caps_word_on_same_line(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'YOU',
            'bottom': 10,
            'chars': [
                {'text': 'Y', 'size': 14, 'y1': 10},
                {'text': 'O', 'size': 12, 'y1': 10},
                {'text': 'U', 'size': 12, 'y1': 10},
            ]
        }
        assert undetermined_state_accumulator.add(word) == True
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert undetermined_state_accumulator.casing == Casing.SMALL_CAPS
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word, word]

    def test_adding_regular_word_on_same_line(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'you',
            'bottom': 10,
            'x0': 60.0,
            'x1': 70.0,
            'chars': [
                {'text': 'y', 'size': 14, 'y1': 10},
                {'text': 'o', 'size': 14, 'y1': 10},
                {'text': 'u', 'size': 14, 'y1': 10}
            ]
        }
        assert undetermined_state_accumulator.add(word) == False
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert undetermined_state_accumulator.casing == Casing.NORMAL
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word]

    def test_adding_all_caps_word_on_different_line(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'YOU',
            'bottom': 15,
            'chars': [
                {'text': 'Y', 'size': 14, 'y1': 15},
                {'text': 'O', 'size': 14, 'y1': 15},
                {'text': 'U', 'size': 14, 'y1': 15},
            ]
        }
        assert undetermined_state_accumulator.add(word) == True
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert undetermined_state_accumulator.casing == Casing.ALL_CAPS
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word, word]

    def test_adding_small_caps_word_on_different_line(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'YOU',
            'bottom': 15,
            'chars': [
                {'text': 'Y', 'size': 14, 'y1': 15},
                {'text': 'O', 'size': 12, 'y1': 15},
                {'text': 'U', 'size': 12, 'y1': 15},
            ]
        }
        assert undetermined_state_accumulator.add(word) == False
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert undetermined_state_accumulator.casing == Casing.ALL_CAPS
        assert undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word]

    def test_adding_regular_word_on_different_line(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'you',
            'bottom': 15,
            'x0': 60.0,
            'x1': 70.0,
            'chars': [
                {'text': 'y', 'size': 14, 'y1': 15},
                {'text': 'o', 'size': 14, 'y1': 15},
                {'text': 'u', 'size': 14, 'y1': 15}
            ]
        }
        assert undetermined_state_accumulator.add(word) == False
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert undetermined_state_accumulator.casing == Casing.ALL_CAPS
        assert undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word]

class TestAccumulatorFromNumberParentheticalUndeterminedState:
    @pytest.fixture
    def initial_word(self):
        return {
                'fontname': 'JJGECB+DeVinne',
                'text': '(1)',
                'bottom': 10,
                'chars': [
                    {'text': '(', 'size': 14, 'y1': 10},
                    {'text': '1', 'size': 14, 'y1': 10},
                    {'text': '1', 'size': 14, 'y1': 10}
                ]
        }

    @pytest.fixture
    def undetermined_state_accumulator(self, accumulator, initial_word):
        accumulator.add(initial_word)
        return accumulator

    def test_state(self, undetermined_state_accumulator, initial_word):
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert undetermined_state_accumulator.casing == Casing.UNKNOWN
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word]

    def test_adding_normal_word(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'you',
            'bottom': 10,
            'x0': 60.0,
            'x1': 70.0,
            'chars': [
                {'text': 'y', 'size': 14, 'y1': 10},
                {'text': 'o', 'size': 14, 'y1': 10},
                {'text': 'u', 'size': 14, 'y1': 10}
            ]
        }
        assert undetermined_state_accumulator.add(word) == False
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert undetermined_state_accumulator.casing == Casing.NORMAL
        assert undetermined_state_accumulator.is_not_heading()
        assert undetermined_state_accumulator.words == [initial_word]

    def test_adding_small_caps_word(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'HI',
            'bottom': 10,
            'x0': 70.0,
            'x1': 80.0,
            'chars': [
                {'text': 'H', 'size': 14, 'y1': 10},
                {'text': 'I', 'size': 12, 'y1': 10},
            ]
        }
        assert undetermined_state_accumulator.add(word) == True
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert undetermined_state_accumulator.casing == Casing.SMALL_CAPS
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word, word]

    def test_adding_all_caps_word(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'HI',
            'bottom': 10,
            'x0': 60.0,
            'x1': 70.0,
            'chars': [
                {'text': 'H', 'size': 14, 'y1': 10},
                {'text': 'I', 'size': 14, 'y1': 10},
            ]
        }
        assert undetermined_state_accumulator.add(word) == True
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert undetermined_state_accumulator.casing == Casing.UNKNOWN
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word, word]

class TestAccumulatorFromNumberUndeterminedState:
    @pytest.fixture
    def initial_word(self):
        return {
                'fontname': 'JJGECB+DeVinne',
                'text': '30,',
                'bottom': 10,
                'chars': [
                    {'text': '3', 'size': 14, 'y1': 10},
                    {'text': '0', 'size': 14, 'y1': 10},
                    {'text': ',', 'size': 14, 'y1': 10}
                ]
        }

    @pytest.fixture
    def undetermined_state_accumulator(self, accumulator, initial_word):
        accumulator.add(initial_word)
        return accumulator

    def test_state(self, undetermined_state_accumulator, initial_word):
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert undetermined_state_accumulator.casing == Casing.UNKNOWN
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word]

    def test_adding_normal_word(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'you',
            'bottom': 10,
            'x0': 60.0,
            'x1': 70.0,
            'chars': [
                {'text': 'y', 'size': 14, 'y1': 10},
                {'text': 'o', 'size': 14, 'y1': 10},
                {'text': 'u', 'size': 14, 'y1': 10}
            ]
        }
        assert undetermined_state_accumulator.add(word) == False
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert undetermined_state_accumulator.casing == Casing.NORMAL
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word]

    def test_adding_another_number(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '2024.',
            'bottom': 10,
            'chars': [
                {'text': '2', 'size': 14, 'y1': 10},
                {'text': '0', 'size': 14, 'y1': 10},
                {'text': '2', 'size': 14, 'y1': 10},
                {'text': '4', 'size': 14, 'y1': 10}
            ]
        }
        assert undetermined_state_accumulator.add(word) == True
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert undetermined_state_accumulator.casing == Casing.UNKNOWN
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word, word]
