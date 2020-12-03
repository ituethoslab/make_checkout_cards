from src.model import GoogleBooks, Catalogue
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    google_resolver = GoogleBooks('config.ini')
    catalogue = Catalogue('data/ETHOS Lab Library.csv', google_resolve
