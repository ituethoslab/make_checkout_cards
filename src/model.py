"""
Generate checkout cards for ETHOS Lab library.

Uses a Word file as a template.
"""

import logging
import requests
import json
from time import sleep
from configparser import ConfigParser
import pandas as pd
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


class GoogleBooks():
    """A Google Books API representation."""
    ENDPOINT = 'https://www.googleapis.com/books/v1/volumes'
    FIELDS = 'items/volumeInfo(authors,title,subtitle,publishedDate)'

    def __init__(self, configfile):
        self._config = ConfigParser()
        self._config.read(configfile)
        logging.debug("Made %s", self.__dir__)

    def getByIsbn(self, isbn, throttle=2):
        logging.debug("Querying %s", isbn)
        creds = {'key': self._config['google']['key']}
        query = {'q': 'isbn:' + isbn, 'fields': self.FIELDS}
        params = {**creds, **query}

        logging.debug("Throttling for %s seconds", throttle)
        sleep(throttle)

        logging.debug("Would query %s with %s", self.ENDPOINT, params)
        resp = requests.get(self.ENDPOINT, params=params)
        logging.debug(resp)
        if resp.ok:
            logging.debug("Retrieved %s", resp.json())
            return resp.json()


class Catalogue():
    """A catalogue for ETHOS Lab."""

    JSONFILE = 'ethos-lib.catalogue.json'

    def __init__(self, datafile, resolver):
        logging.debug("Reading catalogue from %s", datafile)
        self._resolver=resolver
        self._barcodes=pd.read_csv(datafile,
                                   dtype={'Barcode': str})
        self.items = {}
        self.populate()

    def populate(self, load=True, persist=True):
        if load:
            with open(self.JSONFILE) as fd:
                self.items = json.load(fd)

        for barcode in self._barcodes['Barcode']:
            if barcode not in self.items:
                work = self._resolver.getByIsbn(barcode)
                volume = work['items'][0]['volumeInfo']
                self.items[barcode] = volume
        # self.items = [PublicationWork(self._resolver.getByIsbn(isbn)) for isbn in self._barcodes['Barcode']]]
        if persist:
            self.persist()

    def persist(self):
        """Persist to a file."""
        logging.debug("Persisting %s items", len(self.items))
        with open(self.JSONFILE, 'w') as fd:
            serialized_items = json.dumps(self.items, indent=2)
            fd.write(serialized_items)


class PublicationWork():
    def __init__(self, author, title, subtitle, year):
        """Construct the object."""
        self.author = author
        self.title = title
        self.subtitle = subtitle
        self.year = year

    def __str__(self):
        """Return as string."""
        return f"{self.author}: {self.title} ({self.year})"
