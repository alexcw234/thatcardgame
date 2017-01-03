#!/usr/bin/env python3

"""
# Standard Card Class
#
"""
class Card:


    # The card's name.
    cardName = "nonam"

    # The card's numeric value.
    cardValue = 0

    # The card's type.
    cardType = "nothing"

    # The card's suit
    cardSuit = "none"

    # The card's color
    cardColor = "none"

    # The card's full description
    cardFull = "nonam of none (none)"

    """
    # Initializes a new card.
    #
    """
    def __init__(self, ctype, rank, suit, color):
        self.cardName = rank['name']
        self.cardValue = rank['value']
        self.cardType = ctype
        self.cardSuit = suit
        self.cardColor = color
        self.cardFull = "%s of %s (%s) (%d)" % (self.cardName, self.cardSuit, self.cardColor, self.cardValue)


    """
    # Returns the card's full description
    #
    """
    def getFullDesc(self):
        return self.cardFull

    """
    # Returns the card's name.
    #
    """
    def getCardName(self):
        return self.cardName

    """
    # Returns the card's suit.
    #
    """
    def getCardSuit(self):
        return self.cardSuit

    """
    # Returns the card's value.
    #
    """
    def getCardValue(self):
        return self.cardValue

    """
    # Returns the card's color.
    #
    """
    def getCardColor(self):
        return self.cardColor
