"""
******************************************************************************************
** COMP517 Continuous Assessment Task 3 - Voting Rules                                 **
** NAME: RAHUL NAWALE                                                                   **
** STUDENT ID - 201669264                                                               **
** TASK - Design and implement several voting rules.  **
**                                                                                      **
******************************************************************************************
       %%%%       %%%%%     %%%        %%%  %%% %%%%     %%%%%%%%%  %%%  %%%%%%%%
     %%%  %%%   %%%    %%%  %%% %%  %% %%%  %%%     %%%  %%         %%%      %%%%
     %%%        %%%    %%%  %%%   %%   %%%  %%%     %%%  %%%%%      %%%      %%%
     %%%        %%%    %%%  %%%        %%%  %%% %%%%          %%%   %%%     %%%
     %%%  %%%   %%%    %%%  %%%        %%%  %%%               %%%   %%%    %%%
      %%%%        %%%%%     %%%        %%%  %%%          %%%%%      %%%   %%%
===========================================================================================
generatePreferences(values): inputs a set of numerical values that the agents have for the different
alternatives and outputs a preference profile.
"""


def generatePreferences(values):
    alternative_valuations = []  # List to hold all the alternatives for each Agent
    for row in values.iter_rows(min_row=1, max_col=values.max_column):  # Iterate over the rows of worksheet
        alternative_valuation = []  # List to store all values of a particular alternative
        for cell in row:  # for each cell in a row
            alternative_valuation.append(cell.value)  # adding cell value to respective alternative's list
        alternative_valuations.append(alternative_valuation)

    preferenceProfile = {}  # Dictionary with Agent and his/her preference ordering(alternatives)
    # iterate through all values in the preferenceProfile
    for i, alternative_valuation in enumerate(alternative_valuations):
        # preference ordering list sorted and reversed to access each alternative sequentially and get count of it.
        sorted_alternative_valuation = sorted(alternative_valuation, reverse=True)

        preference_list = []  # List to store Agent's preferences
        added_indices = set()  # In case of tie, indices are followed to determine the rank
        for alternative in sorted_alternative_valuation:  # Assigning scoreVector
            # Loop for more than one alternative with same valuation
            if alternative_valuation.count(alternative) > 1:
                indices = [j for j, x in enumerate(alternative_valuation) if x == alternative]
                indices.sort(reverse=True)
                for index in indices:
                    if index not in added_indices:
                        preference_list.append(index+1)
                        added_indices.add(index)
            else:
                index = alternative_valuation.index(alternative)
                preference_list.append(index + 1)
                added_indices.add(index)

        preferenceProfile[i+1] = preference_list
    # returning Agent and his/her preference profile(alternatives) as dictionary
    return preferenceProfile


# An agent is selected, and the winner is the alternative that this agent ranks first.
# For example, if the preference ordering of the selected agent is 4>1>2>3, then the winner is alternative 4 .
def dictatorship(preferenceProfile, agent):
    #  Loop to check if inputted integer corresponds to an Agent
    if int(agent) in preferenceProfile.keys():
        winner = preferenceProfile[int(agent)][0]  # Accessing Agent's preference profile
        return winner  # returns the winning alternative
    else:
        pass


##############################################  Tie-Breaking Rules  ####################################################

# We will consider the following three tie-breaking rules. We assume that the alternatives are represented by integers.
# max: Among the possible winning alternatives, select the one with the highest number.
# min: Among the possible winning alternatives, select the one with the lowest number.
# agent : Among the possible winning alternatives, select the one that agent  ranks the highest in preference ordering
##############################################  Tie-Breaking Rules  ####################################################.


# For every agent, the function assigns the highest score in the scoring vector to the most preferred alternative of the agent
# the second-highest score to the second most preferred alternative of the agent and so on
# and the lowest score to the least preferred alternative of the agent. 
# In the end, it returns the alternative with the highest total score
# use the tie-breaking option to distinguish between alternatives with the same score
def scoringRule(preferences, scoreVector, tieBreak):
    # try catch to handle unsupported variable types
    try:
        scoreVector.sort()
        scoreVector.reverse()
        # Exception handling when length of scoreVector is not equal to number of alternatives
        if len(scoreVector) != len(preferences[1]):
            print("Incorrect input")
            return False

        alt_list_len = len(preferences[1])
        count = 1
        sum_dict = {} # dictionary to score the alternative and its scoreVector
        while count <= alt_list_len:
            sum_dict["{0}".format(count)] = []
            count += 1
        for alist in preferences.values():
            count = 0
            for element in alist:
                sum_dict[str(element)].append(scoreVector[count])
                count += 1
        # List to store summation of alternatives scoreVectors
        max_sum_list = max(sum_dict.values(), key=sum)
        if len([k for k, v in sum_dict.items() if v == max_sum_list]) == 1:
            # returns the winning alternative
            return int([k for k, v in sum_dict.items() if v == max_sum_list][0])

        # Tie-Breaking Rules (See above for detailed information)
        else:
            if tieBreak == "max":
                # returns the winning alternative
                return int(max([k for k, v in sum_dict.items() if v == max_sum_list]))
            if tieBreak == "min":
                # returns the winning alternative
                return int(min([k for k, v in sum_dict.items() if v == max_sum_list]))
            if type(tieBreak == int):
                if tieBreak in preferences.keys():
                    for num in preferences[tieBreak]:
                        if str(num) in [k for k, v in sum_dict.items() if v == max_sum_list]:
                            return num  # returns the winning alternative
                            break
                        else:
                            pass
                else:
                    pass
    except AssertionError:
        pass


# The winner is the alternative that appears the most-
# -times in the first position of the agents' preference orderings
def plurality(preferences, tieBreak):
    count_winner = []  # List to store first ranked alternative of each agent
    # Loop to store first ranked alternative of each agent
    for alist in preferences.values():
        count_winner.append(alist[0])

    winners_dict = {}  # dictionary to store alternative as key and its occurrence as value
    # Loop to store alternatives and its occurrence
    for e in count_winner:
        if e in winners_dict.keys():
            winners_dict[e] += 1
        else:
            winners_dict[e] = 1
    max_occur = max(winners_dict.values())
    max_keys = [k for k, v in winners_dict.items() if v == max_occur]
    if len(max_keys) == 1:
        return max_keys[0]  # returns the winning alternative
    # Tie-Breaking Rules (See above for detailed information)
    elif tieBreak == "max":
        return max(max_keys)  # returns the winning alternative
    elif tieBreak == "min":
        return min(max_keys)  # returns the winning alternative
    elif type(tieBreak) == int:
        if tieBreak in preferences.keys():
            for num in preferences[tieBreak]:
                if num in max_keys:
                    return num  # returns the winning alternative
    else:
        pass


# Every agent assigns 0 points to the alternative that they rank in the last place of their preference orderings,
# and 1 point to every other alternative. The winner is the alternative with the most number of points
def veto(preferences, tieBreak):
    winners_dict = {}  # dictionary to store alternative as key and its points as value
    # Loop to assign points to the alternatives
    for alist in preferences.values():
        for i in range(1, len(alist)):
            if alist[i - 1] in winners_dict.keys():
                winners_dict[alist[i - 1]] += 1
            else:
                winners_dict[alist[i - 1]] = 1
    max_occur = max(winners_dict.values())
    # List of alternatives with maximum points
    max_keys = [k for k, v in winners_dict.items() if v == max_occur]

    if len(max_keys) == 1:
        return max_keys[0]  # returns the winning alternative
    # Tie-Breaking Rules (See above for detailed information)
    elif tieBreak == "max":
        return max(max_keys)  # returns the winning alternative
    elif tieBreak == "min":
        return min(max_keys)  # returns the winning alternative
    elif type(tieBreak) == int:
        if tieBreak in preferences.keys():
            for num in preferences[tieBreak]:
                if num in max_keys:
                    return num  # returns the winning alternative
    else:
        pass


# Every agent assigns a score of 0 to their least-preferred alternative (the one at the bottom of the ranking)
# a score of 1 to the second least-preferred alternative,... , and a score of m-1 to their favourite alternative.
# In other words, the alternative ranked at position j receives a score of m-j.
# The winner is the alternative with the highest score.
def borda(preferences, tieBreak):
    winners_dict = {}  # dictionary to store alternative as key and its points as value
    # Loop to assign points to the alternatives
    for alist in preferences.values():
        for i in range(1, len(alist)+1):
            num = alist[i - 1]
            num_index = alist.index(num)
            if alist[i - 1] in winners_dict.keys():
                winners_dict[alist[i - 1]] = winners_dict[alist[i - 1]] + len(alist) - num_index +1
            else:
                winners_dict[alist[i - 1]] = len(alist) - num_index +1
    max_occur = max(winners_dict.values())
    # List of alternatives with maximum points
    max_keys = [k for k, v in winners_dict.items() if v == max_occur]
    if len(max_keys) == 1:
        return max_keys[0]  # returns the winning alternative
    # Tie-Breaking Rules (See above for detailed information)
    elif tieBreak == "max":
        return max(max_keys)  # returns the winning alternative
    elif tieBreak == "min":
        return min(max_keys)  # returns the winning alternative
    elif type(tieBreak) == int:
        if tieBreak in preferences.keys():
            for num in preferences[tieBreak]:
                if num in max_keys:
                    return num  # returns the winning alternative
    else:
        pass


# Every agent assigns a score of 1/m to their least-preferred alternative (the one at the bottom of the ranking)
# a score of 1/(m-1) to the second least-preferred alternative, ... , and a score of 1 to their favourite alternative.
# In other words, the alternative ranked at position j receives a score of 1/j.
def harmonic(preferences, tieBreak):
    winners_dict = {}  # dictionary to store alternative as key and its points as value
    for alist in preferences.values():
        for i in range(1, len(alist)+1):
            num = alist[i - 1]
            num_index = alist.index(num)
            if alist[i - 1] in winners_dict.keys():
                winners_dict[alist[i - 1]] = winners_dict[alist[i - 1]] + 1/(num_index +1)
            else:
                winners_dict[alist[i - 1]] = 1/(num_index +1)
    max_occur = max(winners_dict.values())
    # List of alternatives with maximum points
    max_keys = [k for k, v in winners_dict.items() if v == max_occur]
    if len(max_keys) == 1:
        return max_keys[0]  # returns the winning alternative
    # Tie-Breaking Rules (See above for detailed information)
    elif tieBreak == "max":
        return max(max_keys)  # returns the winning alternative
    elif tieBreak == "min":
        return min(max_keys)  # returns the winning alternative
    elif type(tieBreak) == int:
        if tieBreak in preferences.keys():
            for num in preferences[tieBreak]:
                if num in max_keys:
                    return num  # returns the winning alternative
    else:
        pass


# The voting rule works in rounds.
# In each round, the alternatives that appear the least frequently in the first position of agents' rankings are removed
# and the process is repeated. When the final set of alternatives is removed (one or possibly more)
# then this last set is the set of possible winners
def STV(preferences, tieBreak):
    count_winner = []  # List to store first ranked alternative of each agent
    # Loop to store first ranked alternative of each agent
    for li in preferences.values():
        count_winner.append(li[0])
    winners_dict = {}  # dictionary to store alternative as key and its points as value
    for e in count_winner:
        if e in winners_dict.keys():
            winners_dict[e] += 1
        else:
            winners_dict[e] = 1
    while len(set(winners_dict.values())) != 1:
        min_occur = min(winners_dict.values())
        # List of alternatives which are the least appearing at the first rank
        min_keys = [k for k, v in winners_dict.items() if v == min_occur]

        for e in min_keys:
            winners_dict.pop(e)
        for l in preferences.values():
            for e in min_keys:
                l.remove(e)
    max_alt = list(winners_dict.keys())
    if len(max_alt) == 1:
        return max_alt[0]  # returns the winning alternative
    # Tie-Breaking Rules (See above for detailed information)
    elif tieBreak == "max":
        return max(max_alt)  # returns the winning alternative
    elif tieBreak == "min":
        return min(max_alt)  # returns the winning alternative
    elif type(tieBreak) == int:
        if tieBreak in preferences.keys():
            for num in preferences[tieBreak]:
                if num in max_alt:
                    return num  # returns the winning alternative
    else:
        pass


# The function should return the alternative that has the maximum sum of valuations,
# i.e., the maximum sum of numerical values in the xlsx file,
# using the tie-breaking option to distinguish between possible winners.
def rangeVoting(values, tieBreak):
    # Read the valuations from the worksheet
    valuations = []  # List to store cell values from rows of worksheet
    for row in values.iter_rows(min_row=1, max_col=values.max_column):
        valuations.append([cell.value for cell in row])
    # List to store alternatives with sum of its valuation
    sums = [sum(x) for x in zip(*valuations)]
    max_keys = [i + 1 for i, x in enumerate(sums) if x == max(sums)]

    if len(max_keys) == 1:
        return max_keys[0]  # returns the winning alternative
    # Tie-Breaking Rules (See above for detailed information)
    else:
        preferences = {}  # Dictionary with Agent and his/her preference ordering(alternatives)
        # iterate through all values in the preferenceProfile
        for i, valuation in enumerate(valuations):
            # preference ordering list sorted and reversed to access each alternative sequentially and get count of it.
            sorted_valuation = sorted(valuation, reverse=True)
            preference_list = []  # List to store Agent's preferences
            added_indices = set()  # In case of tie, indices are followed to determine the rank
            for alternative in sorted_valuation:
                # loop to consider more than alternative having same valuation
                if valuation.count(alternative) > 1:
                    indices = [j for j, x in enumerate(valuation) if x == alternative]
                    indices.sort(reverse=True)
                    for index in indices:
                        if index not in added_indices:
                            preference_list.append(index + 1)
                            added_indices.add(index)
                else:
                    index = valuation.index(alternative)
                    preference_list.append(index + 1)
                    added_indices.add(index)
            # appending Agent and his/her preference profile(alternatives) to the dictionary
            preferences[i + 1] = preference_list
    # Tie-Breaking Rules (See above for detailed information)
    if tieBreak == "max":
        return max(max_keys)  # returns the winning alternative
    elif tieBreak == "min":
        return min(max_keys)  # returns the winning alternative
    elif type(tieBreak) == int:
        if tieBreak in preferences.keys():
            for num in preferences[tieBreak]:
                if num in max_keys:
                    return num  # returns the winning alternative
    # Tie-Breaking Rules (See above for detailed information)
    else:
        pass