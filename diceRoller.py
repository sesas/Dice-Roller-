'''
Later I might want to pass to the initializer a sequence of fractions representing how likely
a number is. (normal 6 sided dice would be (1/6, 1/6, 1/6, 1/6, 1/6, 1/6).

But not for now.
'''
import resources as res
import random 
import itertools as itr
r = random

class dice:

    def __init__(self, num_dice=2, sides = 6, seed = 0):
        self.sides = sides
        self.num_dice = num_dice

        if seed:
            random.seed(seed)
        
        def roll( rolls=num_dice):
            ''' most games would want you to roll 2 dice.
    '''
            return sum( random.randint(1, sides) for j in range(rolls) )
        self.roll = roll

        def checkAverage( rolls=num_dice, length=100 ):
            return sum( roll(rolls) for j in range(length) )/length
        self.checkAverage = checkAverage

    def roll1(self):
        return self.roll(1)

import collections
import os
class statManager:
    def __init__(self, diceObj=None):
        self.rollHist = []
        if diceObj:
            self.setDiceObj(diceObj)

    def setDiceObj(self, diceObj):
        '''
>>> sm = statManager()
>>> d = dice()
>>> sm.setDiceObj(d)
>>> sorted(sm.counter)
[(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0)]
>>> 
'''
        self.dice = diceObj
        self.max = diceObj.num_dice * diceObj.sides
        self.min = diceObj.num_dice
        self.counter = collections.Counter( range(self.min, self.max+1) )
        self.counter.subtract( range(self.min, self.max+1) )
        # the following line is slow if using more than 8 dice.
        # (might want to put on separate thread)
        self.diceProbab = collections.Counter(map( sum,
                                           itr.product( range(1,self.dice.sides+1), repeat=self.dice.num_dice)  ) )
        self.totalPoss = sum( self.diceProbab.values() )
        self.theor_probab = { num:dp/self.totalPoss for num, dp in self.diceProbab.items() }

    def probDiff(self):
        nRolls = len(self.rollHist)
        actualProb = { k:prob/nRolls for k, prob in self.counter.items() }
        probDiff = { k:(actualProb[k]-self.theor_probab[k]) for k in actualProb }
        return probDiff
        pass

    def addRoll(self, rollVal):
        self.rollHist.append(rollVal)
        self.counter[rollVal] += 1
        return rollVal

    def deleteLast(self):
        delVal = self.rollHist.pop()
        self.counter[delVal] -= 1
        return

    def resetCounter(self):
        self.counter.clear()
##        self.counter.update( (j, 0) for j in range(self.min, self.max+1) )
        self.counter.update( range(self.min, self.max+1) )
        self.counter.subtract( range(self.min, self.max+1) )
        self.counter.update( self.rollHist )
        

class histGraph:
    defaultLineFormat = "{num: >3}: {count: >3},{diff: >+8.2F} - {0:{pad}>{strLen}}"
    def __init__(self, statObj, linesWidth = 70, lineFormat = defaultLineFormat, padString='#'):
        self.linesWidth = linesWidth
        self.lineFormat = lineFormat
        self.padString = padString
        if statObj:
            self.statObj = statObj

    def getGraph(self, counterObj=None):
        if not counterObj:
            counterObj = self.statObj.counter
        lines  = []
        maxCount = max(counterObj.values())
        charMultiplier = self.linesWidth / (maxCount*len(self.padString))
        diffDict = self.statObj.probDiff()
        for val, count in sorted(counterObj.items()):
            lines.append( self.lineFormat.format(
                    '', num=val, strLen=int(count*charMultiplier),
                    pad=self.padString, count=count, diff=diffDict[val]*100) )
            pass
        return lines
##            for item in sorted(counterObj):
##                line = defaultLineFormat.format( '', *item )
##        self.getGraph = getGraph

    def getRollHist(self):
        return str(self.statObj.rollHist)[-self.linesWidth:].strip(' ,][')

    def __str__(self):
        histLines = self.getGraph()
        histLines.append( self.getRollHist() + " <> Roll# " + str(len(self.statObj.rollHist)) )
        return os.linesep.join(histLines)
        pass

class game:
    def __init__(self):
        self.dice = dice()
        self.statm = statManager(self.dice)
        self.histGraph = histGraph(self.statm)
        self.numPics = res.num
        self.run()

    def run(self):
        while 1:
            roll = self.statm.addRoll(self.dice.roll())
            try:
                print( self.numPics[roll] )
            except(IndexError):
                print( self.numPics[0] )
            print(self.histGraph)
            input()


##def poss(nd, ns):
##    if nd:
##        gen = poss(nd-1, ns)
##        
##        for j in gen:
##            for r in range(ns):
##                
##                yield j + [r+1]
##    else:
####        for r in range(ns):
##            yield []
##                    
##print ( collections.Counter( map( sum, [k for k in poss(3, 6)]  ) ) )
##           
##print ( collections.Counter( map( sum, [k for k in poss(3, 8)]  ) ) )
##a = collections.Counter( map( sum, itr.product( range(1,7), repeat=2)  ) )
##print (a)
##print (sum(a.values()))
####for j in range(13):
##    

import math
p = 1/6
##print(p)
def binom(n, k, p = p):
    return (n**k / math.factorial(k)) * p**k * (1-p)**(n-k)

if __name__ == "__main__":
##    d = dice()
##    sm = statManager(d)
##    h = histGraph(sm, padString = '|')
##    while 1:
##        for j in range(10):
##            sm.addRoll(d.roll())
##        print( res.num[1] )
##        print(h)
##        input()    
##
            
    g = game()
    pass


