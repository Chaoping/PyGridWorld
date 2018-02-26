from _Getch import *
import GridWorld

class HumanController():
    def __init__(self):
        self.gw = GridWorld.GridWorld()

    def run(self):
        while True:
            print("gimme a direction")
            char_input = getch()
            direction = [0,0,0,0,0]
            if char_input == 't' or char_input == 'q':
                break
            elif char_input == 'w':
                direction[0] = 1
            elif char_input == 'a':
                direction[1] = 1
            elif char_input == 's':
                direction[2] = 1
            elif char_input == 'd':
                direction[3] = 1
            elif char_input == ' ':
                direction[4] = 1
            self.gw.action(direction)
            


hc = HumanController()
hc.run()
