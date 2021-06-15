#This is my very first program in Python. It's inspired by the redstone contraption I first learned how to build
#in Minecraft. The idea was that no matter what four digits you pressed, the door would open. But unless you entered
#the correct combination, the trap would trigger and kill you.

print("Welcome to my RPG test game! You are standing next to a door with a nine-digit keypad.")
counter = 0
code = [1, 2, 3, 4]
for digit in code:
    i = int(input("Please enter a digit. \n"))
    if i == digit:
        print("You hear a chime.")
        counter += 1
    else:
        print("You hear a beep.")
if counter == 4:
    print("The door opens. You walk through and get the treasure. Congratulations!")
else:
    print("The door opens. You see treasure at the end of the hall and eagerly run towards it."
          "Suddenly, the floor opens up beneath you! It was rigged! You plummet to your death. Game over.")
