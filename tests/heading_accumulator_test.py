import pytest
import pdb
from lib import HeadingAccumulator, Casing

ROMAN_NUMERALS = [
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
    "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "ixx", "xx",
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "IXX", "XX",
]

@pytest.fixture
def accumulator():
    return HeadingAccumulator(width=612)

class TestFromInitialState:
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

    def test_quote_letter_enumeration(self, accumulator):
        words = [
            {
                'fontname': 'JJGECB+DeVinne',
                'text': '"(c)',
                'bottom': 10,
                'chars': [
                    {'text': '“', 'size': 14, 'y1': 10},
                    {'text': '(', 'size': 14, 'y1': 10},
                    {'text': 'c', 'size': 14, 'y1': 10},
                    {'text': ')', 'size': 14, 'y1': 10},
                ]
            }
        ]
        assert accumulator.add(words[0]) == False
        assert accumulator.status == HeadingAccumulator.Status.NOT_HEADING

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

    @pytest.mark.parametrize("roman_numeral", ROMAN_NUMERALS)
    def test_adding_roman_numeral_parenthetical_enumeration(self, accumulator, roman_numeral):
        chars = (
            [{'text': '(', 'size': 14, 'y1': 10}] +
            [{'text': char, 'size': 14, 'y1': 10} for char in roman_numeral] +
            [{'text': ')', 'size': 14, 'y1': 10}]
        )
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': f'({roman_numeral})',
            'bottom': 10,
            'chars': chars
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
        assert accumulator.casing == Casing.UNKNOWN
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

    def test_adding_number_with_period(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '3.',
            'bottom': 10,
            'x0': 500.0,
            'x1': 520.0,
            'chars': [
                {'text': '3', 'size': 14, 'y1': 19},
                {'text': '.', 'size': 14, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        assert accumulator.casing == Casing.UNKNOWN
        assert not accumulator.is_heading_complete()
        assert accumulator.words == [word]

    def test_adding_number_in_parenthesis(self, accumulator):
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

    def test_adding_number_with_quotes(self, accumulator):
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
        assert accumulator.add(word) == False
        assert accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert accumulator.casing == Casing.UNKNOWN
        assert accumulator.is_not_heading
        assert accumulator.words == []

    def test_adding_number_with_comma(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '30,',
            'bottom': 10,
            'x0': 500.0,
            'x1': 520.0,
            'chars': [
                {'text': '3', 'size': 14, 'y1': 19},
                {'text': '0', 'size': 14, 'y1': 19},
                {'text': ',', 'size': 14, 'y1': 19},
            ]
        }
        assert accumulator.add(word) == False
        assert accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert accumulator.casing == Casing.UNKNOWN
        assert accumulator.is_not_heading
        assert accumulator.words == []

    def test_adding_heading_style_emdash(self, accumulator):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'text': '—',
            'bottom': 10,
            'x0': 500.0,
            'x1': 520.0,
            'chars': [
                {'text': '—', 'size': 18, 'y1': 19}
            ]
        }
        assert accumulator.add(word) == False
        assert accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert accumulator.casing == Casing.UNKNOWN
        assert accumulator.is_not_heading
        assert accumulator.words == []

class TestFromNotHeadingState:
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

class TestFromHeadingCompleteState:
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

class TestFromHeadingFontUnknownCapsState:
    @pytest.fixture
    def initial_word(self):
        return {
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 18, 'y1': 10},
                    {'text': 'I', 'size': 18, 'y1': 10}
                ]
        }

    @pytest.fixture
    def heading_state_accumulator(self, accumulator, initial_word):
        accumulator.add(initial_word)
        return accumulator

    def test_state(self, heading_state_accumulator, initial_word):
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.casing == Casing.UNKNOWN
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_matching_font_all_caps_word_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'bottom': initial_word['bottom'],
            'text': 'YOU',
            'chars': [
                {'text': 'Y', 'size': 18, 'y1': initial_word['bottom']},
                {'text': 'O', 'size': 18, 'y1': initial_word['bottom']},
                {'text': 'U', 'size': 18, 'y1': initial_word['bottom']},
            ]
        }

        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.casing == Casing.UNKNOWN
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_matching_font_normal_caps_word_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'bottom': initial_word['bottom'],
            'text': 'you',
            'chars': [
                {'text': 'y', 'size': 18, 'y1': initial_word['bottom']},
                {'text': 'o', 'size': 18, 'y1': initial_word['bottom']},
                {'text': 'u', 'size': 18, 'y1': initial_word['bottom']},
            ]
        }

        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.casing == Casing.NORMAL
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_matching_font_all_caps_word_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'bottom': initial_word['bottom'],
            'text': 'YOU',
            'chars': [
                {'text': 'Y', 'size': 18, 'y1': initial_word['bottom']},
                {'text': 'O', 'size': 18, 'y1': initial_word['bottom']},
                {'text': 'U', 'size': 18, 'y1': initial_word['bottom']},
            ]
        }

        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.casing == Casing.ALL_CAPS
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_matching_font_small_caps_word_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'bottom': initial_word['bottom'],
            'text': 'YOU',
            'chars': [
                {'text': 'Y', 'size': 18, 'y1': initial_word['bottom']},
                {'text': 'O', 'size': 15, 'y1': initial_word['bottom']},
                {'text': 'U', 'size': 15, 'y1': initial_word['bottom']},
            ]
        }

        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.casing == Casing.SMALL_CAPS
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_content_word_on_same_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'there',
            'bottom': initial_word['bottom'],
            'chars': [
                {'text': 't', 'size': 14, 'y1': initial_word['bottom']},
                {'text': 'h', 'size': 14, 'y1': initial_word['bottom']},
                {'text': 'e', 'size': 14, 'y1': initial_word['bottom']},
                {'text': 'r', 'size': 14, 'y1': initial_word['bottom']},
                {'text': 'e', 'size': 14, 'y1': initial_word['bottom']}
            ]
        }
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

class TestFromAllCapsHeadingState:
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
            'bottom': 15,
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

    def test_adding_diff_enumerated_heading_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '(a)',
            'bottom': 15,
            'chars': [
                {'text': '(', 'size': 14, 'y1': 15},
                {'text': 'a', 'size': 14, 'y1': 15},
                {'text': ')', 'size': 14, 'y1': 15}
            ]
        }
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_heading_matching_emdash(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'text': '—',
            'bottom': 10,
            'chars': [
                {'text': '—', 'size': 18, 'y1': 10}
            ]
        }
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

class TestFromSmallCapsHeadingState:
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

    def test_state(self, heading_state_accumulator):
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert heading_state_accumulator.casing == Casing.SMALL_CAPS

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
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_heading_on_diff_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'THERE',
            'bottom': 15,
            'chars': [
                {'text': 'T', 'size': 14, 'y1': 15},
                {'text': 'H', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
                {'text': 'R', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
            ]
        }
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_words_on_next_line_starts_small_caps(self, heading_state_accumulator, initial_word):
        word1 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'THERE',
            'bottom': 15,
            'chars': [
                {'text': 'T', 'size': 12, 'y1': 15},
                {'text': 'H', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
                {'text': 'R', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
            ]
        }
        word2 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'BE',
            'bottom': 15,
            'chars': [
                {'text': 'B', 'size': 14, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15}
            ]
        }
        assert heading_state_accumulator.add(word1) == True
        assert heading_state_accumulator.add(word2) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word1, word2]

    def test_adding_all_lower_caps_words_on_next_line(self, heading_state_accumulator, initial_word):
        word1 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'FOO',
            'bottom': 15,
            'chars': [
                {'text': 'F', 'size': 12, 'y1': 15},
                {'text': 'O', 'size': 12, 'y1': 15},
                {'text': 'O', 'size': 12, 'y1': 15},
            ]
        }
        word2 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'BAR',
            'bottom': 15,
            'chars': [
                {'text': 'B', 'size': 12, 'y1': 15},
                {'text': 'A', 'size': 12, 'y1': 15},
                {'text': 'R', 'size': 12, 'y1': 15},
            ]
        }
        word3 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'Baz',
            'bottom': 20,
            'chars': [
                {'text': 'B', 'size': 14, 'y1': 20},
                {'text': 'a', 'size': 14, 'y1': 20},
                {'text': 'z', 'size': 14, 'y1': 20},
            ]
        }
        assert heading_state_accumulator.add(word1) == True
        assert heading_state_accumulator.add(word2) == True
        assert heading_state_accumulator.add(word3) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word1, word2]

    def test_adding_all_lower_caps_over_two_lines(self, heading_state_accumulator, initial_word):
        word1 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'FOO',
            'bottom': 15,
            'chars': [
                {'text': 'F', 'size': 12, 'y1': 15},
                {'text': 'O', 'size': 12, 'y1': 15},
                {'text': 'O', 'size': 12, 'y1': 15},
            ]
        }
        word2 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'BAR',
            'bottom': 15,
            'chars': [
                {'text': 'B', 'size': 12, 'y1': 15},
                {'text': 'A', 'size': 12, 'y1': 15},
                {'text': 'R', 'size': 12, 'y1': 15},
            ]
        }
        word3 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'BAZ',
            'bottom': 20,
            'chars': [
                {'text': 'B', 'size': 12, 'y1': 20},
                {'text': 'A', 'size': 12, 'y1': 20},
                {'text': 'Z', 'size': 12, 'y1': 20},
            ]
        }
        assert heading_state_accumulator.add(word1) == True
        assert heading_state_accumulator.add(word2) == True
        assert heading_state_accumulator.add(word3) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word1, word2, word3]

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
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_adding_em_dash(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '—',
            'bottom': 10,
            'chars': [
                {'text': '—', 'size': 14, 'y1': 10}
            ]
        }
        assert heading_state_accumulator.add(word) == False
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word]

    def test_adding_hyphened_heading_word_on_next_line(self, heading_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'FACE-TO-FACE',
            'bottom': 15,
            'chars': [
                {'text': 'F', 'size': 14, 'y1': 15},
                {'text': 'A', 'size': 12, 'y1': 15},
                {'text': 'C', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
                {'text': '-', 'size': 14, 'y1': 15},
                {'text': 'T', 'size': 12, 'y1': 15},
                {'text': 'O', 'size': 12, 'y1': 15},
                {'text': '-', 'size': 14, 'y1': 15},
                {'text': 'F', 'size': 12, 'y1': 15},
                {'text': 'A', 'size': 12, 'y1': 15},
                {'text': 'C', 'size': 12, 'y1': 15},
                {'text': 'E', 'size': 12, 'y1': 15},
            ]
        }
        assert heading_state_accumulator.add(word) == True
        assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert not heading_state_accumulator.is_heading_complete()
        assert heading_state_accumulator.words == [initial_word, word]

    def test_enumeration_to_small_caps_that_continues_on_next_line(self, accumulator):
        font = 'JJGECB+DeVinne'
        words = [
            {
                'fontname': font,
                'text': '(a)',
                'bottom': 10,
                'chars': [
                    {'text': '(', 'size': 14, 'y1': 10},
                    {'text': 'a', 'size': 14, 'y1': 10},
                    {'text': ')', 'size': 14, 'y1': 10},
                ]
            },
            {
                'fontname': font,
                'text': 'STATE',
                'bottom': 10,
                'chars': [
                    {'text': 'S', 'size': 14, 'y1': 10},
                    {'text': 'T', 'size': 12, 'y1': 10},
                    {'text': 'A', 'size': 12, 'y1': 10},
                    {'text': 'T', 'size': 12, 'y1': 10},
                    {'text': 'E', 'size': 12, 'y1': 10},
                ]
            },
            {
                'fontname': font,
                'text': 'PRO-',
                'bottom': 10,
                'chars': [
                    {'text': 'P', 'size': 14, 'y1': 10},
                    {'text': 'R', 'size': 12, 'y1': 10},
                    {'text': 'O', 'size': 12, 'y1': 10},
                    {'text': '–', 'size': 14, 'y1': 10}
                ]
            },
            {
                'fontname': font,
                'text': 'GRAMS.',
                'bottom': 10,
                'chars': [
                    {'text': 'G', 'size': 12, 'y1': 10},
                    {'text': 'R', 'size': 12, 'y1': 10},
                    {'text': 'A', 'size': 12, 'y1': 10},
                    {'text': 'M', 'size': 12, 'y1': 10},
                    {'text': 'S', 'size': 12, 'y1': 10},
                    {'text': '.', 'size': 14, 'y1': 10},
                ]
            },
        ]
        for word in words:
            assert accumulator.add(word) == True
        assert accumulator.status == HeadingAccumulator.Status.HEADING
        assert not accumulator.is_heading_complete()
        assert accumulator.words == words

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

        def test_state(self, heading_state_accumulator, initial_words):
            assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
            assert heading_state_accumulator.casing == Casing.SMALL_CAPS
            assert not heading_state_accumulator.is_heading_complete()
            assert heading_state_accumulator.words == initial_words

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

        def test_adding_all_lower_caps_words_on_same_line(self, heading_state_accumulator, initial_words):
            word = {
                'fontname': 'JJGECB+DeVinne',
                'text': 'BAR',
                'bottom': 10,
                'chars': [
                    {'text': 'B', 'size': 12, 'y1': 10},
                    {'text': 'A', 'size': 12, 'y1': 10},
                    {'text': 'R', 'size': 12, 'y1': 10},
                ]
            }
            assert heading_state_accumulator.add(word) == True
            assert heading_state_accumulator.status == HeadingAccumulator.Status.HEADING
            assert heading_state_accumulator.words == initial_words + [word]

class TestFromAllCapsUndeterminedState:
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

class TestFromNumberParentheticalUndeterminedState:
    @pytest.fixture
    def initial_word(self):
        return {
                'fontname': 'JJGECB+DeVinne',
                'text': '(1)',
                'bottom': 10,
                'chars': [
                    {'text': '(', 'size': 14, 'y1': 10},
                    {'text': '1', 'size': 14, 'y1': 10},
                    {'text': ')', 'size': 14, 'y1': 10}
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
        word_1 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'HI.',
            'bottom': 10,
            'x0': 70.0,
            'x1': 80.0,
            'chars': [
                {'text': 'H', 'size': 14, 'y1': 10},
                {'text': 'I', 'size': 12, 'y1': 10},
                {'text': '.', 'size': 14, 'y1': 10},
            ]
        }
        word_2 = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'Foo',
            'bottom': 10,
            'chars': [
                {'text': 'F', 'size': 14, 'y1': 10},
                {'text': 'o', 'size': 14, 'y1': 10},
                {'text': 'o', 'size': 14, 'y1': 10},
            ]
        }
        assert undetermined_state_accumulator.add(word_1) == True
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert undetermined_state_accumulator.casing == Casing.SMALL_CAPS
        assert not undetermined_state_accumulator.is_heading_complete()
        assert undetermined_state_accumulator.words == [initial_word, word_1]

        assert undetermined_state_accumulator.add(word_2) == False
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert undetermined_state_accumulator.words == [initial_word, word_1]



    def test_small_caps_heading_adding_parethetical_on_next_line(self, undetermined_state_accumulator, initial_word):
        words = [
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 12, 'y1': 10},
                ]
            },
            {
                'fontname': 'JJGECB+DeVinne',
                'text': '(A)',
                'bottom': 20,
                'chars': [
                    {'text': '(', 'size': 14, 'y1': 20},
                    {'text': 'A', 'size': 14, 'y1': 20},
                    {'text': ')', 'size': 14, 'y1': 20},
                ]
            }
        ]
        assert undetermined_state_accumulator.add(words[0]) == True
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING
        assert undetermined_state_accumulator.casing == Casing.SMALL_CAPS

        assert undetermined_state_accumulator.add(words[1]) == False
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert undetermined_state_accumulator.words == [initial_word, words[0]]

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

class TestFromLetterParentheticalUndeterminedState:
    @pytest.fixture
    def initial_word(self):
        return {
                'fontname': 'JJGECB+DeVinne',
                'text': '(a)',
                'bottom': 10,
                'chars': [
                    {'text': '(', 'size': 14, 'y1': 10},
                    {'text': 'a', 'size': 14, 'y1': 10},
                    {'text': ')', 'size': 14, 'y1': 10}
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

class TestFromNumberUndeterminedState:
    @pytest.fixture
    def initial_word(self):
        return {
                'fontname': 'JJGECB+DeVinne',
                'text': '30.',
                'bottom': 10,
                'chars': [
                    {'text': '3', 'size': 14, 'y1': 10},
                    {'text': '0', 'size': 14, 'y1': 10},
                    {'text': '.', 'size': 14, 'y1': 10}
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

    def test_adding_a_heading_word_on_next_line(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'HI',
            'bottom': 15,
            'chars': [
                {'text': 'H', 'size': 14, 'y1': 15},
                {'text': 'I', 'size': 12, 'y1': 15}
            ]
        }
        assert undetermined_state_accumulator.add(word) == False
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert undetermined_state_accumulator.is_not_heading()

    def test_adding_enumeration(self, undetermined_state_accumulator, initial_word):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': '(a)',
            'bottom': 10,
            'chars': [
                {'text': '(', 'size': 14, 'y1': 10},
                {'text': 'a', 'size': 14, 'y1': 10},
                {'text': ')', 'size': 14, 'y1': 10}
            ]
        }
        assert undetermined_state_accumulator.add(word) == False
        assert undetermined_state_accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert undetermined_state_accumulator.is_not_heading()

class TestTierMethod:
    def test_when_no_words(self, accumulator):
        with pytest.raises(HeadingAccumulator.BadStateError):
            accumulator.tier

    def test_when_status_not_heading(self, accumulator):
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
        accumulator.add(word)
        assert accumulator.status == HeadingAccumulator.Status.NOT_HEADING
        assert accumulator.tier == None

    def test_when_status_heading(self, accumulator):
        word = {
            'fontname': 'JJGECG+NewCenturySchlbk-Bold',
            'text': 'HI',
            'bottom': 10,
            'chars': [
                {'text': 'H', 'size': 18, 'y1': 10},
                {'text': 'I', 'size': 18, 'y1': 10}
            ]
        }
        accumulator.add(word)
        assert accumulator.status == HeadingAccumulator.Status.HEADING
        with pytest.raises(HeadingAccumulator.BadStateError):
            accumulator.tier

    def test_when_status_undetermined(self, accumulator):
        word = {
            'fontname': 'JJGECB+DeVinne',
            'text': 'HI',
            'bottom': 10,
            'chars': [
                {'text': 'H', 'size': 14, 'y1': 10},
                {'text': 'I', 'size': 14, 'y1': 10}
            ]
        }
        accumulator.add(word)
        assert accumulator.status == HeadingAccumulator.Status.UNDETERMINED
        with pytest.raises(HeadingAccumulator.BadStateError):
            accumulator.tier

    def test_when_status_heading_complete_tier_1(self, accumulator):
        words = [
            {
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 18, 'y1': 10},
                    {'text': 'I', 'size': 18, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'text': 'YOU',
                'bottom': 10,
                'chars': [
                    {'text': 'Y', 'size': 18, 'y1': 10},
                    {'text': 'O', 'size': 18, 'y1': 10},
                    {'text': 'U', 'size': 18, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 14, 'y1': 10}
                ]
            }
        ]
        for word in words:
            accumulator.add(word)

        assert accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert accumulator.tier == 1

    def test_when_status_heading_complete_tier_2(self, accumulator):
        words = [
            {
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 14, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'text': 'YOU',
                'bottom': 10,
                'chars': [
                    {'text': 'Y', 'size': 14, 'y1': 10},
                    {'text': 'O', 'size': 14, 'y1': 10},
                    {'text': 'U', 'size': 14, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 14, 'y1': 10}
                ]
            }
        ]
        for word in words:
            accumulator.add(word)

        assert accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert accumulator.tier == 2

    def test_when_status_heading_complete_tier_2_with_year(self, accumulator):
        words = [
            {
                'text': 'DIV',
                'bottom': 213.8670000000002,
                'height': 14.0,
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'chars': [
                    {
                        'y1': 600,
                        'size': 14.0,
                        'text': 'D'
                    },
                    {
                        'y1': 600,
                        'size': 14.0,
                        'text': 'I'
                    },
                    {
                        'y1': 600,
                        'size': 14.0,
                        'text': 'V'
                    }
                ]
            },
            {
                'text': 'FOO',
                'bottom': 213.8670000000002,
                'height': 14.0,
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'chars': [
                    {
                        'y1': 592.1329999999998,
                        'size': 14.0,
                        'text': 'F'
                    },
                    {
                        'y1': 592.1329999999998,
                        'size': 14.0,
                        'text': 'O'
                    },
                    {
                        'y1': 592.1329999999998,
                        'size': 14.0,
                        'text': 'O'
                    }
                ]
            },
            {
                'text': '2025',
                'bottom': 213.8670000000002,
                'height': 14.0,
                'fontname': 'JJGECG+NewCenturySchlbk-Bold',
                'chars': [
                    {
                        'y1': 592.1329999999998,
                        'size': 14.0,
                        'text': '2'
                    },
                    {
                        'y1': 592.1329999999998,
                        'size': 14.0,
                        'text': '0'
                    },
                    {
                        'y1': 592.1329999999998,
                        'size': 14.0,
                        'text': '2'
                    },
                    {
                        'y1': 592.1329999999998,
                        'size': 14.0,
                        'text': '5'
                    }
                ]
            },
            {
                'text': 'end',
                'bottom': 213.8670000000002,
                'height': 14.0,
                'fontname': 'JJGECG+NewCenturySchlbk',
                'chars': [
                    {
                        'y1': 600,
                        'size': 14.0,
                        'text': 'e'
                    },
                    {
                        'y1': 600,
                        'size': 14.0,
                        'text': 'n'
                    },
                    {
                        'y1': 600,
                        'size': 14.0,
                        'text': 'd'
                    }
                ]
            }
        ]

        for word in words:
            accumulator.add(word)

        assert accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert accumulator.tier == 2

    def test_when_status_heading_complete_tier_4(self, accumulator):
        words = [
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 14, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'YOU',
                'bottom': 10,
                'chars': [
                    {'text': 'Y', 'size': 14, 'y1': 10},
                    {'text': 'O', 'size': 14, 'y1': 10},
                    {'text': 'U', 'size': 14, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 15,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 15},
                    {'text': 'i', 'size': 14, 'y1': 15}
                ]
            }
        ]
        for word in words:
            accumulator.add(word)

        assert accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert accumulator.tier == 4

    def test_when_status_heading_complete_tier_5(self, accumulator):
        words = [
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 12, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'YOU',
                'bottom': 10,
                'chars': [
                    {'text': 'Y', 'size': 14, 'y1': 10},
                    {'text': 'O', 'size': 12, 'y1': 10},
                    {'text': 'U', 'size': 12, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 15,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 15},
                    {'text': 'i', 'size': 14, 'y1': 15}
                ]
            }
        ]
        for word in words:
            accumulator.add(word)

        assert accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert accumulator.tier == 5

    def test_when_status_heading_complete_tier_5_with_mixed_casing(self, accumulator):
        words = [
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 10,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 10},
                    {'text': 'I', 'size': 14, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'YOU',
                'bottom': 10,
                'chars': [
                    {'text': 'Y', 'size': 14, 'y1': 10},
                    {'text': 'O', 'size': 12, 'y1': 10},
                    {'text': 'U', 'size': 12, 'y1': 10}
                ]
            },
            {
                'fontname': 'JJGECB+DeVinne',
                'text': 'HI',
                'bottom': 15,
                'chars': [
                    {'text': 'H', 'size': 14, 'y1': 15},
                    {'text': 'i', 'size': 14, 'y1': 15}
                ]
            }
        ]
        for word in words:
            accumulator.add(word)

        assert accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert accumulator.tier == 5

    def test_division_subheading_2(self, accumulator):
        words =  [
            {
                'text': 'PROCESSING,',
                'bottom': 351.8978,
                'fontname': 'JJGECB+DeVinne',
                'chars': [
                    {'text': 'P', 'size': 14.0, 'y1': 454.1068999999998},
                    {'text': 'R', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'O', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'C', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'E', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'S', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'S', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'I', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'N', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'G', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': ',', 'size': 14.0, 'y1': 454.1022}
                ]
            }, {
                'text': 'RESEARCH,',
                'bottom': 351.8978,
                'fontname': 'JJGECB+DeVinne',
                'chars': [
                    {'text': 'R', 'size': 14.0, 'y1': 454.1022},
                    {'text': 'E', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'S', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'E', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'A', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'R', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'C', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'H', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': ',', 'size': 14.0, 'y1': 454.1022}
                ]
            }, {
                'text': 'AND',
                'bottom': 351.182408,
                'fontname': 'JJGECB+DeVinne',
                'chars': [
                    {'text': 'A', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'N', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'D', 'size': 10.54400000000004, 'y1': 451.36159200000003}
                ]
            }, {
                'text': 'MARKETING',
                'bottom': 351.8978,
                'fontname': 'JJGECB+DeVinne',
                'chars': [
                    {'text': 'M', 'size': 14.0, 'y1': 454.1022},
                    {'text': 'A', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'R', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'K', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'E', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'T', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'I', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'N', 'size': 10.54400000000004, 'y1': 451.36159200000003},
                    {'text': 'G', 'size': 10.54400000000004, 'y1': 451.36159200000003}
                ]
            }, {
                'text': 'OFFICE',
                'bottom': 377.18250800000004,
                'fontname': 'JJGECB+DeVinne',
                'chars': [
                    {'text': 'O', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'F', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'F', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'I', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'C', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'E', 'size': 10.54400000000004, 'y1': 425.361492}
                ]
            }, {
                'text': 'OF',
                'bottom': 377.18250800000004,
                'fontname': 'JJGECB+DeVinne',
                'chars': [
                    {'text': 'O', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'F', 'size': 10.54400000000004, 'y1': 425.361492}
                ]
            }, {
                'text': 'THE',
                'bottom': 377.18250800000004,
                'fontname': 'JJGECB+DeVinne',
                'chars': [
                    {'text': 'T', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'H', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'E', 'size': 10.54400000000004, 'y1': 425.361492}
                ]
            }, {
                'text': 'SECRETARY',
                'bottom': 377.18250800000004,
                'fontname': 'JJGECB+DeVinne',
                'chars': [
                    {'text': 'S', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'E', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'C', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'R', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'E', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'T', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'A', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'R', 'size': 10.54400000000004, 'y1': 425.361492},
                    {'text': 'Y', 'size': 10.54400000000004, 'y1': 425.361492}
                ]
            }, {
                'text': 'For',
                'bottom': 393.18250800000004,
                'fontname': 'JJGECB+DeVinne',
                'chars': [
                    {'text': 'F', 'size': 14, 'y1': 425.361492},
                    {'text': 'o', 'size': 14, 'y1': 425.361492},
                    {'text': 'r', 'size': 14, 'y1': 425.361492}
                ]
            }
        ]

        for word in words:
            accumulator.add(word)

        assert accumulator.status == HeadingAccumulator.Status.HEADING_COMPLETE
        assert accumulator.tier == 5
