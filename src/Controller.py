"""Controller - The controller object that mediates between the game world and the display window"""
import random, datetime
import Game

days_to_sec = 24*60*60

class World(object):
    """ global controller construct"""
    def __init__(self):
        self.id=random.randint(101,1001) 
        self.timeScale = 1          #Number of seconds per day in game-time
        self.time = 0               #realtime in seconds since start of game
        self.G= Game.Game()
        self.end = False 
        self.history={}
    
    def quit(self):
        self.end = True
    
    def step(self, elapsedtime=1, GW=False):
        # Primary logic loop for a 'turn'
        self.time=self.time + elapsedtime/1000.
        self.elapsedtime = elapsedtime/1000.
        # Run World Value / Progress Calcs
        step_messages = []
        self.G.date += datetime.timedelta(days = elapsedtime/1000./self.timeScale)
        decimal_days = elapsedtime/1000./self.timeScale
        for mycity in self.G.cities:
            #note that the cities update their projects
            step_messages.extend(mycity.time_step(decimal_days, self.G))
            
        for myplayer in self.G.players:
            #Note that players update their dredges
            step_messages.extend(myplayer.time_step(decimal_days, self.G))
        
        # Record world for history I'm sure this will be interesting later 
        self.history[self.time]=self
        return step_messages
