# This is my very first program in Python. It's inspired by the redstone contraption I first learned how to build
# in Minecraft. The idea was that no matter what four digits you pressed, the door would open. But unless you entered
# the correct combination, the trap would trigger and kill you.
# Working title: "Snakes in a Cave"

import re
import json
with open("gamedata.json", "r") as gamedata:
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


class Item:
    def __init__(self, desc, inf=False, reuse=False):
        self.infinite = inf
        self.reuse = reuse
        self.description = desc


class Key(Item):
    name = "key"

    def __init__(self, code, desc):
        super().__init__(desc)
        self.item_code = code


class Feature:
    def __init__(self, obj_code, effect):
        self.obj_code = obj_code
        self.effect = effect


class Gate(Feature):
    def __init__(self, obj_code, effect):
        super().__init__(obj_code, effect)


class Lever(Feature):
    def __init__(self, obj_code, effect):
        super().__init__(obj_code, effect)


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

    if input(">> ").lower() in ("ls", "list"):
        pass
    # TODO: Add command list in the help function.


class Location:
    is_occupied = False
    is_explored = False

    # Set to 0 if you can't move that direction, or 1 if you can. "nsewud"
    def __init__(self, move="000000"):
        self.n_passable = int(move[0])
        self.s_passable = int(move[1])
        self.e_passable = int(move[2])
        self.w_passable = int(move[3])
        self.up_passable = int(move[4])
        self.down_passable = int(move[5])


class Room(Location):
    def __init__(self, desc, visual, loot=None, features=None, move="000000"):
        super().__init__(move)
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
        [Wall(), Wall(), Room(data["u_desc"], data["u_vis"], move="010000"), Wall(), Wall()],
        [Wall(), Room(data["l_desc"], data["l_vis"], move="001000"), Room(data["s_desc"], data["s_vis"], move="111100"),
         Room(data["r_desc"], data["r_vis"], features=[data["gate"]], move="000100"), Room(data["dun_desc"], data["dun_vis"], move="000110")],
        [Wall(), Wall(), Room(data["d_desc"], data["d_vis"], loot=[data["key"]], move="100000"), Wall(), Wall()],
        [Wall(), Wall(), Wall(), Wall(), Wall()]
        ]
    floor2 = [
        [Wall(), Wall(), Wall(), Wall(), Wall()],
        [Wall(), Wall(), Room(data["u_desc"], data["u_vis"], move="010000"), Wall(), Wall()],
        [Wall(), Room(data["l_desc"], data["l_vis"], move="001000"), Room(data["s_desc"], data["s_vis"], move="111100"),
         Room(data["r_desc"], data["r_vis"], features=[data["gate"]], move="000100"), Room(data["dun_desc"], data["dun_vis"], move="000101")],
        [Wall(), Wall(), Room(data["d_desc"], data["d_vis"], loot=[data["key"]], move="100000"), Wall(), Wall()],
        [Wall(), Wall(), Wall(), Wall(), Wall()]
        ]
    floors = [floor1, floor2]

    current_location = floors[0][2][2]
    previous_location = floors[0][2][2]
    coords = [0, 2, 2]
    prev_coords = [0, 2, 2]

    def move(self, destination):
        z, y, x = self.coords[0], self.coords[1], self.coords[2]
        is_passable = False
        barrier = True

        if destination in data["north"]:
            y = y - 1
            if self.current_location.n_passable and self.floors[z][y][x].s_passable:
                is_passable = True

        elif destination in data["south"]:
            y = y + 1
            if self.current_location.s_passable and self.floors[z][y][x].n_passable:
                is_passable = True

        elif destination in data["east"]:
            x = x + 1
            if self.current_location.e_passable and self.floors[z][y][x].w_passable:
                is_passable = True

        elif destination in data["west"]:
            x = x - 1
            if self.current_location.w_passable and self.floors[z][y][x].e_passable:
                is_passable = True

        elif destination == "upstairs":
            z = z + 1
            if self.current_location.up_passable and self.floors[z][y][x].down_passable:
                is_passable = True

        elif destination == "downstairs":
            z = z - 1
            if self.current_location.down_passable and self.floors[z][y][x].up_passable:
                is_passable = True

        elif destination == "stairs":
            upstairs = False
            downstairs = False
            if self.current_location.up_passable and self.floors[z+1][y][x].down_passable:
                upstairs = True
            if self.current_location.down_passable and self.floors[z-1][y][x].up_passable:
                downstairs = True

            if upstairs and downstairs:
                print("Okay, but, like... Were you wanting to go up, or down?")
                barrier = False
            elif upstairs and not downstairs:
                z = z - 1
                is_passable = True
            elif downstairs and not upstairs:
                z = z + 1
                is_passable = True
            else:
                print("There aren't any stairs in this room. Maybe if you find a boulder you can stand on it and pretend?")
                barrier = False

        elif destination in data["backward"]:
            if self.current_location == self.previous_location:
                print("You look up towards the hole you fell from. You jump, but it remains out of reach.")
            else:
                self.current_location.is_occupied = False
                self.current_location, self.previous_location = self.previous_location, self.current_location
                self.coords, self.prev_coords = self.prev_coords, self.coords
                self.current_location.is_occupied = True
                print(self.current_location.short_description)
            barrier = False

        else:
            print("You really, really want to do that. But try as you might, you can't think what direction that is.")
            barrier = False

        if is_passable:
            self.current_location.is_occupied = False
            self.previous_location = self.current_location
            self.current_location = self.floors[z][y][x]
            self.prev_coords = self.coords
            self.coords = [z, y, x]
            self.current_location.is_occupied = True
            if self.current_location.is_explored:
                print(self.current_location.short_description)
            else:
                self.current_location.is_explored = True
                print(self.current_location)
        elif barrier:
            print("You have hit a wall and cannot go this way.")

        # if action[-1] in data["stairs"]:
        #     if self.current_location.upstairs and self.floors[layer - 1][row][col].downstairs:
        #         self.current_location.is_occupied = False
        #         self.previous_location = self.current_location
        #         self.current_location = self.floors[layer - 1][row][col]
        #         self.previous_floor = self.current_floor
        #         self.current_floor = self.floors[layer-1]
        #         self.prev_coords = self.coords
        #         self.coords = [row, col, layer-1]
        #         self.current_location.is_occupied = True
        #         if self.current_location.is_explored:
        #             print(self.current_location.short_description)
        #         else:
        #             self.current_location.is_explored = True
        #             print(self.current_location)
        #
        #     elif self.current_location.downstairs and self.floors[layer + 1][row][col].upstairs:
        #         self.current_location.is_occupied = False
        #         self.previous_location = self.current_location
        #         self.current_location = self.floors[layer + 1][row][col]
        #         self.previous_floor = self.current_floor
        #         self.current_floor = self.floors[layer+1]
        #         self.prev_coords = self.coords
        #         self.coords = [row, col, layer+1]
        #         self.current_location.is_occupied = True
        #         if self.current_location.is_explored:
        #             print(self.current_location.short_description)
        #         else:
        #             self.current_location.is_explored = True
        #             print(self.current_location)

    def view_map(self):
        special = 0  # If a special character is printed, this prevents the normal character from printing.
        z = self.coords[0]
        current_floor = self.floors[z]
        for row_idx, row in enumerate(current_floor):
            for idx, line in enumerate(self.current_location.visual):  # For each row in the room's visual representation.
                for col_idx, room in enumerate(row):
                    if room.is_explored:
                        for char in range(len(line)):  # Go through each character individually
                            # Player marker
                            if room.is_occupied and char == 4 and idx == 2:
                                print("X", end="")
                                special += 1
                            # Eastern gate
                            if current_floor[row_idx][min(len(row) - 1, col_idx + 1)] != room:  # Boundary verification
                                if not room.e_passable and current_floor[row_idx][col_idx + 1].w_passable \
                                        and char == len(line) - 2 and idx == len(self.current_location.visual) // 2:
                                    print("+", end="")
                                    special += 1
                            # Western gate
                            if current_floor[row_idx][max(0, col_idx - 1)] != room:  # Boundary verification
                                if not room.w_passable and current_floor[row_idx][col_idx - 1].e_passable \
                                        and char == 1 and idx == len(self.current_location.visual) // 2:
                                    print("+", end="")
                                    special += 1
                            # Northern gate
                            if current_floor[max(0, row_idx - 1)][col_idx] != room:  # Boundary verification
                                if not room.n_passable and current_floor[row_idx - 1][col_idx].s_passable \
                                        and char == len(line) // 2 and idx == 1:
                                    print("+", end="")
                                    special += 1
                            # Southern gate
                            if current_floor[min(len(current_floor), row_idx + 1)][col_idx] != room:  # Boundary verification
                                if not room.s_passable and current_floor[row_idx + 1][col_idx].n_passable \
                                        and char == len(line) // 2 and idx == len(self.current_location.visual) - 2:
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
            self.move(item)
        else:
            if self.current_location.loot:
                for thing in self.current_location.loot:
                    if item == thing["name"]:
                        Player.inventory.append(thing)
                        self.current_location.loot.remove(thing)
                        print(f"You take the {item} and place it in your inventory.")
                    else:
                        print("You searched high and low, but you can't seem to find that object in this room.")
            else:
                print("You searched high and low, but you can't seem to find that object in this room.")

    def examine(self, target):
        if target == "map":
            self.view_map()
        elif target in data["space"]:
            print(self.current_location)
        elif target in data["bag"]:
            items_list = []
            if Player.inventory:
                for item in Player.inventory:
                    items_list.append(item["name"])
                print(", ".join(items_list))
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
        if self.current_location.features:
            for thing in self.current_location.features:
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
    game.current_location.is_occupied = True
    game.current_location.is_explored = True
    print(game.current_location)
    while x:
        stairs = None
        action = re.split(r"\s", input(">> ").lower())
        if action[-1] in data["stairs"]:
            if "up" in action:
                stairs = "upstairs"
            elif "down" in action:
                stairs = "downstairs"
            else:
                stairs = action[-1]

        if action[0] in data["motion"]:
            if stairs:
                game.move(stairs)
            else:
                game.move(action[-1])
        elif action[0] in data["observe"]:
            game.examine(action[-1])
        elif action[0] in data["take"]:
            if stairs:
                game.move(stairs)
            else:
                game.loot_room(action[-1])
        elif action[0] in data["usage"]:
            if stairs:
                game.move(stairs)
            else:
                game.use_item()
        elif action[0] == "help":
            game_help()
        elif action[0] in data["emote"]:
            print("Self-expression is truly a wonderful thing, isn't it?")
        # elif action[0] == "exit":
        #     x = False
