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
#gobal stats for the hitting team
G_uBB = [0] * 9 
G_HBP = [0] * 9 
G_B1 = [0] * 9 
G_B2 = [0] * 9 
G_B3 = [0] * 9 
G_HR = [0] * 9 
G_AB = [0] * 9 
G_BB = [0] * 9 
G_IBB = [0] * 9  
G_SF= [0] * 9 


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
def getPitchingStatsForYear(team, year):
    filePath = 'statsheets/' + team + 'Pitch' + str(year) + '.csv'
    with open(filePath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            return float(row['H'])/(float(row['BF'])+float(row['BB'])+float(row['HBP'])) # this returns batting avg against, minus some stats b/c this csv does not have them
            
    return 0
def getHittingStatsForYear(team, year):
    global G_uBB
    global G_HBP
    global G_B1
    global G_B2
    global G_B3
    global G_HR 
    global G_AB
    global G_BB 
    global G_IBB 
    global G_SF
    filePath = 'statsheets/' + team + 'Bats' + str(year) + '.csv'
    with open(filePath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            if(i>8):
                break
            G_uBB[i] = float(0) # not in statsheet
            G_HBP[i] = float(row['HBP'])
            G_B1[i] = float(row['H'])
            G_B2[i] = float(row['2B']) 
            G_B3[i] = float(row['3B'])
            G_HR[i] = float(row['HR']) 
            G_AB[i] = float(row['AB']) 
            G_BB[i] = float(row['BB'])
            G_IBB[i] = float(row['IBB'])  
            G_SF[i] = float(row['SF'])
            i+=1
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

battingAvgAgainst = 0
getWeightsForYear("2025")
print("Are the Angels or Dodgers hitting?d")
hittingTeam = input()
if(True):
    getHittingStatsForYear('Angels', 2025)
    battingAvgAgainst = getPitchingStatsForYear('Dodgers',2025)
    print(wOBAvP(G_uBB[0], G_HBP[0], G_B1[0], G_B2[0], G_B3[0], G_HR[0], G_AB[0], G_BB[0], G_IBB[0], G_SF[0], battingAvgAgainst, .244))
#getWeightsForYear("2025")