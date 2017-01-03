#!/usr/bin/env python3
from random import shuffle
from .card import Card

"""
# Standard Deck Class
#
"""
class Deck:

    # Number of cards in deck
    deckbaseSize = 0

    # The deck
    deck = []

    # The Rank dict
    ranks = {}

    # The Suit dict
    suits = {}

    # The Color dict
    colors = {}

    """ Initialization Functions """


    """
    # Initializes a new deck.
    # Parameters:
    #   size | number of cards in base deck (before specials)
    #
    """
    def __init__(self, size, Ranks, Suits, Colors):
        self.deck = []
        self.deckbaseSize = size
        self.ranks = Ranks
        self.suits = Suits
        self.colors = Colors


    """
    # Generates the base deck of 52? cards
    """
    def makeBase(self):
        self._makeBaseSet('numeric')
        self._makeBaseSet('face')

    """
    # Generates set of numeric or face cards called by makeBase
    """
    def _makeBaseSet(self, theSet):
        if (theSet != 'numeric' and theSet != 'face'):
            print ("Improper set specified")
            return False

        for entry in self.ranks[theSet]:
            cRank = entry
            for suitentry in self.suits['suits']:
                cSuit = suitentry['name']
                for colorentry in self.colors['colors']:
                    if (suitentry['notColor'] != colorentry['name']):
                        cColor = colorentry['name']
                        self._addBaseCard(theSet, cRank, cSuit, cColor)

    """
    # Adds NEW base card to top of deck, called by makeBaseSet
    """
    def _addBaseCard(self, btype, brank, bsuit, bcolor):
        theBaseCard = self._createCard(btype, brank, bsuit, bcolor)
        self.deck.append(theBaseCard)

    """
    # Adds NEW special card to top of deck
    """
    def addSpecialCard(self):
        print ("unimplemented")

    """
    # Creates a card.
    # Parameters:
    #   ctype | card type
    #   rank  | card rank
    #   suit  | card suit
    #   color | card color
    #
    # Returns the card
    """
    def _createCard(self, ctype, rank, suit, color):
        newCard = Card(ctype, rank, suit, color)
        return newCard

    """ Checker functions """

    """
    # Checks if empty deck
    """
    def isEmpty(self):
        if (len(self.deck)) <= 0:
            return True
        else:
            return False


    """ Deck operation Functions """

    """
    # Prints the entire deck
    """
    def printDeck(self):
        print ("[")
        for card in self.deck:
            print (card.getFullDesc())
        print ("]")



    """
    # Shuffles the deck
    """
    def shuffle(self):
        shuffle(self.deck)


    """
    # Returns (but not removes) top card from deck.
    """
    def peek(self):
        if (not self.isEmpty()):
            return self.deck[len(self.deck) - 1]
        else:
            return False

    """
    # Returns (and removes) top card from deck
    """
    def pop(self):
        if (not self.isEmpty()):
            return self.deck.pop()
        else:
            return False

    """
    # Adds card to top of deck
    """
    def cardToTop(self, cardToAdd):
        self.deck.append(cardToAdd)

    """
    # Adds card to bottom of deck
    """
    def cardToBottom(self, cardToAdd):
        self.deck.reverse()
        self.deck.append(cardToAdd)
        self.deck.reverse()



#
