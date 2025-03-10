import pytest
import pdb
from lib import Section

@pytest.fixture
def section():
    return Section("Heading", tier=1, content="Content")

class TestSection:
    def test_init(self, section):
        assert section.heading == "Heading"
        assert section.tier == 1
        assert section.content == "Content"
        assert section.subsections == []

    def test_init_with_no_heading(self):
        with pytest.raises(ValueError):
            Section(None, tier=1, content="Content")

    def test_init_with_blank_heading(self):
        with pytest.raises(ValueError):
            Section("", tier=1, content="Content")

    def test_token_count(self, section):
        assert section.token_count() == 9

    def test_text(self, section):
        assert section.text() == "<h1>Heading<h1>\n\nContent\n\n"

    def test_text_with_subsections(self, section):
        section.subsections = [
            Section("Sub Heading", tier=2, content="Sub Content")
        ]
        assert section.text() == "<h1>Heading<h1>\n\nContent\n\n<h2>Sub Heading<h2>\n\nSub Content\n\n"

    def test_text_with_multiple_subsections(self, section):
        section.subsections = [
            Section("Sub Heading 1", tier=2, content="Sub Content 1"),
            Section("Sub Heading 2", tier=2, content="Sub Content 2")
        ]
        assert section.text() == "<h1>Heading<h1>\n\nContent\n\n<h2>Sub Heading 1<h2>\n\nSub Content 1\n\n<h2>Sub Heading 2<h2>\n\nSub Content 2\n\n"

    def test_text_with_nested_subsections(self, section):
        section.subsections = [
            Section("Sub Heading 1", tier=2, content="Sub Content 1"),
            Section(
                "Sub Heading 2",
                tier=2,
                content="Sub Content 2",
                subsections=[
                  Section("Sub Sub Heading", tier=3, content="Sub Sub Content")
                ]
            )
        ]
        assert section.text() == "<h1>Heading<h1>\n\nContent\n\n<h2>Sub Heading 1<h2>\n\nSub Content 1\n\n<h2>Sub Heading 2<h2>\n\nSub Content 2\n\n<h3>Sub Sub Heading<h3>\n\nSub Sub Content\n\n"

    def test_add_subsection(self, section):
        new_section = Section("Sub Heading", tier=2, content="Sub Content")
        section.add_subsection(new_section)
        assert section.subsections[0] == new_section
        assert section.subsections[0].heading == new_section.heading
        assert section.subsections[0].tier == new_section.tier
        assert section.subsections[0].content == new_section.content
        assert section.subsections[0].subsections == []
