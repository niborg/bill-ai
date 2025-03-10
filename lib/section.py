import tiktoken
import pdb

class Section:
  def __init__(self, heading, tier=1, content=None, subsections=None):
    if heading is None or heading == "":
        raise ValueError("heading cannot be None")

    self.heading = heading
    self.tier = tier
    self.content = content
    self.subsections = subsections if subsections is not None else []

  def add_subsection(self, section):
    if section.tier <= self.tier:
      return None
    else:
      if len(self.subsections) == 0 or not self.subsections[-1].add_subsection(section):
        self.subsections.append(section)
        return self
      return self.subsections[-1]

  def last_subsection(self):
    if len(self.subsections) == 0:
      return self
    else:
      return self.subsections[-1].last_subsection()

  def token_count(self, model="gpt-4o"):
    encoder = tiktoken.encoding_for_model(model)
    return len(encoder.encode(self.text()))

  def text(self):
    content = "" if self.content is None else self.content
    section_result = f"<h{self.tier}>{self.heading}<h{self.tier}>\n\n" + content + "\n\n"
    subsections_result = "".join([s.text() for s in self.subsections])
    return section_result + subsections_result

  def print_headings(self):
    print(f"{'#' * self.tier} {self.heading.text()}")
    for subsection in self.subsections:
      subsection.print_headings()
