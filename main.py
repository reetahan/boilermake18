
import pandas as pd
import numpy as np




def main():
    print ('Welcome to the Neighborhood Suggestion Machine!')
    weight_list = []
    other_info = []

    airQualNum = input('Air Quality Weight?')
    weight_list.append(int(airQualNum))

    crimeNum = input('Crime Weight?')
    weight_list.append(int(crimeNum))

    hospNum = input('Hospital Weight?')
    weight_list.append(int(hospNum))

    parkWeight = input('Park Weight?')
    weight_list.append(int(parkWeight))


    incomeVal = input('What is your income?')
    incomeNum = input('Income Weight:')
    weight_list.append(int(incomeNum))
    other_info.append(int(incomeVal))

    polParty = input('What political party do you align with?')
    if(polParty.lower()=='republican' or polParty.lower()=='r' or polParty.lower == 'gop'):
        polPartyNum = -1
    if(polParty.lower()=='democrat' or polParty.lower()=='d' or polParty.lower == 'democrats'):
        polPartyNum = 1
    else:
        polPartyNum = 0
    polPartyWeight = input('Politics Weight?')
    weight_list.append(int(polPartyWeight))
    other_info.append(polPartyNum)



    kidAge = 0
    kidsNum = input('How many kids do you have?')
    schoolWeight = input('School Weight')
    if(int(kidsNum) > 0):
        kidAge = input('Age of the youngest child?')
    weight_list.append(int(schoolWeight))
    other_info.append(int(kidsNum))
    other_info.append(int(kidAge))

    '''end data collection'''

    lines = [line.strip() for line in open('townlist.txt')]
    the_scores = []
    scores_to_towns = {}
    for i in range(0,35):
        cur = str(lines[i])
        score = calc_town(cur,weight_list, other_info)
        the_scores.append(score)
        scores_to_towns[score] = cur



    the_scores.sort()

    best_town = scores_to_towns[the_scores[len(the_scores)-1]]
    second_best = scores_to_towns[the_scores[len(the_scores)-2]]
    third_best = scores_to_towns[the_scores[len(the_scores)-3]]
    print(best_town)
    print(second_best)
    print(third_best)



def calc_town(town,weight, add_info):
    score = 0

    '''read CSVs'''
    aqi = pd.read_csv('aqi.csv')
    schools = pd.read_csv('Schools.csv')
    sea_crime = pd.read_csv('SeattleCrime.csv')
    sea_hosp = pd.read_csv('SeattleHospitals.csv')
    sea_income = pd.read_csv('SeattleIncome.csv')
    sea_parks = pd.read_csv('SeattleParks.csv')
    politics = pd.read_csv('politics.csv')

    '''Air Quality'''

    aq_avg = int(aqi['AQI'].mean())
    aq = int(aqi.loc[aqi['Neighborhood'] == town,'AQI'])
    aq_calc = (1-(aq/aq_avg))*(weight[0])
    score += aq_calc

    '''Crime'''
    crime_violence = 1 - 10*(int(sea_crime.loc[sea_crime['Neighborhood'] == town,'Violent Crime']))
    crime_nonviolence = -1*(int(sea_crime.loc[sea_crime['Neighborhood'] == town,'Non-Violent Crime']))
    score += (crime_violence + crime_nonviolence)*(weight[1])

    '''Hospitals'''
    hosp_sum = sea_hosp['Distance to nearest good hospital'].sum()
    hosp_avg = hosp_sum/36

    zeze = (weight[2])*(hosp_avg - (int(sea_hosp.loc[sea_hosp['Neighborhood'] == town,'Distance to nearest good hospital'])))
    if(zeze > 10):
        zeze = 10
        score += zeze
    elif (zeze < 0):
        zeze = 0
        score += zeze
    else:
        score += zeze


    '''Parks'''
    list_neighbor = sea_parks['Neighborhood'].tolist()
    list_neighbor_parkdist = sea_parks['Distance to Park'].tolist()

    counter = 0
    i = 0
    park_sum = 0
    while(counter < 3):
        if(str(list_neighbor[i]) == town):
            park_sum += int(list_neighbor_parkdist[i])
            counter = counter + 1
        i = i + 1
    a = park_sum/3.0
    score += (weight[3])*(1.0/(a+1))

    '''Income'''
    ratio = (int(sea_income.loc[sea_income['Neighborhood'] == town,'Median Income']))/(add_info[0])
    absd = abs(ratio - 1)
    score += (weight[4])*(1- absd)

    '''Politics'''
    if(int(politics.loc[politics['Neighborhood'] == town,'Political Leaning'])*(add_info[1]) == -1):
        weight[5] = -1*weight[5]
    score += (abs(add_info[1]))*(weight[5])

    '''Schools'''
    elem = False
    middle = False

    if(weight[6] > 0 and add_info[2] == 0):
        elem = True
        middle = True
    if(add_info[3] <= 11):
        elem = True
        middle = True
    if(add_info[3] >= 12 and add_info[3] <= 14):
        middle = True


    if(elem and middle):
        sum = int(schools.loc[schools['Neighborhood'] == town,'E Rating']) + int(schools.loc[schools['Neighborhood'] == town,'M Rating']) + int(schools.loc[schools['Neighborhood'] == town,'H Rating'])
        score += (weight[6])*((sum - 15)/15.0)

    elif(middle):
        sum = int(schools.loc[schools['Neighborhood'] == town,'M Rating']) + int(schools.loc[schools['Neighborhood'] == town,'H Rating'])
        score += (weight[6])*((sum - 10)/10.0)

    else:
        sum =  int(schools.loc[schools['Neighborhood'] == town,'H Rating'])
        score += (weight[6])*((sum - 5)/5.0)

        '''Hurray'''

    return score


if __name__ == '__main__':
    main()
