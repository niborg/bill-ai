from .content_type import ContentType
from .content_group import ContentCharacteristics
from .casing import Casing

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
    ContentType.DIVISION_HEADING_1: ContentCharacteristics("JJGECG+NewCenturySchlbk-Bold", 18.0, casing=Casing.ALL_CAPS),
    ContentType.DIVISION_HEADING_2: ContentCharacteristics("JJGECG+NewCenturySchlbk-Bold", 14.0, casing=Casing.ALL_CAPS),
    ContentType.DIVISION_SUBHEADING_1: ContentCharacteristics("JJGECB+DeVinne", 14.0, casing=Casing.ALL_CAPS),
    ContentType.DIVISION_SUBHEADING_2: ContentCharacteristics("JJGECB+DeVinne", 14.0, casing=Casing.SMALL_CAPS),
    ContentType.DIVISION_SUBHEADING_3: ContentCharacteristics("JJGECB+DeVinne", 10.5, casing=Casing.ALL_CAPS),
    ContentType.LAW_SECTION: ContentCharacteristics("JJGECG+NewCenturySchlbk-Bold", 10.0, casing=Casing.ALL_CAPS)
}
HEADINGS = [
    ContentType.DIVISION_HEADING_1,
    ContentType.DIVISION_HEADING_2,
    ContentType.DIVISION_SUBHEADING_2,
    ContentType.DIVISION_SUBHEADING_3,
    ContentType.LAW_SECTION
]
POSSIBLE_HEADINGS = [
    ContentType.DIVISION_SUBHEADING_1
]
HEADING_HIERARCHY = [
    ContentType.DIVISION_HEADING_1,
    ContentType.DIVISION_HEADING_2,
    ContentType.LAW_SECTION,
    ContentType.DIVISION_SUBHEADING_1,
    ContentType.DIVISION_SUBHEADING_2,
    ContentType.DIVISION_SUBHEADING_3
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
