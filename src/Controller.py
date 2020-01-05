"""Controller - The controller object that mediates between the game world and the display window"""
import random
import Game

class World(object):
    """ global controller construct"""
    def __init__(self):
        self.id=random.randint(101,1001)
        self.end = False
        self.G = Game.Game()
        self.history = {}
    
    def quit(self):
        self.end = True
    
    def step(self, move_type=('end_turn',)):
        """Primary logic loop for a 'move'

        move_type is a tuple: ('text indicating the move',
                               other objects related to the move,
                               ...)
        """
        step_messages = []
        if move_type[0] == 'end_turn':
            print('Advancing turn to {}'.format(self.G.turn+1))
            self.G.turn += 1
            step_messages.append("Turn: {0:,}".format(int(self.G.turn)))
            # Run World Value / Progress Calcs
            for mycity in self.G.cities:
                step_messages.extend(mycity.turn_step(self.G))

            for myplayer in self.G.players:
                #Note that players update their units
                step_messages.extend(myplayer.turn_step(self.G))

        # Record world for history I'm sure this will be interesting later 
        self.history[self.G.turn]=step_messages
        return step_messages
