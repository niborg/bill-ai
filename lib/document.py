from lib import HeadingAccumulator, Section
import pdb

class Document:
    LINE_SKIP_TOLERANCE = 2

    def __init__(self):
        self.pages = []
        self.sections = []
        self.current_content = ''
        self._line_skip = None
        self.current_heading = None
        self.current_content = []
        self.headings = []

    def add_page(self, page):
        self._line_skip = None
        self.current_page = page
        all_words = page.extract_words(extra_attrs=['fontname'], return_chars=True, split_at_punctuation="—")

        for word in all_words:
            self.add_token(word)

        self.pages.append(page)
        return True

    def add_token(self, token):
        if self._line_skip:
            if abs(token['bottom'] - self._line_skip) < Document.LINE_SKIP_TOLERANCE:
                self.current_content.append(token)
                return False
            else:
                self._line_skip = None

        if self.current_heading is None:
            self.current_heading = HeadingAccumulator(width=self.current_page.width)

        if self.current_heading.add(token):
            return True

        if self.current_heading.is_heading_complete():
            self.headings.append(self.current_heading)
            tier = self.current_heading.tier
            if len(self.sections) == 0:
                self.sections.append(
                    Section(self.current_heading, tier=tier)
                )
            else:
                last_subsection = self.sections[-1].last_subsection()
                last_subsection.content = self.current_content
                self.current_content = []
                if tier is not None:
                    new_section = Section(self.current_heading, tier=tier)
                    if not self.sections[-1].add_subsection(new_section):
                        self.sections.append(new_section)
                else:
                    # Not clear that this path is ever taken.
                    last_subsection.content.append(self.current_heading.words)

            self.current_heading = None

            for word in self.headings[-1].accumulated_subheading_words():
                self.add_token(word) # Retry any subheading words that were accumulated.
            return self.add_token(token) # Retry current word with new heading accumulator

        if self.current_heading.is_not_heading():
            if len(self.current_heading.words) > 0:
                self._line_skip = self.current_heading.words[-1]['bottom']
                self.current_content.append(self.current_heading.words)
                self.current_heading = None
                return self.add_token(token)
            self.current_heading = None
            self._line_skip = token['bottom']
            return False

        return False # Token was something that should be ignored

    def print_headings(self):
        for section in self.sections:
            section.print_headings()
