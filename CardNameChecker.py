from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog

class CardNameChecker:
    def __init__(self):
        self

    def find_cards_by_name_set(self, inputCardName, inputSetName):
        cardNameQuery = Card.where(name=inputCardName).where(set=inputSetName)
        cards = cardNameQuery.all()

        if len(cards) <= 0:
            raise Exception("No cards found, review input parameters")
        else:
            return cards
