from _Getch import *
import GridWorld

class HumanController():
    def __init__(self):
        self.gw = GridWorld.GridWorld()

    def run(self):
        while True:
            print("gimme direction")
            direction = getch()
            self.gw.action(direction)
            if direction == 't' or direction == 'q':
                break


hc = HumanController()
hc.run()
