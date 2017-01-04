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

    # List of player scores
    playerScores = []

    # The field
    field = []

    # The exit order
    exitOrder = []

    # Bomb cycle flag
    bombCycle = False

    # How much bonus the round winner gets
    winningMultiplier = 2


    """
    # Initializes a new game.
    # Parameters:
    #   players | total number of players
    #
    """
    def __init__(self, players, baseSize, winmult):
        self.numPlayers = players
        self.deckbaseSize = baseSize
        self.playerScores = []
        self.winningMultiplier = winmult

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

            for pl in range(self.numPlayers):
                self.playerScores.append(0)

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
    # Controls the flow of the game
    #
    #
    """
    def gameMain(self):
        gameOver = False

        while (gameOver == False):
            self.cycleMain()

            self.endcycle()

            self.newcycleSetup()



    """
    # Controls flow of the cycle
    #
    #
    #
    """
    def cycleMain(self):

        roundWinner = 0
        cycleOver = False
        while (cycleOver == False):
            roundWinner = self.roundMain(roundWinner)

            self.endround(roundWinner)

            if (len(self.exitOrder) >= self.numPlayers - 1
                cycleOver = True
            else:
                self.newroundSetup(roundWinner)





    """
    # Controls flow of the round
    #
    # Returns: the number of the player who won the round.
    #
    """
    def roundMain(self, cplayer):
        currentplayer = cplayer
        lastActivePlayer = None
        passcount = 0
        roundOver = False
        self.bombCycle = False

        while (roundOver == False):

            playinghand = self.playerHands[currentplayer]
            print ("Current player:")
            print (currentplayer)

            if (len(self.field) > 0):
                print ("Current field:")

                for card in self.field[len(self.field) - 1]['theSelection']:
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
                    finalSelection['playedBy'] = currentplayer
                    self.playgroup(finalSelection)
                    playinghand.selectionPlayed()
                    lastActivePlayer = currentplayer
                    passcount = 0
                else:
                    print ("Can't play that, try again!")
                    playinghand.clearSelection()


            if (passcount >= self.numPlayers):
                roundOver = True

            findingNextPlayer = True

            while (findingNextPlayer):
                currentplayer = currentplayer + 1

                if (currentplayer > self.numPlayers - 1):
                    currentplayer = 0

                if (currentplayer not in self.exitOrder):
                    findingNextPlayer = False

        return lastActivePlayer

    """
    # Checks to see is you can really play that valid selection
    """
    def isValidPlay(self, selectionDetail):
        if (len(self.field) == 0):
            return True
        else:
            tempgroup = self.field[len(self.field) - 1]['theSelection']

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
    def playgroup(self, thegroup):
        self.field.append(thegroup)





    """
    # Controls end of round operation flow
    # eg. scoring
    #
    #
    #
    """
    def endround(self, winner):

        print ("Player %d won the round!" % (winner))

        # Scoring
        self.scoreRound(winner)
        playerNo = 0
        print ("Current Scores")
        for playerscore in self.playerScores:
            print ("Player %d : %d" % (playerNo, playerscore))
            playerNo = playerNo + 1


        # Check if winner has exit
        lengthOfWinningHand = self.playerhands[winner]
        if (lengthOfWinningHand == 0):
            exitOrder.append(winner)

    """
    # Scores the groups from the round.
    #
    #
    """
    def scoreRound(self, winner):
        playertoScore = None

        tempScoringArray = []

        # Group scoring
        while not self.fieldEmpty():

            score = 0

            scoringGroup = self.field.pop()
            playertoScore = scoringGroup['playedBy']

            score = self.calcScore(scoringGroup)

            if (playertoScore == winner):
                score = score * self.winningMultiplier


            self.playerScores[playertoScore] = self.playerScores[playertoScore] + score
            tempScoringArray.append(scoringGroup)


        # Escalation scoring
        while (len(tempScoringArray) > 0):
            count = 0
            score = 0
            scoringGroup = tempScoringArray.pop()


    """
    # Calculates the score of a group
    #
    #
    """
    def calcScore(self, sGroup):
        thescore = 0
        scoringGroup = sGroup
        theSelection = scoringGroup['theSelection']

        if (scoringGroup['groupType'] == 'Bomb'):
            pass
        elif (scoringGroup['groupType'] == 'Straight'):
            pass
        else:
            pass

        return thescore

    """
    # Determines if field is empty.
    #
    """
    def fieldEmpty(self):
        if (len(self.field) == 0):
            return True
        else:
            return False


    """
    # Controls setup for next round
    #
    #
    #
    #
    """
    def newroundSetup(self, winner):
        pass



    """
    # Controls end of cycle
    #
    #
    """
    def endcycle(self):
        pass




    """
    # Controls setup for new Cycle
    #
    #
    #
    #
    """
    def newcycleSetup(self):
        pass













#
