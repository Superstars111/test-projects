# This is my very first program in Python. It's inspired by the redstone contraption I first learned how to build
# in Minecraft. The idea was that no matter what four digits you pressed, the door would open. But unless you entered
# the correct combination, the trap would trigger and kill you.

import re
motion = ("walk", "run", "move", "stroll", "sprint", "go", "waddle")
north = ("north", "up")
south = ("south", "down")
east = ("east", "right")
west = ("west", "left")
s_desc = ["The room you started in. There are four corridors, one for each cardinal direction.",
          "This room is a large and empty circle. Sunlight filters down from a hole high above you. "
          "That's probably where you fell down. Four ornate doorposts can be seen along the walls, "
          "one for each cardinal direction."]
s_vis = ["*-\"-*", "|   |", "=   =", "|   |", "*-\"-*"]
u_desc = ["The northern room. There is a keypad on the wall, and a door to the south.",
          "A single torch lights this room. It is small, enough that only a few people could stand here comfortably" 
          "at a time. On the northern wall there is a small, 9-digit keypad next to an indent in the shape of a door."]
u_vis = ["*---*", "|   |", "|   |", "|   |", "*-\"-*"]
d_desc = ["The southern room. It contains a bed and a chest. There is a door to the north.",
          "This room is quite cozy. The floor is carpeted, and there is a bed in the corner. Posters hang on the" 
          "walls, a small chest sits at the foot of the bed."]
d_vis = ["*-\"-*", "|   |", "|   |", "|   |", "*---*"]
l_desc = ["The western room. A grand hall with a door to the east.",
          "This room is a grand hall, built from marble with massive pillars reaching to the ceiling. Hundreds of" 
          "torches line the walls, and dozens of great banquet tables fill the room. Each one is set as if it has" 
          "been prepared ahead of time, and recently. At the east is the door you came from, and at the head of" 
          " the room opposite that there is a massive throne."]
l_vis = ["*---*", "|   |", "|   =", "|   |", "*---*"]
r_desc = ["The eastern room. A passage lies to the west, and a locked gate is to the east.",
          "This long room is almost like a hallway itself, if it weren't far too wide for that. At the far eastern" 
          "end of the room is a massive gate. An enormous lock is bolting it shut. Through the bars you can see" 
          "nothing but darkness. The door you came from is to the west."]
r_vis = ["*---*", "|   |", "=   |", "|   |", "*---*"]


class Location:
    occupied = False
    explored = False

    def __init__(self, n=True, s=True, e=True, w=True):
        self.n_passable = n
        self.s_passable = s
        self.e_passable = e
        self.w_passable = w


class Room(Location):
    def __init__(self, desc, visual, loot=None):
        super().__init__()
        self.loot = loot
        self.short_description = desc[0]
        self.long_description = desc[1]
        self.visual = visual

    def __str__(self):
        return self.long_description


class Wall(Location):
    def __init__(self, n=False, s=False, e=False, w=False):
        super().__init__(n, s, e, w)
        self.visual = ["*---*", "|   |", "|   |", "|   |", "*---*"]


class Player:
    inventory = []


class Map:
    rooms = [
        [Wall(), Wall(), Wall(), Wall(), Wall()],
        [Wall(), Wall(), Room(u_desc, u_vis), Wall(), Wall()],
        [Wall(), Room(l_desc, l_vis), Room(s_desc, s_vis), Room(r_desc, r_vis), Wall()],
        [Wall(), Wall(), Room(d_desc, d_vis), Wall(), Wall()],
        [Wall(), Wall(), Wall(), Wall(), Wall()]
        ]
    current = rooms[2][2]
    coords = [2, 2]

    def move(self, coords):
        row, col = coords[0], coords[1]

        if action[min(1, len(action) - 1)] in north:
            if not self.rooms[row-1][col].s_passable and self.current.n_passable:
                print("You have hit a wall and cannot go this way.")
            else:
                self.current.occupied = False
                self.current = self.rooms[row-1][col]
                self.coords = [row-1, col]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)

        elif action[min(1, len(action) - 1)] in south:
            if not self.rooms[row+1][col].n_passable and self.current.s_passable:
                print("You have hit a wall and cannot go this way.")
            else:
                self.current.occupied = False
                self.current = self.rooms[row+1][col]
                self.coords = [row+1, col]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)

        elif action[min(1, len(action) - 1)] in west:
            if not self.rooms[row][col-1].e_passable and self.current.w_passable:
                print("You have hit a wall and cannot go this way.")
            else:
                self.current.occupied = False
                self.current = self.rooms[row][col-1]
                self.coords = [row, col-1]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)

        elif action[min(1, len(action) - 1)] in east:
            if not self.rooms[row][col+1].w_passable and self.current.e_passable:
                print("You have hit a wall and cannot go this way.")
            else:
                self.current.occupied = False
                self.current = self.rooms[row][col+1]
                self.coords = [row, col+1]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)

        else:
            print("Invalid direction")

    def view_map(self):
        for row in self.rooms:
            for i in range(5):
                for room in row:
                    if room.explored:
                        print(room.visual[i], end="")
                    else:
                        print("#####", end="")
                print()


if __name__ == "__main__":
    game = Map()
    x = True
    game.current.occupied = True
    game.current.explored = True
    print(game.current)
    while x:
        action = re.split(r"\s", input("What would you like to do? ").lower())
        if action[0] in motion:
            game.move(game.coords)
        elif action[0] == "map":
            game.view_map()


# print("Welcome to my RPG test game! You are standing next to a door with a nine-digit keypad.")
# counter = 0
# code = [1, 2, 3, 4]
# for digit in code:
#     i = int(input("Please enter a digit. \n"))
#     if i == digit:
#         print("You hear a chime.")
#         counter += 1
#     else:
#         print("You hear a beep.")
# if counter == 4:
#     print("The door opens. You walk through and get the treasure. Congratulations!")
# else:
#     print("The door opens. You see treasure at the end of the hall and eagerly run towards it."
#           "Suddenly, the floor opens up beneath you! It was rigged! You plummet to your death. Game over.")
