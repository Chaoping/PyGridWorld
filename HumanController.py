from _Getch import *
import GridWorld

class HumanController():
    def __init__(self):
        self.gw = GridWorld.GridWorld()

    def run(self):
        while True:
            print("gimme a direction")
            direction = getch()
            if direction == 't' or direction == 'q':
                break
            self.gw.action(direction)
            


hc = HumanController()
hc.run()
