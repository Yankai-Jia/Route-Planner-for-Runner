import math
class Node():

    def __init__(self, parent=None, position=None):
        self.position = position
        self.parent = parent

        self.g = 0
        self.h = 0
        self.f = 0
        self.DD = 0
        self.Rate = 0

        # self.preRate = 0
        self.cycleRate = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(map, start, end, length):
    """Returns a list of tuples as a path from the given start to the given end in the given map"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = start_node.DD = start_node.Rate = start_node.preRate = start_node.cycleRate = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = end_node.DD = end_node.Rate = end_node.preRate = end_node.cycleRate = 0

    # Initialize open list in which we store adjacent nodes of the current node
    open_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    t = 0
    route_length = 0
    while len(open_list) > 0:
    # while True:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        print("----------------current node---------: ",current_node.position)

        # Clean the open_list
        open_list = []

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                if current.parent:
                    route_length += math.sqrt(((current.position[0] - current.parent.position[0]) ** 2) + ((current.position[1] - current.parent.position[1]) ** 2))
                current = current.parent
            if route_length >= length:
                return path[::-1] # Return reversed path

        # Generate children, find the adjacent node for the current node.
        children = []
        direction = map[current_node.position][1:]
        i = 1
        if 1 not in direction:
            while True:
                if (current_node.position[0]-i,current_node.position[1]) not in map:
                    i += 1
                    continue
                else:
                    new_node = Node(current_node, (current_node.position[0]-i,current_node.position[1]))
                    children.append(new_node)
                    i = 1
                    break
        if 2 not in direction:
            while True:
                if (current_node.position[0],current_node.position[1]+i) not in map:
                    i += 1
                    continue
                else:
                    new_node = Node(current_node, (current_node.position[0],current_node.position[1]+i))
                    children.append(new_node)
                    i = 1
                    break
        if 3 not in direction:
            while True:
                if (current_node.position[0]+i,current_node.position[1]) not in map:
                    i += 1
                    continue
                else:
                    new_node = Node(current_node, (current_node.position[0]+i,current_node.position[1]))
                    children.append(new_node)
                    i = 1
                    break
        if 4 not in direction:
            while True:
                if (current_node.position[0],current_node.position[1]-i) not in map:
                    i += 1
                    continue
                else:
                    new_node = Node(current_node, (current_node.position[0],current_node.position[1]-i))
                    children.append(new_node)
                    i = 1
                    break

        # Loop through children
        for child in children:
            print(current_node.position,"'s child is",child.position)

            # Create the f, g, and h values
            if child.position[0] == current_node.position[0]:
                child.g = current_node.g + abs(child.position[1] - current_node.position[1])
            if child.position[1] == current_node.position[1]:
                child.g = current_node.g + abs(child.position[0] - current_node.position[0])


            child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            child.DD = abs((child.g + child.h - length))
            # child.preRate = (map[child.position][0]+ current_node.preRate) / 2

            cycle_count  = cycleRateSum = 0
            for node in map:
                if node[0]>=min(child.position[0],end_node.position[0]) and node[0] <= max(child.position[0],end_node.position[0]) and node[1]>=min(child.position[1],end_node.position[1]) and node[1] <= max(child.position[1],end_node.position[1]):
                    cycleRateSum += map[node][0]
                    cycle_count += 1
            print("cycle_count",cycle_count)
            child.cycleRate = cycleRateSum / cycle_count
            child.Rate = child.cycleRate
            child.f = child.DD * child.Rate
            # print(child.position,child.f,child.g,child.h,child.cycleRate, child.Rate)
            print(child.f,child.position)


            # Add the child to the open list
            open_list.append(child)

        t += 1
        print('test', t)
        print(current_node.g,"current_node.g")


def main():

    # Every conner of the street are sotred in a hash map: (x,y):[crimeRate, fork of the corner].
    # key is the coordination of the corner (x,y).
    # For fork of the corner, 0 means it's a normal corner, have 4 fork. 1 means it does not have west fork. 2 - north, 3 - east, 4 - south.
    map = {(0,0):[0.1,0], (2,0):[0.1,4], (-1,0):[0.2,1], (4,0):[0.2,4], (5,0):[0.2,2,3], (0,3):[0.1,1], (0,4):[0.2,2], (0,-1):[0.2,3], (0,-3):[0.1,4], (-1,4):[0.1,1,2], (-1,-1):[0.2,1], (-1,-3):[0.1,1,4], (2,3):[0.1,2], (4,3): [0.1,3],(4,4):[0.1,2,3],(5,-3):[0.1,3,4]}

    start = (0, 0)
    end = (5, -3)
    length = 40

    path = astar(map, start, end, length)
    print("An optimal route for running start from", start,"to", end, "with length of", length,"is: \n",path)


if __name__ == '__main__':
    main()
