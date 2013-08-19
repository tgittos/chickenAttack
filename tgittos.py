import actions
import math

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
        self.chicken_actions = {}
        self.orders = {}
        self.width = len(money_payout_rates)
        self.height = len(money_payout_rates[0])


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

        # print("Enemies: {}".format(enemies))
        # print("Friendlies: {}".format(friendlies))


        # on each move, track each chicken's last position, current orders and it's action
            # determine if any chickens died and mark their targets available (if no other chicken monitors it), clear their orders
            # determine if chickens attacking hostile targets need to boost numbers
                # if so, call nearest chicken in as reinformcement

        # for each chicken, if it doesn't have orders, give it orders
            # calculate the best target that is available
            # build a path to the target
            # mark the target as unvailable
            # if the target is held by enemy chickens, dispatch enough chickens to win the target
        
        # if it does have orders
            # if it hasn't reached the target, follow orders
            # if it has, noop

        # monitor enemy chicken movements.
            # determine if enemy chickens are approaching a held target
            # if so, find furthest possible chicken and order as reinforcement
            # if no reinforcements can make it, find next desirable target and path to it, becomes new orders

        # if a chicken is called in as a reinforcement, mark its spot vacant

        # --------------------------------------

        # first, lets take our chickens and apply their orders, to see if they are where we expect them
        existing_friendlies = {}
        for order_key in list(self.chicken_actions.keys()): # Python 3 compatability
            # order_key[0] = pos, #order_key[1] = action
            new_x, new_y = actions.next_pos(order_key[0], order_key[1])
            existing_friendlies[(new_x, new_y)] = self.chicken_actions[order_key]

        # print("Existing friendlies: {}".format(existing_friendlies))

        dead_chickens = {}
        new_chickens = {}

        for key in list(existing_friendlies.keys()):
            if not key in friendlies:
                dead_chickens[key] = existing_friendlies[key]
            else:
                delta = friendlies[key] - existing_friendlies[key]
                if (delta > 0):
                    new_chickens[key] = delta
                elif (delta < 0):
                    dead_chickens[key] = delta

        # print("Dead chickens: {}".format(dead_chickens))
        print("New chickens: {}".format(new_chickens))

        # give new chickens a set of orders
        for key in list(new_chickens.keys()):
            x, y = key
            num = new_chickens[key]
            print("{} chickens at {}".format(num, (x, y)))
            food = True
            for i in range(num):
                if food:
                    targets = self.high_food_targets
                else:
                    targets = self.high_money_targets
                # print("Selecting target from: {}".format(targets))
                available = [target for target in targets.items() if not target[1][1]][0]
                print("Next target: {}".format(available))
                self.high_food_targets[available[0]] = (available[1][1], True)
                print("Generating a* from {} to {}".format((x,y), available[0]))
                plan = self.astar((x, y), available[0])
                print("Plan: {}".format(plan))
                food = not food

        # translate orders into actions
        self.chicken_actions = {}
        for key in list(friendlies.keys()):
            x, y = key
            num = friendlies[key]

            for i in range(num):
                key = ((x, y), actions.ALL_ACTIONS[i % len(actions.ALL_ACTIONS)])
                if key not in self.chicken_actions:
                    self.chicken_actions[key] = 1
                else:
                    self.chicken_actions[key] += 1

        # print("Orders: {}".format(self.chicken_actions))

        return self.chicken_actions

    def get_guys(self, guys, friendlies):
        filtered_guys = {}
        for x in range(0, len(guys)):
            for y in range(0, len(guys[x])):
                if not guys[x][y]: continue
                num_guys, is_mine = guys[x][y]
                if is_mine == friendlies: continue
                if (x, y) not in list(filtered_guys.keys()):
                    filtered_guys[(x, y)] = guys[x][y][0]
                else:
                    filtered_guys[(x, y)] += guys[x][y][0]
        return filtered_guys

    def get_high_money_targets(self, map):
        # temporarily short-cut this
        return self.flatten_map(map)
        # return sorted(self.flatten_map(map).items(), key=lambda t: t[1][0])

    def get_high_food_targets(self, map):
        # temporarily short-cut this
        return self.flatten_map(map)
        # return sorted(self.flatten_map(map).items(), key=lambda t: 1-t[1][0])

    def flatten_map(self, map):
        flattened = {}
        for x in range(0, len(map)):
            for y in range(0, len(map[x])):
                flattened[(x, y)] = (map[x][y], False)
        return flattened

    def astar(self, start_pos, finish_pos):
        # print("start_pos: {}, finish_pos: {}".format(start_pos, finish_pos))
        # node format: ((g_score, h_score), point, parent)
        start_node = ((0, self.astar_hscore(start_pos, finish_pos)), start_pos, None)
        # print("start_node: {}".format(start_node))
        open = [start_node]
        open_coords = [start_pos]
        closed = []
        closed_coords = []
        while(len(open) > 0):
            open.sort(key = lambda node: node[0][0] + node[0][1])
            # print ("sorted open list: {}".format([(sum(n[0]), n[1]) for n in open]))
            node = open.pop(0)
            node_pos = node[1]
            node_gscore = node[0][0]
            # print("node_pos: {}, node_gscore: {}".format(node_pos, node_gscore))
            closed.append(node)
            closed_coords.append(node_pos)
            if node_pos == finish_pos:
                # print("found finish_pos")
                break
            # print("searching adjacent nodes")
            for delta_pos in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                # print("delta_pos: {}".format(delta_pos))
                adj_pos = tuple([sum(pair) for pair in zip(delta_pos, node_pos)])
                # don't consider nodes that are off the map!
                if (adj_pos[0] > self.width) or (adj_pos[0] < 0) or (adj_pos[1] > self.height) or (adj_pos[1] < 0): continue
                # print("adj_pos: {}".format(adj_pos))
                if adj_pos in closed_coords: continue
                if adj_pos in open_coords:
                    continue
                else:
                    open_coords.append(adj_pos)
                    open.append((self.astar_fscore(node_pos, node_gscore, adj_pos, finish_pos), adj_pos, node))
        # walk the path from the finish, back to the start
        path = []
        node = closed.pop()
        while(node[2] != None):
            path.append(node)
            node = node[2]
        # collect just the positions
        path.reverse()
        return [node[1] for node in path]

    def astar_fscore(self, current_pos, current_gscore, next_pos, finish_pos):
        # print("calculating a* fscore")
        return (self.astar_gscore(current_pos, current_gscore, next_pos), self.astar_hscore(next_pos, finish_pos))
    
    def astar_gscore(self, current_pos, current_gscore, next_pos):
        # print("calculating a* gscore")
        delta = abs(next_pos[0] - current_pos[0]) + abs(next_pos[1] - current_pos[1])
        return current_gscore + delta * 1

    def astar_hscore(self, next_pos, finish_pos):
        # print("calculating a* hscore")
        return abs(finish_pos[0] - next_pos[0]) + abs(finish_pos[1] - next_pos[1])

    def get_closest(self, list, target):
        return sorted([get_distance(item, target) for item in list])

    def get_distance(self, pos, target):
        # print("Getting distance between {} and {}".format(pos, target))
        return math.sqrt((pos[0] - target[0]) ** 2 + (pos[1] - target[1]) ** 2)
