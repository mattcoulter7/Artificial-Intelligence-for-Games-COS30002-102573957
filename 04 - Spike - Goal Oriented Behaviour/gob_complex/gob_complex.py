'''Goal Oriented Behaviour

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

Works with Python 3+

Simple decision approach.
* Choose the most pressing goal (highest insistence value)
* Find the action that fulfills this "goal" the most (ideally?, completely?)

Goal: Eat (initially = 4)
Goal: Sleep (initially = 3)

Action: get raw food (Eat -= 3)
Action: get snack (Eat -= 2)
Action: sleep in bed (Sleep -= 4)
Action: sleep on sofa (Sleep -= 2)


Notes:
* This version is simply based on dictionaries and functions.

'''

VERBOSE = True

# Global goals with initial values
goals = {
    'Money': 100, #goal is complete when = 0
    'Energy': 100, #goal is complete when equal = 0
}

# Global (read-only) actions and effects
actions = {
    # Money Focussed
    'Sell unused belongings': { 'Money': -10, 'Energy': 5}, # chance is the probability of this action actually making money
    'Get a part time job': { 'Money': -20, 'Energy': 30},
    'Get a full time job': { 'Money': -40, 'Energy': 70},
    'Apply for scholarship': { 'Money': -25, 'Energy': 5},
    'Enter competition': { 'Money': -15, 'Energy': 40},
    'Invest in stock market': { 'Money': -50, 'Energy': -5},

    # Energy Focussed
    'Buy ice cream': { 'Money': 1, 'Energy': -5 },
    'Go for a walk': { 'Money': 0, 'Energy': -15 },
    'Relax': { 'Money': 0, 'Energy': -10 },
    'Watch TV': { 'Money': 0, 'Energy': -8 },
    'Go to the bar': { 'Money': 2, 'Energy': -20 },
    'Go on holiday': { 'Money': 6, 'Energy': -80 }
}

probability = {
    'Sell unused belongings': 0.6,
    'Get a part time job': 0.7,
    'Get a full time job': 0.3,
    'Apply for scholarship': 0.37,
    'Enter competition': 0.3,
    'Invest in stock market': 0.25,
    'Buy ice cream': 0.75,
    'Go for a walk': 0.75,
    'Relax': 0.8,
    'Watch TV': 0.5,
    'Go to the bar': 0.3,
    'Go on holiday': 0.4
}

import random

def apply_action(action):
    '''Change all goal values using this action. An action can change multiple
    goals (positive and negative side effects).
    Negative changes are limited to a minimum goal value of 0.
    '''
    for goal, change in actions[action].items():
        goals[goal] = max(goals[goal] + change, 0)

def action_success(action):
    '''returns true or false whether the action succeeded.
    
    each action has an assigned probability of success (Ln 56).
    if a random number is above that, the action was a success so the 'money' goal 
    will be affected.
    '''
    
    attempt = random.uniform(0, 1) # A random number that represents the attempt
    if attempt < probability[action]:
        return True
    return False

def get_othergoal(current_goal):
    for goal, value in goals.items():
        if goal != current_goal:
            return goal
    return None

def determine_canafford(action):
    ''' returns a string of the goal that is not the best goal
    used to calculate utility by considering the negative affect
    ***ONLY WORKS FOR EXACTLY 2 GOALS
    '''

    canafford = True
    for g,v in goals.items():
            if canafford and v + actions[action][g] > 200: # value here (500) is the maximum value for both goals => i.e. money and energy cannot exceed 200
                canafford = False
    return canafford

def action_utility(action, goal):
    '''Return the 'value' of using "action" to achieve "goal".
    
    Extension
      - return a higher utility for actions that don't change our goal past zero
      and/or
      - take any other (positive or negative) effects of the action into account
        (you will need to add some other effects to 'actions')
    '''
    if action_success(action):
        othergoal = get_othergoal(goal)
        if determine_canafford(action):
            if actions[action][othergoal] == 0:
                return -actions[action][goal]/1 # Necessary to avoid divide by zero error
            else:
                return -actions[action][goal]/actions[action][othergoal]
    return 0

def get_mostinsistent():
    best_goal = None
    for key, value in goals.items():
        if best_goal is None or value > goals[best_goal]:
            best_goal = key
    return best_goal

def choose_action():
    # Find the most insistent goal:
    best_goal = get_mostinsistent()

    if VERBOSE: print('BEST_GOAL:', best_goal, goals[best_goal])

    # Find the best (highest utility) action to take.
    best_action = None
    best_utility = None
    for key, value in actions.items():
        # Note, at this point:
        #  - "key" is the action as a string,
        #  - "value" is a dict of goal changes (see line 35)

        # Does this action change the "best goal" we need to change?
        if best_goal in value:
            # Do we currently have a "best action" to try? If not, use this one
            if best_action is None:
                ### 1. store the "key" as the current best_action
                best_action = key
                ### 2. use the "action_utility" function to find the best_utility value of this best_action
                best_utility = action_utility(best_action,best_goal)

            # Is this new action better than the current action?
            else:
                ### 1. use the "action_utility" function to find the utility value of this action
                utility = action_utility(key,best_goal)
                ### 2. If it's the best action to take (utility > best_utility), keep it! (utility and action)
                if utility > best_utility:
                    best_utility = utility
                    best_action = key

    # Return the "best action"
    return best_action


#==============================================================================

def print_actions():
    print('ACTIONS:')
    # for name, effects in list(actions.items()):
    #     print(" * [%s]: %s" % (name, str(effects)))
    for name, effects in actions.items():
        print(" * [%s]: %s" % (name, str(effects)))


def run_until_all_goals_zero():
    HR = '-'*40
    print_actions()
    print('>> Start <<')
    print(HR)
    running = True
    while running:
        print('GOALS:', goals)
        # What is the best action
        action = choose_action()
        print('BEST ACTION:', action)
        # Apply the best action
        apply_action(action)
        print('NEW GOALS:', goals)
        # Stop?
        if all(value == 0 for goal, value in goals.items()):
            running = False
        print(HR)
    # finished
    print('>> Done! <<')


if __name__ == '__main__':
    print(actions)
    print(actions.items())
    for k, v in actions.items():
        print(k,v)
    print_actions()

    run_until_all_goals_zero()


