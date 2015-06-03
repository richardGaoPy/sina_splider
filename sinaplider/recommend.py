#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data_config import sina_data
from math import sqrt

def similarity_score(person1,person2):
    """get the similar socre"""

    both_viewed = {}        #get p1, p2 item

    for item in sina_data[person1]:
        if item in sina_data[person2]:
            both_viewed[item] = 1

        # they both items len
        if len(both_viewed) == 0:
            return 0

        # Finding Euclidean distance
        sum_of_eclidean_distance = []

        for item in sina_data[person1]:
            if item in sina_data[person2]:
                sum_of_eclidean_distance.append(pow(sina_data[person1][item] - sina_data[person2][item],2))
        sum_of_eclidean_distance = sum(sum_of_eclidean_distance)

        return 1/(1+sqrt(sum_of_eclidean_distance))



def pearson_correlation(person1,person2):
    """
    :return p1, p2 relation
    """
    both_rated = {}
    for item in sina_data[person1]:
        if item in sina_data[person2]:
            both_rated[item] = 1

    number_of_ratings = len(both_rated)

    # Checking for number of ratings in common
    if number_of_ratings == 0:
        return 0

    # Add up all the preferences of each user
    person1_preferences_sum = sum([sina_data[person1][item] for item in both_rated])
    person2_preferences_sum = sum([sina_data[person2][item] for item in both_rated])

    # Sum up the squares of preferences of each user
    person1_square_preferences_sum = sum([pow(sina_data[person1][item],2) for item in both_rated])
    person2_square_preferences_sum = sum([pow(sina_data[person2][item],2) for item in both_rated])

    # Sum up the product value of both preferences for each item
    product_sum_of_both_users = sum([sina_data[person1][item] * sina_data[person2][item] for item in both_rated])

    # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/number_of_ratings)
    denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum,2)/number_of_ratings) * (person2_square_preferences_sum -pow(person2_preferences_sum,2)/number_of_ratings))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value/denominator_value
        return r

def most_similar_users(person,number_of_users):
    # returns the number_of_users (similar persons) for a given specific person.
    scores = [(pearson_correlation(person,other_person),other_person) for other_person in sina_data if  other_person != person ]

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    scores.reverse()
    return scores[0:number_of_users]

def user_reommendations(person):

    # get relations list
    totals = {}
    simSums = {}
    rankings_list =[]
    for other in sina_data:
        # don't compare me to myself
        if other == person:
            continue
        sim = pearson_correlation(person,other)
        #print ">>>>>>>",sim

        # ignore scores of zero or lower
        if sim <=0:
            continue
        for item in sina_data[other]:

            # only score movies i haven't seen yet
            if item not in sina_data[person] or sina_data[person][item] == 0:

                # Similrity * score
                totals.setdefault(item,0)
                totals[item] += sina_data[other][item]* sim
                # sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+= sim

        # Create the normalized list

    rankings = [(total/simSums[item],item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    # returns the recommended items
    recommendataions_list = [recommend_item for score,recommend_item in rankings]
    return recommendataions_list

# if __name__ == "__main__":
#     print user_reommendations('7')
