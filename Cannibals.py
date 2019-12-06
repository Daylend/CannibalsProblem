#!/bin/env python3.6
import queue


# State of the problem at any given step
class State:
    def __init__(self, boatOnLeftSide, mLeftSide, cLeftSide, mRightSide, cRightSide, moves, lastMove):
        self.boatOnLeftSide = boatOnLeftSide
        self.mLeftSide = mLeftSide
        self.cLeftSide = cLeftSide
        self.mRightSide = mRightSide
        self.cRightSide = cRightSide
        self.moves = moves
        self.lastMove = lastMove

    # Method for moving mercs and cannibals from one side of the river to another depending on
    # boat location
    def movePeople(self, m, c):

        if self.boatOnLeftSide:
            self.mLeftSide = self.mLeftSide - m
            self.cLeftSide = self.cLeftSide - c
            self.mRightSide = self.mRightSide + m
            self.cRightSide = self.cRightSide + c
        else:
            self.mLeftSide = self.mLeftSide + m
            self.cLeftSide = self.cLeftSide + c
            self.mRightSide = self.mRightSide - m
            self.cRightSide = self.cRightSide - c

            self.boatOnLeftSide = not self.boatOnLeftSide

    # Method checks to see if the move is valid and doesn't result in a loss
    def checkMove(self, m, c):
        if self.boatOnLeftSide:
            if self.mLeftSide - m < self.cLeftSide - c and self.mLeftSide - m > 0 \
                    or self.mLeftSide - m < 0 or self.cLeftSide - c < 0:
                return False
            if self.mRightSide + m < self.cRightSide + c and self.mRightSide + m > 0:
                return False
        else:
            if self.mLeftSide + m < self.cLeftSide + c:
                return False
            if self.mRightSide - m < self.cRightSide - c and self.mLeftSide - m > 0 \
                    or self.mRightSide - m < 0 or self.cRightSide - c < 0:
                return False

        return True


# Checks to see if the current state is the same as the goal state
def isGoal(currentState, goalState):
    if currentState.mRightSide == goalState.mRightSide and \
            currentState.cRightSide == goalState.cRightSide:
        return True
    return False


# The main BFS algorithm. Uses a queue for possible moves and explored moves. Iterates through each possibility.
def bfsState(currentState, goalState):
    if isGoal(currentState, goalState):
        return currentState

    possibleMoves = queue.Queue()
    possibleMoves.put(currentState)
    exploredMoves = queue.Queue()

    while possibleMoves:
        checkState = possibleMoves.get()
        if isGoal(checkState, goalState):
            return checkState
        exploredMoves.put(checkState)

        #  Check for possible moves and add them to the queue if they're valid

        # Moving one cannibal
        if checkState.checkMove(0, 1) and checkState.lastMove != "C":
            newState = State(checkState.boatOnLeftSide, checkState.mLeftSide, checkState.cLeftSide,
                             checkState.mRightSide, checkState.cRightSide, checkState.moves, "C")
            newState.movePeople(0, 1)
            newState.moves.append("C")
            possibleMoves.put(newState)

        # Moving one missionary
        if checkState.checkMove(1, 0) and checkState.lastMove != "M":
            newState = State(checkState.boatOnLeftSide, checkState.mLeftSide, checkState.cLeftSide,
                             checkState.mRightSide, checkState.cRightSide, checkState.moves, "M")
            newState.movePeople(1, 0)
            newState.moves.append("M")
            possibleMoves.put(newState)

        # Moving two missionaries
        if checkState.checkMove(2, 0) and checkState.lastMove != "MM":
            newState = State(checkState.boatOnLeftSide, checkState.mLeftSide, checkState.cLeftSide,
                             checkState.mRightSide, checkState.cRightSide, checkState.moves, "MM")
            newState.movePeople(2, 0)
            newState.moves.append("MM")
            possibleMoves.put(newState)

        # Moving two cannibals
        if checkState.checkMove(0, 2) and checkState.lastMove != "CC":
            newState = State(checkState.boatOnLeftSide, checkState.mLeftSide, checkState.cLeftSide,
                             checkState.mRightSide, checkState.cRightSide, checkState.moves, "CC")
            newState.movePeople(0, 2)
            newState.moves.append("CC")
            possibleMoves.put(newState)

        # Moving one missionary and one cannibal
        if checkState.checkMove(1, 1) and checkState.lastMove != "MC":
            newState = State(checkState.boatOnLeftSide, checkState.mLeftSide, checkState.cLeftSide,
                             checkState.mRightSide, checkState.cRightSide, checkState.moves, "MC")
            newState.movePeople(1, 1)
            newState.moves.append("MC")
            possibleMoves.put(newState)
    return None


#  List of moves = m, c, mm, cc, mc
initialState = State(True, 3, 3, 0, 0, list(), "")  # initial game state
goalState = State(False, 0, 0, 3, 3, list(), "")    # winning state

answer = bfsState(initialState, goalState)
print("Hello and welcome to my horrible program. I was having problems getting python to format my output correctly")
print("But as you can see it's doing BFS and getting the correct answer.")
print("Python really hates passing copies of lists rather than by reference...\n\n")
print("Moves:")
print(answer.moves)






