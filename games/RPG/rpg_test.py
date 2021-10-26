# This is my very first program in Python. It's inspired by the redstone contraption I first learned how to build
# in Minecraft. The idea was that no matter what four digits you pressed, the door would open. But unless you entered
# the correct combination, the trap would trigger and kill you.
# Working title: "Snakes in a Cave"

import re
import json
with open("C:\\Users\\jared\\Desktop\\Tech_Stuff\\Python_Learning\\RPG\\gamedata.json", "r") as gamedata:
    data = json.load(gamedata)
# motion = ("walk", "run", "move", "stroll", "sprint", "go", "waddle", "head")
# take = ("take", "loot", "grab", "steal")
# observe = ("look", "check", "view", "examine", "read", "study")
# space = ("room", "area", "location", "place", "space", "surroundings")
# bag = ("bag", "backpack", "inventory", "pocket", "pockets", "satchel")
# usage = ("use", "utilize", "activate")
# emote = ("dance", "sing", "frolic", "daydream", "draw", "paint")
# controls = ("controls", "commands", "help")
# north = ("north", "up")
# south = ("south", "down")
# east = ("east", "right")
# west = ("west", "left")
# forward = ("forward", "forth", "ahead", "onward")
# backward = ("back", "backward", "reverse")
# stairs = ("stairs", "upstairs", "downstairs")
# s_desc = ["The room you started in. There are four corridors, one for each cardinal direction.",
#           "This room is a large and empty circle. Sunlight filters down from a hole high above you. "
#           "That's probably where you fell down. Four ornate doorposts can be seen along the walls, "
#           "one for each cardinal direction."]
# s_vis = ["*---\"---*", "|       |", "=       =", "|       |", "*---\"---*"]
# u_desc = ["The northern room. There is a keypad on the wall, and a door to the south.",
#           "A single torch lights this room. It is small, enough that only a few people could stand here comfortably "
#           "at a time. On the northern wall there is a small, 9-digit keypad next to an indent in the shape of a door."]
# u_vis = ["*-------*", "|       |", "|       |", "|       |", "*---\"---*"]
# d_desc = ["The southern room. It contains a bed and a chest. There is a door to the north.",
#           "This room is quite cozy. The floor is carpeted, and there is a bed in the corner. Posters hang on the "
#           "walls, a small chest sits at the foot of the bed."]
# d_vis = ["*---\"---*", "|       |", "|       |", "|       |", "*-------*"]
# l_desc = ["The western room. A grand hall with a door to the east.",
#           "This room is a grand hall, built from marble with massive pillars reaching to the ceiling. Hundreds of "
#           "torches line the walls, and dozens of great banquet tables fill the room. Each one is set as if it has "
#           "been prepared ahead of time, and recently. At the east is the door you came from, and at the head of "
#           " the room opposite that there is a massive throne."]
# l_vis = ["*-------*", "|       |", "|       =", "|       |", "*-------*"]
# r_desc = ["The eastern room. A passage lies to the west, and a locked gate is to the east.",
#           "This long room is almost like a hallway itself, if it weren't far too wide for that. At the far eastern "
#           "end of the room is a massive gate. An enormous lock is bolting it shut. Through the bars you can see "
#           "nothing but darkness. The door you came from is to the west."]
# r_vis = ["*-------*", "|       |", "=       =", "|       |", "*-------*"]
# dun_desc = ["The dungeon. You used your key to get here.",
#             "Beyond the gate lies an enormous dungeon. Massive chains hang from the walls, all shattered. Beneath "
#             "them, huge shackles lie on the ground, far too large to hold any human. The walls are scarred with "
#             "gashes and scorch marks."]
# dun_vis = ["*-------*", "|       |", "=       |", "|       |", "*-------*"]
# key = {
#     "name": "key",
#     "code": 1,
#     "reusable": False,
#     "desc": "A large metal key. It looks exactly like the default key you would see in any low-effort adventure game."
# }
# gate = {
#     "name": "gate",
#     "code": 1,
#     "effect": 1,
#     "desc": "An enormous iron gate. It looks like it was built to contain something dangerous. ...Either that, or just "
#             "to look impressive. Could be either."
# }
# lever = {
#     "name": "lever",
#     "effect": 2,
#     "desc": "It appears to be an old lever. Who knows what it does?"
# }


# Unfinished help function
def game_help():
    print("Welcome! My name is Jared. I built this text-based RPG for practicing Python. I've tried to make it\n"
          "intuitive, but there are limitations in both the program and my understanding, so please forgive me if\n"
          "something doesn't work.\n"
          "In order to play, you'll type in a command when prompted. These can be simple things like \"walk\" or\n"
          "\"look,\" and will usually be paired with a target. For example, \"walk north.\" I've tried to include\n"
          "as much flexibility as I can. So for example, \"go left\" and \"move west\" will both be understood by\n"
          "the computer, and will do the same thing. In some situations, you can also add grammatical syntax to your\n"
          "commands. So \"check surroundings\" is valid, but so is \"look around the room.\"\n"
          "You can get back to this page at any time by typing \"help,\" but since you're here, I figure you already\n"
          "knew that.\n"
          "My goal is to make it so that you can intuitively do whatever you'd like (within reason), so ideally you\n"
          "won't need a list of commands. However, if you'd like one, you can type \"list\" now. Otherwise, you can\n"
          "type \"done\" to get back to the game.")
    com_list = input(">> ").lower()
    if com_list in ("ls", "list"):
        pass


class Location:
    occupied = False
    explored = False

    def __init__(self, n=False, s=False, e=False, w=False, us=False, ds=False):
        self.n_passable = n
        self.s_passable = s
        self.e_passable = e
        self.w_passable = w
        self.upstairs = us
        self.downstairs = ds


class Room(Location):
    def __init__(self, desc, visual, loot=None, features=None, n=False, s=False, e=False, w=False, us=False, ds=False):
        super().__init__(n, s, e, w, us, ds)
        self.loot = loot
        self.features = features
        self.short_description = desc[0]
        self.long_description = desc[1]
        self.visual = visual

    def __str__(self):
        return self.long_description


class Wall(Location):
    short_description = "A wall"
    long_description = "A wall. How the heck did you even get in here?"
    features = None
    loot = None

    def __init__(self):
        super().__init__()
        self.visual = ["*-----*", "|-----|", "|-----|", "|-----|", "*-----*"]

    def __str__(self):
        return self.long_description


class Player:
    inventory = []


class Map:
    floor1 = [
        [Wall(), Wall(), Wall(), Wall(), Wall()],
        [Wall(), Wall(), Room(data["u_desc"], data["u_vis"], s=True), Wall(), Wall()],
        [Wall(), Room(data["l_desc"], data["l_vis"], e=True), Room(data["s_desc"], data["s_vis"], n=True, s=True, e=True, w=True),
         Room(data["r_desc"], data["r_vis"], features=[data["gate"]], w=True), Room(data["dun_desc"], data["dun_vis"], w=True, ds=True)],
        [Wall(), Wall(), Room(data["d_desc"], data["d_vis"], loot=[data["key"]], n=True), Wall(), Wall()],
        [Wall(), Wall(), Wall(), Wall(), Wall()]
        ]
    floor2 = [
        [Wall(), Wall(), Wall(), Wall(), Wall()],
        [Wall(), Wall(), Room(data["u_desc"], data["u_vis"], s=True), Wall(), Wall()],
        [Wall(), Room(data["l_desc"], data["l_vis"], e=True), Room(data["s_desc"], data["s_vis"], n=True, s=True, e=True, w=True),
         Room(data["r_desc"], data["r_vis"], features=[data["gate"]], w=True), Room(data["dun_desc"], data["dun_vis"], w=True, us=True)],
        [Wall(), Wall(), Room(data["d_desc"], data["d_vis"], loot=[data["key"]], n=True), Wall(), Wall()],
        [Wall(), Wall(), Wall(), Wall(), Wall()]
        ]

    current = floor1[2][2]
    previous = floor1[2][2]
    coords = [2, 2, 0]
    prev_coords = [2, 2, 0]
    floors = [floor1, floor2]
    current_floor = floors[0]
    previous_floor = floors[0]

    def move(self):
        row, col, layer = self.coords[0], self.coords[1], self.coords[2]

        if action[-1] in data["stairs"]:
            if self.current.upstairs and self.floors[layer-1][row][col].downstairs:
                self.current.occupied = False
                self.previous = self.current
                self.current = self.floors[layer-1][row][col]
                self.previous_floor = self.current_floor
                self.current_floor = self.floors[layer-1]
                self.prev_coords = self.coords
                self.coords = [row, col, layer-1]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)

            elif self.current.downstairs and self.floors[layer+1][row][col].upstairs:
                self.current.occupied = False
                self.previous = self.current
                self.current = self.floors[layer+1][row][col]
                self.previous_floor = self.current_floor
                self.current_floor = self.floors[layer+1]
                self.prev_coords = self.coords
                self.coords = [row, col, layer+1]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)

        elif action[min(1, len(action) - 1)] in data["north"]:
            if self.current.n_passable and self.current_floor[row - 1][col].s_passable:
                self.current.occupied = False
                self.previous = self.current
                self.current = self.current_floor[row - 1][col]
                self.prev_coords = self.coords
                self.coords = [row-1, col, layer]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)
            else:
                print("You have hit a wall and cannot go this way.")

        elif action[min(1, len(action) - 1)] in data["south"]:
            if self.current.s_passable and self.current_floor[row + 1][col].n_passable:
                self.current.occupied = False
                self.previous = self.current
                self.current = self.current_floor[row + 1][col]
                self.prev_coords = self.coords
                self.coords = [row+1, col, layer]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)
            else:
                print("You have hit a wall and cannot go this way.")

        elif action[min(1, len(action) - 1)] in data["west"]:
            if self.current.w_passable and self.current_floor[row][col - 1].e_passable:
                self.current.occupied = False
                self.previous = self.current
                self.current = self.current_floor[row][col - 1]
                self.prev_coords = self.coords
                self.coords = [row, col-1, layer]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)
            else:
                print("You have hit a wall and cannot go this way.")

        elif action[min(1, len(action) - 1)] in data["east"]:
            if self.current.e_passable and self.current_floor[row][col + 1].w_passable:
                self.current.occupied = False
                self.previous = self.current
                self.current = self.current_floor[row][col + 1]
                self.prev_coords = self.coords
                self.coords = [row, col+1, layer]
                self.current.occupied = True
                if self.current.explored:
                    print(self.current.short_description)
                else:
                    self.current.explored = True
                    print(self.current)
            else:
                print("You have hit a wall and cannot go this way.")

        elif action[min(1, len(action) - 1)] in data["backward"]:
            if self.current == self.previous:
                print("You look up towards the hole you fell from. You jump, but it remains out of reach.")
            else:
                self.current.occupied = False
                self.current, self.previous = self.previous, self.current
                self.coords, self.prev_coords = self.prev_coords, self.coords
                self.current_floor, self.previous_floor = self.previous_floor, self.current_floor
                self.current.occupied = True
                print(self.current.short_description)

        else:
            print("You really, really want to do that. But try as you might, you can't think what direction that is.")

    def view_map(self):
        special = 0  # If a special character is printed, this prevents the normal character from printing.
        for row_idx, row in enumerate(self.current_floor):
            for idx, line in enumerate(self.current.visual):  # For each row in the room's visual representation.
                for col_idx, room in enumerate(row):
                    if room.explored:
                        for char in range(len(line)):  # Go through each character individually
                            # Player marker
                            if room.occupied and char == 4 and idx == 2:
                                print("X", end="")
                                special += 1
                            # Eastern gate
                            if self.current_floor[row_idx][min(len(row) - 1, col_idx + 1)] != room:  # Boundary verification
                                if not room.e_passable and self.current_floor[row_idx][col_idx + 1].w_passable \
                                        and char == len(line) - 2 and idx == len(self.current.visual) // 2:
                                    print("+", end="")
                                    special += 1
                            # Western gate
                            if self.current_floor[row_idx][max(0, col_idx - 1)] != room:  # Boundary verification
                                if not room.w_passable and self.current_floor[row_idx][col_idx - 1].e_passable \
                                        and char == 1 and idx == len(self.current.visual) // 2:
                                    print("+", end="")
                                    special += 1
                            # Northern gate
                            if self.current_floor[max(0, row_idx - 1)][col_idx] != room:  # Boundary verification
                                if not room.n_passable and self.current_floor[row_idx - 1][col_idx].s_passable \
                                        and char == len(line) // 2 and idx == 1:
                                    print("+", end="")
                                    special += 1
                            # Southern gate
                            if self.current_floor[min(len(self.current_floor), row_idx + 1)][col_idx] != room:  # Boundary verification
                                if not room.s_passable and self.current_floor[row_idx + 1][col_idx].n_passable \
                                        and char == len(line) // 2 and idx == len(self.current.visual) - 2:
                                    print("+", end="")
                                    special += 1
                            if not special:
                                print(room.visual[idx][char], end="")
                            special = 0
                    else:  # If the room hasn't been explored, don't show it on the map.
                        print("#########", end="")
                print()

    def loot_room(self, item):
        if item == "stairs":
            self.move()
        else:
            if self.current.loot:
                for thing in self.current.loot:
                    if item == thing["name"]:
                        Player.inventory.append(thing)
                        self.current.loot.remove(thing)
                        print(f"You take the {item} and place it in your inventory.")
                    else:
                        print("You searched high and low, but you can't seem to find that object in this room.")
            else:
                print("You searched high and low, but you can't seem to find that object in this room.")

    def examination(self, target):
        if target == "map":
            self.view_map()
        elif target in data["space"]:
            print(self.current)
        elif target in data["bag"]:
            if Player.inventory:
                for item in Player.inventory:
                    print(f"{item['name']}")  # Will likely add additional formatting later. Hence the f-string.
            else:
                print("Your inventory seems to be empty... Wait- is that a pebble!?")
        elif target in data["controls"]:
            game_help()

    def use_item(self):
        tool = {}
        target = {}
        if Player.inventory:
            for item in Player.inventory:
                if item["name"] in action:
                    tool = item
                    if not item["reusable"]:
                        Player.inventory.remove(item)
        if self.current.features:
            for thing in self.current.features:
                if thing["name"] in action:
                    target = thing
        if not tool:
            print("You search through your bag, but you can't seem to find it there...")
        elif not target:
            print("You look around, but you can't seem to find that object. Maybe it was in a different room?")
            Player.inventory.append(tool)
        elif tool["code"] != target["code"]:
            print(f"You attempt to use the {tool['name']} on the {target['name']}, but it's about as effective as "
                  f"hitting a couple of sticks together. Weakly.")
        else:
            self.effect(target["effect"])

    def effect(self, code):
        if code == 1:
            self.floor1[2][3].features = None
            self.floor1[2][3].e_passable = True
            print("You try to use the key on the gate. Golly, what a shock. I don't think anyone's ever thought of "
                  "that before. More importantly, did it work? Well... Yes. Yes it did. The gate is open.")
            self.floor1[2][3].short_description = "The eastern room. A passage lies to the west, and an open gate is " \
                                                  "to the east."
            self.floor1[2][3].long_description = "This long room is almost like a hallway itself, if it weren't far " \
                                                 "too wide for that. At the far eastern end of the room is a massive " \
                                                 "gate. An enormous lock was bolting it shut, but has now been " \
                                                 "opened. Through the bars you can see nothing but darkness. " \
                                                 "The door you came from is to the west."


if __name__ == "__main__":
    game = Map()
    x = True
    game.current.occupied = True
    game.current.explored = True
    print(game.current)
    while x:
        action = re.split(r"\s", input(">> ").lower())
        if action[0] in data["motion"]:
            game.move()
        elif action[0] in data["observe"]:
            game.examination(action[-1])
        elif action[0] in data["take"]:
            game.loot_room(action[-1])
        elif action[0] in data["usage"]:
            game.use_item()
        elif action[0] == "help":
            game_help()
        elif action[0] in data["emote"]:
            print("Self-expression is truly a wonderful thing, isn't it?")


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
