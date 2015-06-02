#!/usr/bin/evn python
# -*- coding:utf-8 -*-
#0p = sqrt((x1-x2)^2 + (y1-y2)^2) |x| = ~(x2+y2)

from math import sqrt

from data_config import sina_data

def conform_score(p1, p2):
    """
    :return [euclidean]distance score of person1 and person2
    """
    both_viewed = dict()        #get rated items

    for item in sina_data[p1]:
        if item in sina_data[p2]:
            both_viewed[item] = 1

    if len(both_viewed) == 0:
        return 0

    sum_of_eclidean_distance = []

    for item in both_viewed:
        sum_of_eclidean_distance.append(pow(sina_data[p1][item]-sina_data[p2][item], 2))

    sum_distance = sum(sum_of_eclidean_distance)
    return 1/(1+sqrt(sum_distance))

def corelation_person(p1, p2):
    """"""
    both_rated = dict()
    for item in sina_data[p1]:
        if item in sina_data[p2]:
            both_rated[item] = 1

    num_of_ratings = len(both_rated)

    if num_of_ratings == 0:
        return 0

    #sum preferences of each user
    p1_preferences_sum = sum([sina_data[p1][item] for item in both_rated])
    p2_preferences_sum = sum([sina_data[p2][item] for item in both_rated])

    sum_of_both_users = sum([sina_data[p1][item]*sina_data[p2][item] for item in both_rated])

    numerator_value = sum_of_both_users - (p1_preferences_sum*p2_preferences_sum/num_of_ratings)
    denominator_value = sqrt((p1_preferences_sum - pow(p1_preferences_sum,2)/num_of_ratings) *
                             (p2_preferences_sum - pow(p2_preferences_sum,2)/num_of_ratings))

    if denominator_value == 0:
        return 0
    else:
        r = numerator_value/denominator_value
        return r

def most_conform_users(person, number_of_users):
    scores = [(corelation_person(person, other_person), other_person)
              for other_person in sina_data if other_person != person]
    scores.sort()
    scores.reverse()
    return scores[0:number_of_users]

def user_reommendation(person):
    totals = {}
    sim_sums = {}
    rankings_list = []
    for other in sina_data:
        if other == person:
            continue
        sim = corelation_person(person, other)

        if sim <= 0:
            continue
        for item in sina_data[other]:
            if item not in sina_data[person] or sina_data[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += sina_data[other][item]*sim

                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    rankings = [(totals/sim_sums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    reco_list = [recommend_item for score, recommend_item in rankings]
    return reco_list

if __name__ == "__main__":
    user_reommendation()