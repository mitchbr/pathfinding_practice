from math import sqrt

from matplotlib import colors
from matplotlib import pyplot as plt


def calc_h_cost(x, y):
    return sqrt((goal[0] - x) ** 2 + (goal[1] - y) ** 2)


def calc_g_cost(parent_coords, child_coords, curr_cost):
    return curr_cost + sqrt(
        (parent_coords[0] - child_coords[0]) ** 2
        + (parent_coords[1] - child_coords[1]) ** 2
    )


def min_f(nodes):
    min_key = None
    for key in nodes.keys():
        if min_key is None:
            min_key = key

        if nodes[key]["f"] < nodes[min_key]["f"]:
            min_key = key

    return min_key


def key_gen(x, y):
    return str(x) + str(y)


plt.ion()

# Set up the maze
maze_x = list(range(12))
maze_y = list(range(12))
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

cmap = colors.ListedColormap(["white", "black", "green", "blue", "red"])
graph = plt.pcolor(maze_x, maze_y, maze, cmap=cmap, edgecolors="k", linewidths=1)
plt.pause(3)

# Set up A*
goal = [10, 10]
origin_h_cost = calc_h_cost(1, 1)
origin_f_cost = origin_h_cost + 0
open_nodes = {
    "11": {
        "f": origin_f_cost,
        "h": origin_h_cost,
        "g": 0,
        "coords": [1, 1],
        "parent": None,
    }
}
nodes = {"11": {"parent": None}}
closed_nodes = []

# Run A*
while open_nodes:
    curr = open_nodes.pop(min_f(open_nodes))
    closed_nodes.append(curr["coords"])
    nodes[key_gen(curr["coords"][0], curr["coords"][1])] = {
        "parent": curr["parent"],
        "coords": curr["coords"],
    }
    maze[curr["coords"][0]][curr["coords"][1]] = 4
    if curr["coords"] == goal:
        break

    for x in range(curr["coords"][0] - 1, curr["coords"][0] + 2):
        for y in range(curr["coords"][1] - 1, curr["coords"][1] + 2):
            if [x, y] in closed_nodes:
                continue
            h_cost = calc_h_cost(x, y)
            g_cost = calc_g_cost(curr["coords"], [x, y], curr["f"])
            f_cost = h_cost + g_cost
            if (
                key_gen(x, y) not in open_nodes.keys()
                or g_cost < open_nodes[key_gen(x, y)]["g"]
            ) and maze[x][y] != 1:
                open_nodes[key_gen(x, y)] = {
                    "f": f_cost,
                    "h": h_cost,
                    "g": g_cost,
                    "coords": [x, y],
                    "parent": curr["coords"],
                }
                maze[x][y] = 3

    graph.remove()

    graph = plt.pcolor(maze_x, maze_y, maze, cmap=cmap, edgecolors="k", linewidths=1)
    plt.pause(0.1)


# Plot the path from end to start
curr = nodes["1010"]
while curr is not None:
    maze[curr["coords"][0]][curr["coords"][1]] = 2
    graph = plt.pcolor(maze_x, maze_y, maze, cmap=cmap, edgecolors="k", linewidths=1)
    plt.pause(0.1)
    if curr["parent"] is None:
        break
    curr = nodes[key_gen(curr["parent"][0], curr["parent"][1])]
graph = plt.pcolor(maze_x, maze_y, maze, cmap=cmap, edgecolors="k", linewidths=1)
plt.pause(120)
