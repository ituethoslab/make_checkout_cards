"""
Generate checkout cards for ETHOS Lab library.

Uses a Word file as a template.
"""

import logging
from docx import Document

logger = logging.getLogger()

DEBUG = True

if DEBUG:
    logger.setLevel(logging.DEBUG)
 

class CheckoutCard():
    """A checkout card."""

    FILE = 'templates/ethos library checkout card.docx'
    OUTPUTDIR = 'output'

    def __init__(self, author, title, year):
        """Construct the object.

        Parameters:
        author (str): Lastname, Firstname
        title (str):  Book title
        year (int):   Publication year
        """
        self._doc = Document(self.FILE)
        self._author_form = self._doc.paragraphs[0]
        self._title_form = self._doc.paragraphs[1]
        self._year_form = self._doc.paragraphs[2]

        self.author = author
        self.title = title
        self.year = year

        self._generate_id()
        self._populate()

        logging.debug(repr(self))

    def _generate_id(self):
        id_a = self.author.lower().replace(' ', '_')
        id_t = self.title.lower().replace(' ', '_')
        id_y = self.year
        self._id = f"{id_a}-{id_t}-{id_y}"

    def _populate(self):
        """Populate the form."""
        self._author_form.text = self.author
        self._title_form.text = self.title
        self._year_form.text = str(self.year)

    def __str__(self):
        """Return as string.."""
        return f"{self.author}: {self.title} ({self.year})"

    def __repr__(self):
        """Return as representation."""
        cls = self.__class__
        author = self.author
        title = self.title
        year = self.year
        # return f"{self.__class__}: {self.author}; {self.title}; {self.year}"
        return f'{cls}(author="{author}",title="{title}",year={year})'

    def save(self, filename=None):
        """Save the document to a file.

        Parameters:
        filename (str): file name
        """
        if not filename:
            filename = f"{self.OUTPUTDIR}/{self._id}.docx"

        logging.debug("Writing %s", filename)
        self._doc.save(filename)
