#!/usr/bin/env python3

from random import shuffle
from .card import Card
from .selection import Selection

"""
# Standard Hand Class
#
"""
class Hand:


    # The hand
    hand = []

    # The player number
    playerNo = -1

    # The selection
    # Mirrors selection in the selection class
    selection = []

    # The selection class
    selectionClass = ""

    """ Initialization Functions """


    """
    # Initializes a new Hand.
    # Parameters:
    #
    #
    """
    def __init__(self, playernumber):
        self.selection = []
        self.selectionClass = None
        self.hand = []
        self.playerNo = playernumber
        self.selectionClass = Selection()

    """
    # Adds card to hand
    """
    def addCard(self, card):
        self.hand.append(card)


    """
    # Prints entire hand
    """
    def printHand(self):
        print ("[")
        for card in self.hand:
            print (card.getFullDesc())
        print ("]")

    """
    # Checks if hand is empty
    """
    def isEmpty(self):
        if (len(self.hand) <= 0):
            return True
        else:
            return False

    """
    # Returns hand length
    """
    def getLength(self):
        return len(self.hand)

    """
    # Returns card by index
    """
    def getCardByIndex(self, cardIndex):
        return self.hand[cardIndex]


    """
    # Sorts the hand
    """
    def sortHand(self):
        self.sortBySuit()
        self.sortByRank()

    """
    # Sorts the hand by suit
    """
    def sortBySuit(self):
        tempHand = []

        tempHand.append(self.hand.pop())

        while (self.isEmpty() != True):
            tempCard = self.hand.pop()
            tempCardVal = tempCard.getCardSuit()

            for anchorIn in range(len(tempHand)):
                anchorCard = tempHand[anchorIn]
                anchorCardVal = anchorCard.getCardSuit()

                if (tempCardVal < anchorCardVal):

                    tempHand.insert(anchorIn, tempCard)
                    break
                elif (tempCardVal > anchorCardVal and anchorIn >= len(tempHand) - 1):

                    tempHand.append(tempCard)
                    break
                elif (tempCardVal == anchorCardVal):

                    tempHand.insert(anchorIn, tempCard)
                    break
        self.hand = tempHand

    """
    # Sorts the hand by rank
    """
    def sortByRank(self):
        tempHand = []

        tempHand.append(self.hand.pop())

        while (self.isEmpty() != True):
            tempCard = self.hand.pop()
            tempCardVal = tempCard.getCardValue()

            for anchorIn in range(len(tempHand)):
                anchorCard = tempHand[anchorIn]
                anchorCardVal = anchorCard.getCardValue()

                if (tempCardVal < anchorCardVal):

                    tempHand.insert(anchorIn, tempCard)
                    break
                elif (tempCardVal > anchorCardVal and anchorIn >= len(tempHand) - 1):

                    tempHand.append(tempCard)
                    break
                elif (tempCardVal == anchorCardVal):

                    tempHand.insert(anchorIn, tempCard)
                    break
        self.hand = tempHand

    """
    # Toggles the selection of card
    #
    """
    def toggleSelect(self, theCard):
        if theCard not in self.selection:
            self.select(theCard)
        elif theCard in self.selection:
            self.deselect(theCard)


    """
    # Select a card
    #
    """
    def select(self, theCard):
        if theCard not in self.selection:
            selectedCard = self.selectionClass.select(theCard)
            self.selection.append(selectedCard)

    """
    # Deselect a card
    #
    """
    def deselect(self, theCard):
        if theCard in self.selection:
            deselectedCard = self.selectionClass.deselect(theCard)
            self.selection.remove(theCard)


    """
    # Finalize Selection
    #
    """
    def finalizeSelection(self):
        if (self.selectionClass.isEmpty() == True):
            return False

        validation = self.selectionClass.validate()

        if (validation['returnTrue'] == True):
            self.selection = validation['theSelection']
            return validation
        else:
            return False


    """
    # Clear Selection
    #
    """
    def clearSelection(self):
        self.selection = []
        self.selectionClass.clearSelection()

    """
    # Returns the Selection
    #
    """
    def getSelection(self):
        return self.selection

    """
    # Remove selection from hand
    #
    """
    def selectionPlayed(self):
        for card in self.selection:
            self.hand.remove(card)
        self.clearSelection()



#
