from tgittos import Player
from map import Map

start_pos = (1, 1)
end_pos = (15, 5)

m = Map()
p = Player(*m.constructor_data_for_p1())
plan = p.astar(start_pos, end_pos)

print("A* plan from {} to {}: {}".format(start_pos, end_pos, plan))