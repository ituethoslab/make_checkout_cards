from src.model import CheckoutCardTwoCols, GoogleBooks, Catalogue

if __name__ == "__main__":
    google_books = GoogleBooks('config.ini')
    catalogue = Catalogue('data/ETHOS Lab library.csv', google_books)

    for i in range(0, len(catalogue.items), 2):
    # for i in range(2, 4, 2):
        as_list = list(catalogue.items)
        left = catalogue.items[as_list[i]]
        right = catalogue.items[as_list[i+1]]

        # print()
        # print(left)
        # print(right)

        two_cards = CheckoutCardTwoCols(left, right)
        two_cards._populate()
        # two_cards.save('output/two_cards-next-from-data.docx')
        two_cards.save(f'output/two-cards-{i}_and_{i+1}.docx')
        print(repr(two_cards))
