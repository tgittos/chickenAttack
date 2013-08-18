import actions

class Player:

    #Get passed all the board information that never changes throughout the game.
    #It is recommended that you store these in member variables since you will probably need to look at them later.
    # PARAMS:

    #  money_payout_rates:
    #   This is a 50x50 2D array of floats between 0.0 and 1.0 that tell your bot how money per turn this spot produces
    #   Food production is the inverse of money production and follow the formula food_payout_rate = 1.0 - money_payout_rate
    #   This means areas that produce a lot of money, produce less food

    #  my_spawn_point:
    #   An (x, y) tuple of where your new chickens will hatch each turn

    #  their_spawn_point:
    #   An (x, y) tuple of where your opponent's chickens will hatch each turn
    def __init__(self, money_payout_rates, my_spawn_point, their_spawn_point):
        self.money_payout_rates = money_payout_rates,
        self.my_spawn_point = my_spawn_point
        self.their_spawn_point = their_spawn_point
        self.high_money_targets = self.get_high_money_targets(money_payout_rates)
        self.high_food_targets = self.get_high_food_targets(money_payout_rates)


    # Gets called each turn and where you decide where your chickens will go
    # PARAMS:

    #   guys:
    #       A 50x50 2D matrix showing where all the guys are on the board.
    #       An entry of 'None' indicates an unoccupied spot.
    #       A space with chickens will be an object with "num_guys" and "is_mine" properties.
    #

    #   my_food:
    #       A float showing how much food you have left over from last turn.

    #   their_food:
    #       A float showing how much food your opponent has left over from last run.

    #   my_money:
    #       A float showing how much money you will earn at market so far

    #   their_money:
    #       A float showing how much money your opponent will earn at market so far

    # RETURN:
    #   a python dict that takes a tuple ((x_pos, y_pos), direction) as a key and the number of guys to move as the value.
    #   direction is defined in action.py

    # STRATEGY:
    #   Attempt to capture high value targets, namely squares that are worth
    #   the most money and the most food.
    #   Favor food over money, so that we can build a larger population and
    #   overwhelm the enemy
    #   If we have more chickens, be aggressive
    #   Only attack a position if we know we're going to get it
    #   If we don't, be evasive

    def take_turn(self, guys, my_food, their_food, my_money, their_money):
        friendlies = self.get_guys(guys, False)
        enemies = self.get_guys(guys, True)

        # if len(enemies) > 0: print("Enemies: {}".format(enemies))
        # if len(friendlies) > 0: print("Friendlies: {}".format(friendlies))

        orders ={}
        for chicken in friendlies:
            x, y, num = chicken

            for i in range(num):
                key = ((x, y), actions.ALL_ACTIONS[i % len(actions.ALL_ACTIONS)])
                if key not in orders:
                    orders[key] = 1
                else:
                    orders[key] += 1

        return orders



    def get_guys(self, guys, friendlies):
        filtered_guys = []
        for x in range(0, len(guys)):
            for y in range(0, len(guys[x])):
                if not guys[x][y]: continue
                num_guys, is_mine = guys[x][y]
                if is_mine == friendlies: continue
                filtered_guys.append([x, y, guys[x][y][0]])
        return filtered_guys

    def get_high_money_targets(self, map):
        return sorted(self.flatten_map(map), key=lambda t: t[2])

    def get_high_food_targets(self, map):
        return sorted(self.flatten_map(map), key=lambda t: 1-t[2])

    def flatten_map(self, map):
        flattened = []
        for x in range(0, len(map)):
            for y in range(0, len(map[x])):
                flattened.append([x, y, map[x][y]])
        return flattened

    #def astar():

    def get_closest(list, target):
        return sorted([get_distance(item, target) for item in list])

    def get_distance(pos, target):
        return math.sqrt((pos[0] + target[0]) ** 2 + (pos[1] + target[1]) ** 2)
