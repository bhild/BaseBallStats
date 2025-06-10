#the stats the will are most likely to matter are as follows:
# offensive stats:
#   batting average
#   slugging percentage
#   RBI
#   On-base percentage
#   Walks drawn
# Defensive stats:
#   ERA
#   Hits allowed
#   Bases Allowed
#   Strikeouts
#   Walks thrown
#   Batting Average Against
#team stats:
#   Errors
#   Past Head to Head
#   Left On Base
#   Win percentage

import csv



#these are the weights for weighted on base average
wBB	= .0 #weight for base on balls (walks)
wHBP = .0 #wieght for hit by pitch
w1B	= .0 #wieght for single
w2B = .0 #wieght for double
w3B	= .0 #wieght for triple
wHR	= .0 #wieght for homerun

#odds of a hitter getting a hit against a pitcher

def getWeightsForYear(year): #gets the wOBA weights for the relevant year
    global wBB
    global wHBP
    global w1B
    global w2B
    global w3B
    global wHR
    with open('statsheets/FanGraph_wOBA_weights.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['year'] == year):
                wBB = float(row['wBB'])
                wHBP = float(row['wHBP'])
                w1B = float(row['w1B'])
                w2B = float(row['w2B'])
                w3B = float(row['w3B'])
                wHR = float(row['wHR'])
    print(wBB, wHBP, w1B, w2B, w3B, wHR)
    return 0

def hittingOdds( battingAvg, battingAvgAgainst, leagueAvg):
    hitChance = ((battingAvg*battingAvgAgainst)/leagueAvg)
    hitChance /= hitChance + (((1-battingAvg)*(1-battingAvgAgainst))/(1-leagueAvg))
    return hitChance

#expected number of bases
def wOBA(uBB, HBP, B1, B2, B3, HR, AB, BB, IBB, SF):
    #B1 = single
    #b2 = double
    #b3 = triple
    #HR = homerun
    #AB = at bats
    #BB = base on balls (walks)
    #IBB = intentional base on balls
    #SF = sacrifice fly
    #HBP = hit by pitch
    ret = (wBB * uBB + wHBP * HBP + w1B * B1 + w2B * B2 + w3B * B3 + wHR * HR)
    ret /= (AB + BB - IBB + SF + HBP)
    return ret

#this is wOBA vs a pitcher
#I am not sure the best way to compute this
#for now I am going to plug wOBA into the hittingOdds in place of batting average, which should produce a value close to the target
def wOBAvP(uBB, HBP, B1, B2, B3, HR, AB, BB, IBB, SF, battingAvgAgainst, leagueAvg):
    hitChance = hittingOdds(wOBA(uBB, HBP, B1, B2, B3, HR, AB, BB, IBB, SF), battingAvgAgainst, leagueAvg)
    ret = (wBB * uBB + wHBP * HBP + w1B * B1 + w2B * B2 + w3B * B3 + wHR * HR)
    ret /= (AB + BB - IBB + SF + HBP) # total number of 
    return ret


getWeightsForYear("2025")