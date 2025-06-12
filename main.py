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
G_uBB = [0] * 50 
G_HBP = [0] * 50
G_B1 = [0] * 50
G_B2 = [0] * 50
G_B3 = [0] * 50
G_HR = [0] * 50
G_AB = [0] * 50
G_BB = [0] * 50
G_IBB = [0] * 50  
G_SF= [0] * 50
G_SF= [0] * 50
G_BA = [0] * 50
G_HNAME = [""] * 50
G_PNAME = [""] * 50
G_AVG_AGAINST = [0] * 50

#odds of a hitter getting a hit against a pitcher

def truncateArray(size, array):
    arr = [0] * size
    for i in range(size):
        arr[i] = array[i]
    return arr

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
    return 0
def getPitchingStatsForYear(team, year):
    global G_AVG_AGAINST
    global G_PNAME
    filePath = 'statsheets/' + team + 'Pitch' + str(year) + '.csv'
    with open(filePath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            if(str(row['Player']) == "Team Totals"):
                break
            try:
                G_AVG_AGAINST[i] = float(row['H'])/(float(row['BF'])-float(row['BB'])-float(row['HBP'])) # this returns batting avg against, minus some stats b/c this csv does not have them
                G_PNAME[i] = str(row['Player'])
            except:
                #print("Invalid Pitcher ", str(row['Player']))
                pass #right now no error handeling is needed
            i += 1
    G_AVG_AGAINST = truncateArray(i, G_AVG_AGAINST)
    G_PNAME = truncateArray(i, G_PNAME)
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
    global G_BA
    global G_HNAME
    filePath = 'statsheets/' + team + 'Bats' + str(year) + '.csv'
    with open(filePath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            if(str(row['Player']) == "Team Totals"):
                break
            try:
                G_HNAME[i] = str(row['Player'])
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
                G_BA[i] = float(row['BA'])
            except:
                #print("Invalid Player", str(row['Player']))
                pass #right now no error handeling is needed
            i+=1
        G_uBB = truncateArray(i,G_uBB)
        G_HBP = truncateArray(i,G_HBP)
        G_B1 = truncateArray(i,G_B1)
        G_B2 = truncateArray(i,G_B2)
        G_B3 = truncateArray(i,G_B3)
        G_HR = truncateArray(i,G_HR) 
        G_AB = truncateArray(i,G_AB)
        G_BB = truncateArray(i,G_BB)
        G_IBB = truncateArray(i,G_IBB) 
        G_SF = truncateArray(i,G_SF)
        G_BA = truncateArray(i,G_BA)
        G_HNAME = truncateArray(i,G_HNAME)
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
def selectPitcher():
    for i in range(len(G_PNAME)):
        print(i, ":", G_PNAME[i])
    print("Enter the number of the pitcher: ")
    selection = -1
    while(selection == -1):
        try:
            selection = int(input())
            G_PNAME[selection]
        except:
            selection = -1
            print("Invalid Number, Try again")
    return selection

def selectHitter():
    for i in range(len(G_HNAME)):
        print(i, ":", G_HNAME[i])
    print("Enter the number of the hitter: ")
    selection = [-1]*9
    i = 0
    while(i < 9 and selection[i] == -1):
        try:
            selection[i] = int(input())
            G_HNAME[selection[i]]
            print("Enter the number of the next hitter: ")
            i+=1
        except:
            selection[i] = -1
            print("Invalid Number, Try again")
    return selection

battingAvgAgainst = 0
getWeightsForYear("2025")
print("Enter team 1:")
hittingTeam = ''
while(hittingTeam == ''):
    try:
        hittingTeam = input()
        getHittingStatsForYear(hittingTeam, 2025)
    except:
        print("Invalid team try again")
print("Enter team 2:")
pitchingTeam = ''
while(pitchingTeam == ''):
    try:
        pitchingTeam = input()
        getPitchingStatsForYear(pitchingTeam,2025)
    except:
        print("Invalid team try again")


hitters = selectHitter()
pitcher = selectPitcher()
val = [0] * 9
valT = 0
for i in range(len(hitters)):
    print(hittingOdds( G_BA[hitters[i]],G_AVG_AGAINST[pitcher], .244), G_HNAME[i])
    val[i] += hittingOdds( G_BA[hitters[i]],G_AVG_AGAINST[pitcher], .244)
    valT += val[i]




print("Expexted Hits per line up:", valT)
#getWeightsForYear("2025")