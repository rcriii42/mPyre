"""Player.py - Contains the Player object"""
from Dredge import Dredge
import Game


class Player(object):
    """Player with dredges"""

    def __init__(self, name="First Player"):
        self.name = name
        self.dredges = []
        self.value = 1000000
        self.projects = []  # a list of Projects
        if Game.Demo:
            self.dredges.append(Dredge(name="Treasure Island", owner=self, production=850, loc=(5 + 16, 425 + 16)))
            self.dredges.append(Dredge(owner=self, loc=(400, 400)))

    def generate_dredge(self, name=None):
        """Add a dredge to a player"""
        self.dredges.append(Dredge())

    def time_step(self, steptimesize, game):
        """Adjust the player to reflect moving forward in time.

           steptimesize is the time step in days.
           game is the game I am part of."""
        ts_messages = []
        revenue = 0
        for myproject in self.projects:
            # For Profit - expect projects to be updated before players
            revenue += myproject.quantity_this_period * myproject.unit_cost
        fixed_costs = 0
        working_costs = 0
        for mydredge in self.dredges:
            # For Payroll! wait Boo!
            fixed_costs -= mydredge.fixed_costs * steptimesize
            mydredge.time_step(steptimesize, game)
            city_its_in = [c for c in game.cities if mydredge.in_city(c)]
            if mydredge.assigned_project and city_its_in:
                working_costs -= mydredge.working_costs * steptimesize
            elif city_its_in:
                projects = [p for p in city_its_in[0].projects if p.player == self]
                if projects:
                    mydredge.assigned_project = projects[0]
                    mydredge.assigned_project.dredges.append(mydredge)
                    ts_messages.append((mydredge, "%s assigned to %s" % (mydredge.name, mydredge.assigned_project)))
        self.value += (revenue + fixed_costs + working_costs)
        return ts_messages
