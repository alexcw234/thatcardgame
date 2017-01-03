#!/usr/bin/env python3

from .deck import Deck
from .card import Card
from .hand import Hand
import json


"""
# Contains That Card Game
#
"""
class Game:

    # Number of players total
    numPlayers = 0

    # Default base deck size
    deckbaseSize = 0

    # The Rank dict
    ranks = {}

    # The Suit dict
    suits = {}

    # The Color dict
    colors = {}

    # The Game state
    # 0 = initialized
    # 1 = setup complete
    # 2 = game ended
    state = 0

    # List of player decks
    playerDecks = []

    # List of player hands
    playerHands = []

    # The field
    field = []

    # Bomb cycle flag
    bombCycle = False


    """
    # Initializes a new game.
    # Parameters:
    #   players | total number of players
    #
    """
    def __init__(self, players, baseSize):
        self.numPlayers = players
        self.deckbaseSize = baseSize
        print ("Initialized")


    """
    # Sets up new game,
    # called externally.
    #
    """
    def setup(self):
        res = self.loadCRS()
        playerDecks = self.playerDecks

        if (res == True):

            aNewDeck = self.newDeck()
            aNewDeck.shuffle()
            aNewDeck.shuffle()

            for pl in range(self.numPlayers):
                self.playerHands.append(Hand(pl))

            while (aNewDeck.isEmpty() == False):
                for pl in range(self.numPlayers):
                    if (aNewDeck.isEmpty() == False):
                        self.playerHands[pl].addCard(aNewDeck.pop())

            for pl in range(self.numPlayers):
                self.playerHands[pl].sortHand()
                self.playerHands[pl].printHand()



        else:
            return False

    """
    # Loads card information from json files.
    #
    #
    """
    def loadCRS(self):
        try:
            with open('Classes/cardRanks.json') as ranksData:
                try:
                    typ = json.load(ranksData)
                except ValueError as exc:
                    print (exc)
                    return False
            self.ranks = typ

            with open('Classes/cardSuits.json') as suitsData:
                try:
                    typ = json.load(suitsData)
                except ValueError as exc:
                    print (exc)
                    return False
            self.suits = typ

            with open('Classes/cardColors.json') as colorsData:
                try:
                    typ = json.load(colorsData)
                except ValueError as exc:
                    print (exc)
                    return False
            self.colors = typ

        except (IOError, OSError) as exc:
            print (exc)
            return False

        return True

    """
    # Creates a deck.
    #
    # Returns the new deck.
    """
    def newDeck(self):

        theDeck = Deck(self.deckbaseSize, self.ranks, self.suits, self.colors)

        theDeck.makeBase()

        return theDeck


    """
    # Controls flow of the round
    """
    def roundMain(self):
        currentplayer = 0
        passcount = 0
        self.bombCycle = False
        while (True):

            playinghand = self.playerHands[currentplayer]
            print ("Current player:")
            print (currentplayer)

            if (len(self.field) > 0):
                print ("Current field:")

                for card in self.field[len(self.field) - 1]:
                    print (card.getFullDesc())

            print ("Current Hand:")

            playinghand.printHand()
            validplay = False

            while (validplay == False):
                selecting = True
                finalSelection = {}
                while (selecting == True):
                    # Selection phase
                    print ("Selection:")
                    for card in playinghand.getSelection():
                        print (card.getFullDesc())

                    userinputstr = input()
                    userinput = userinputstr

                    if (userinput == ''):
                        finalSelection = playinghand.finalizeSelection()

                        if (finalSelection != False):
                            selecting = False
                        else:
                            print ("Invalid selection, try again")
                            playinghand.clearSelection()

                    elif (userinputstr == "pass"):
                        break

                    else:
                        intOfInput = 0
                        wasAnInt = False
                        try:
                            intOfInput = int(userinput)
                        except ValueError:
                            pass
                        else:
                            wasAnInt = True

                        if (wasAnInt == True):
                            if (int(userinput) >= 0 and int(userinput) < playinghand.getLength()):
                                cardToSel = playinghand.getCardByIndex(int(userinput))
                                playinghand.toggleSelect(cardToSel)
                            else:
                                print ("Invalid input, try again")
                        else:
                            print ("Invalid input, try again")

                if (selecting == True):
                    passcount = passcount + 1
                    playinghand.clearSelection()
                    break

                if (self.isValidPlay(finalSelection)):
                    validplay = True
                    self.playgroup(playinghand.getSelection())
                    playinghand.selectionPlayed()
                else:
                    print ("Can't play that, try again!")
                    playinghand.clearSelection()

            currentplayer = currentplayer + 1
            if (currentplayer > self.numPlayers - 1):
                currentplayer = 0


    """
    # Checks to see is you can really play that valid selection
    """
    def isValidPlay(self, selectionDetail):
        if (len(self.field) == 0):
            return True
        else:
            tempgroup = self.field[len(self.field) - 1]

            if (len(tempgroup) != selectionDetail['groupLength'] and selectionDetail['groupType'] != 'Bomb'):
                return False

            if (selectionDetail['groupType'] == 'Bomb' and self.bombCycle == False):
                self.bombCycle = True
                return True
            elif (selectionDetail['groupType'] == 'Bomb' and self.bombCycle == True):
                if (tempgroup[0].getCardValue() <= selectionDetail['groupPower']):
                    return True
                else:
                    return False
            elif (selectionDetail['groupType'] == 'Straight'):
                if (tempgroup[1].getCardValue() == tempgroup[0].getCardValue() + 1 and selectionDetail['groupPower'] >= tempgroup[0].getCardValue() ):
                    return True
                else:
                    return False
            else:
                if (tempgroup[0].getCardValue() <= selectionDetail['groupPower']):
                    return True
                else:
                    return False

    """
    # Plays the group
    """
    def playgroup(self, theselection):
        self.field.append(theselection)






#
