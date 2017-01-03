#!/usr/bin/env python3



"""
# Class of Selection
# For call by selection class
"""
class Selection:

    # The selection list
    # Meant to mirror the list in the selection class
    selection = []

    """
    # Initialize Selection
    #
    """
    def __init__(self):
        self.selection = []



    """
    # Adds card to selection, then returns the card
    """
    def select(self, theCard):
        self.selection.append(theCard)
        return theCard



    """
    # Removes card from selection, then returns the card
    """
    def deselect(self, theCard):
        self.selection.remove(theCard)
        return theCard

    """
    # Clears selection
    #
    """
    def clearSelection(self):
        self.selection = []

    """
    # Sorts the selection by rank
    """
    def sortByRank(self):
        tempselection = []

        tempselection.append(self.selection.pop())

        while (self.isEmpty() != True):
            tempCard = self.selection.pop()
            tempCardVal = tempCard.getCardValue()

            for anchorIn in range(len(tempselection)):
                anchorCard = tempselection[anchorIn]
                anchorCardVal = anchorCard.getCardValue()

                if (tempCardVal < anchorCardVal):

                    tempselection.insert(anchorIn, tempCard)
                    break
                elif (tempCardVal > anchorCardVal and anchorIn >= len(tempselection) - 1):

                    tempselection.append(tempCard)
                    break
                elif (tempCardVal == anchorCardVal):

                    tempselection.insert(anchorIn, tempCard)
                    break
        self.selection = tempselection




    """
    #
    # Validates Selection
    #
    """
    def validate(self):
        gType = 0
        gPower = 0
        self.sortByRank()
        if (self.isSingle()):
            gType = len(self.selection)
            gPower = self.selection[0].getCardValue()
            gLength = len(self.selection)
        elif (self.isMatch(2)):
            gType = len(self.selection)
            gPower = self.selection[0].getCardValue()
            gLength = len(self.selection)
        elif (self.isBomb(2 + 1)):
            gType = "Bomb"
            gPower = self.selection[0].getCardValue()
            gLength = len(self.selection)
        elif (self.isStraight(4)):
            gType = "Straight"
            gPower = self.selection[0].getCardValue()
            gLength = len(self.selection)
        else:
            return {'returnTrue' : False, 'groupType' : None, 'groupLength': None, 'groupPower' : None, 'theSelection' : None}

        return {'returnTrue' : True, 'groupType' : gType, 'groupLength': gLength, 'groupPower': gPower, 'theSelection' : self.selection}


    """
    #
    # Is single card
    #
    """
    def isSingle(self):
        if (len(self.selection) == 1):
            return True
        else:
            return False

    """
    #
    # Is Match
    #
    """
    def isMatch(self, maxMatchBeforeisBomb):
        firstCard = self.selection[0]
        firstCardVal = firstCard.getCardValue()
        if (len(self.selection) > maxMatchBeforeisBomb):
            return False

        for card in self.selection:
            tempCardVal = card.getCardValue()
            if (firstCardVal != tempCardVal):
                return False
        return True

    """
    #
    # Is bomb (let's say these are 3 or more for now)
    #
    """
    def isBomb(self, minBeforeisNotBomb):
        firstCard = self.selection[0]
        firstCardVal = firstCard.getCardValue()
        if (len(self.selection) < minBeforeisNotBomb):
            return False
        for card in self.selection:
            tempCardVal = card.getCardValue()
            if (firstCardVal != tempCardVal):
                return False
        return True


    """
    #
    # Is straight (let's require a length of 4 for now)
    #
    """
    def isStraight(self, minStraightRequired):
        firstCard = self.selection[0]
        firstCardVal = firstCard.getCardValue()
        if (len(self.selection) < minStraightRequired):
            return False

        for cardInd in range(len(self.selection) - 1):

            tempCardVal = self.selection[cardInd + 1].getCardValue()
            if (firstCardVal + 1 != tempCardVal):
                return False

            firstCardVal = tempCardVal


        return True

    """
    # Checks if selection is empty
    """
    def isEmpty(self):
        if (len(self.selection) <= 0):
            return True
        else:
            return False
