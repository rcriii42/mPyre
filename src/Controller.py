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
            for p in self.G.players:
                num_units = len(p.cities)+len(p.units)
                if num_units < 1:
                    self.G.player_lost(p)
            if len(self.G.players) ==1:
                step_messages.append("Player {} won!".format(self.G.players[0].name))

            if self.G.next_player is None:
                step_messages.extend(self.G.advance_turn())
                # Run World Value / Progress Calcs
                for mycity in self.G.cities:
                    step_messages.extend(mycity.turn_step(self.G))

                for myplayer in self.G.players:
                    #Note that players update their units
                    step_messages.extend(myplayer.turn_step(self.G))
            else:
                step_messages.extend(self.G.advance_player())

        # Record world for history I'm sure this will be interesting later 
        self.history[self.G.turn]=step_messages
        return step_messages

    def move_unit(self, moving_unit, key):
        """Move the given unit if possible"""
        if moving_unit.move_speed > 0:
            target_unit = moving_unit.move(key, self.G)
            if target_unit:
                if target_unit.owner is not moving_unit.owner: #Attack!
                    return self.resolve_combat(moving_unit, target_unit)
            else:
                return moving_unit
        else:
            return None

    def resolve_combat(self, attacker, defender):
        """Resolve an attack by one unit on another"""
        result = random.random()*(attacker.attack+defender.defense)
        if result < attacker.attack: #Attacker won
            defender.current_strength -= attacker.attack
            if defender.current_strength <= 0:
                if defender in defender.owner.cities:
                    #A city changes hands
                    print("resolve_combat: {} captured city of {}".format(attacker.name, defender.name))
                    defender.owner.cities.remove(defender)
                    attacker.owner.assign_city(defender)
                    defender.plane.destroy()
                    defender.plane = None
                else:
                    #A unit is destroyed
                    print("resolve_combat: {} defeated {}".format(attacker.name, defender.name))
                    defender.owner.units.remove(defender)
                    defender.plane.destroy()
                    attacker.plane.rect.move(defender.coords)
                    del defender
            return attacker
        else: #Defender won
            attacker.current_strength -= defender.defense
            if attacker.current_strength <= 0:
                #Attacker destroyed
                print("resolve_combat: {} defeated by {}".format(attacker.name, defender.name))
                attacker.owner.units.remove(attacker)
                attacker.plane.destroy()
                del attacker
            return None