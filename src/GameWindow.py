"""Game Window for the Pyre Game"""

#     This part of mPyre, a python implementation of the game Empire
#     Copyright (C) 2019  Robert C. Ramsdell III <rcriii42@gmail.com>
#
#     mPyre is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     mPyre is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with mPyre.  If not, see <https://www.gnu.org/licenses/>.
#
#     Work started on 19 December, 2019



import pygame
from pygame.locals import Rect
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.locals import K_KP1, K_KP2, K_KP3, K_KP4, K_KP6, K_KP7, K_KP8, K_KP9
from pygame.locals import K_n, K_END

import planes
import planes.gui
from GraphicUtils import colors
import BaseObjects, Cities
from MapBuilder import draw_map

char_width = 10

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
teal = (0, 128, 128)
yellow = (255, 255, 0)
white = (255, 255, 255)
buff = (240, 220, 130)
black = (0, 0, 0, 255)

bubble_nos = set(range(1000)) #serial nos for bubbles, hope we never have more than 1000
class MessageBubble(planes.gui.OutlinedText):
    """
    MessageBubble - A label that self-destructs after a short period of time
    """
    def __init__(self, item, text, text_color=yellow, res_time=2, float=0):
        """Initialise the MessageBubble.
            item is the item to put the bubble next to (expected to have name & rect parameter)
           text is the text to be written on the Label. If text is None, it is
           replaced by an empty string.
           res_time is the time to stay active in seconds.
           If float positive, the bubble moves up and to the right that many pixels per update
        """
        self.num = bubble_nos.pop()
        name = "%s_%d"%(item.name, self.num)
        planes.gui.OutlinedText.__init__(self, name, text, text_color)
        self.clock = pygame.time.Clock()
        self.life = res_time*1000.
        self.float = (float, float*-1)
        
    def update(self):
        """Call the base class update, then check for end-of-life.
        """
        self.rect.move_ip(self.float)
        planes.gui.Label.update(self)
        self.life -= self.clock.tick()
        if self.life <= 0:
            bubble_nos.add(self.num)
            self.destroy()
        return

class CityStatus(planes.gui.Container):
    """
    CityStatus - Class to wrap a status window for a city that updates each turn
    """
    def __init__(self, city, msgs=[] ,padding = 0, background_color = None):
        """
        initialize.  Initialized with a name, destroy button in upper right, and
        basic city information.
        """
        planes.gui.Container.__init__(self, "{}_status".format(city.name), padding, background_color)
        self.city = city
        if city.owner:
            owner_name = city.owner.name
        else:
            owner_name = 'Neutral'
        city_data_strs = [('city_name', city.name),
                          ('city owner', owner_name)]
        city_data_strs.extend(msgs)
        self.num_proj=-1

        name_length = max([len(s[1]) for s in city_data_strs])*char_width+char_width
        for s in city_data_strs:
            name_label=planes.gui.Label(s[0],
                                            s[1],
                                            Rect(0, 0, name_length, 15),
                                            background_color=teal)
            self.sub(name_label)

        destroy_button = planes.gui.Button('X',
                                               Rect(name_label.rect.width-char_width, 0, char_width, 15),
                                               lambda x: x.parent.parent.destroy(),
                                               background_color=teal)
        name_label.sub(destroy_button)


    def update(self):
        """
        Update the labels for the city.
        """
        planes.gui.Container.update(self)

class GameWindow(object):
    """
    GameWindow - Class to wrap the graphical display for the game.
    """
    def __init__(self, controller, image_size):
        self.controller = controller
        self.image_size = image_size

        pygame.init()
        self.screenSize = (controller.size[0]*image_size + image_size*2 + 12,
                           image_size*17 + image_size*2 + 30)
        self.w32windowClass = "pygame"  #The win32 window class for this object
        self.screen = planes.Display(self.screenSize)
        self.windowCaption = "mPyre"
        pygame.display.set_caption(self.windowCaption)        
        self.white = pygame.Color("white")
        self.screen.image.fill(self.white)
        pygame.display.flip()

        
        # #The game screen
        self.game_plane = planes.Plane("game screen", Rect(0, 0,
                                                           (controller.size[0] + 2)*image_size,
                                                           (controller.size[1] + 2)*image_size))

        self.game_background = draw_map(self.game_plane, self.controller.G.map, self.image_size)

        self.game_plane.image.blit(self.game_background, (0,0))

        scroller = planes.gui.ScrollingPlane("scroller",
                                             Rect(0, 0, self.screenSize[0]-12, self.screenSize[1] - 30),
                                             self.game_plane)
        self.screen.sub(scroller)
        
        #The main status display - turn and player name
        self.turn_status = planes.gui.Button("Turn: 1",
                                             Rect(0, self.screenSize[1]-30, 150, 30),
                                             self.next_turn) #callback placeholder
        self.screen.sub(self.turn_status)
        self.player_status = planes.gui.Button("Player: player_1",
                                               Rect(150, self.screenSize[1]-30, 125, 30),
                                               None) #callback placeholder
        self.screen.sub(self.player_status)

        self.status_window = None
        self._selected = None
        
        self.city_bubble = None

        self.advance_turn = False

        pygame.display.flip()

    @property
    def selected(self):
        """The selected object"""
        return self._selected

    @selected.setter
    def selected(self, s):
        if self._selected:
            if self._selected.plane:
                self._selected.plane.remove("outlined_selection")
                #self._selected.plane.render()
            if not isinstance(self._selected, Cities.City) and self._selected.plane:
                self.game_plane.sub(self._selected.plane,
                                    insert_before=self.game_plane.subplanes_list[0])
        self._selected = s
        if isinstance(s, BaseObjects.Unit):
            self.show_city_status(s)
            img = s.plane.image.copy()
            pygame.draw.rect(img,
                             red,
                             [0, 0, self.image_size-1, self.image_size-1],
                             3)
            outlined = planes.Plane("outlined_selection",
                                    Rect([0, 0, self.image_size-1, self.image_size-1]))
            outlined.image.blit(img, (0,0))
            s.plane.sub(outlined)
            self.game_plane.sub(s.plane)
        else:
            pass

    def update(self):
        """update - update the game window"""
        game = self.controller.G
        self.game_plane.image.blit(self.game_background, (0,0)) #reset background drawing
        for c in game.cities:
            if not c.plane:
                c_rect = Rect((c.coords[0]*self.image_size, c.coords[1]*self.image_size),
                              [self.image_size]*2)
                c.set_image([self.image_size]*2, c.owner.color)
                c.plane = planes.Plane("City of {}".format(c.name), c_rect)
                c.plane.image.blit(c.image, (0,0))
                self.game_plane.sub(c.plane)

        for u in game.units:
            if not u.plane:
                u_rect = Rect((u.coords[0] * self.image_size, u.coords[1] * self.image_size),
                              [self.image_size] * 2)
                u.set_image([self.image_size]*2, u.owner.color)
                u.plane = planes.Plane("Unit {}".format(u.name), u_rect)
                u.plane.image.blit(u.image, (0, 0))
                self.game_plane.sub(u.plane,
                                    insert_before=self.game_plane.subplanes_list[0])
                # d.plane.draggable=True
                # self.game_plane.sub(d.plane)

        if not self.selected and self.status_window:
            self.status_window.destroy()
            self.status_window = None
        self.turn_status.text = "Turn: {0:,}".format(int(game.turn))
        self.player_status.current_color = colors[game.current_player.color]
        self.player_status.text = "{}".format(game.current_player.name)
        self.screen.update()
        self.screen.render()
        
        pygame.display.flip()
        return True
    
    def show_city_status(self, c):
        if self.status_window:
            self.status_window.destroy()
        if isinstance(c, Cities.City):
            if c.building.name == 'none':
                msgs = [('building', "Building: {}".format(c.building.name))]
            else:
                msgs = [('building', "Building: {}".format(c.building.name)),
                        ('finished', '{:d} turns left'.format(c.time_to_build))]
        else: #assume the unit is a combat unit
            msgs = [('strength', 'Strength: {}'.format(c.current_strength)),
                    ('moves_left:', 'Moves: {}'.format(c.move_speed - c.moved))]
        city_status = CityStatus(c, msgs)

        #place city status where it will not lap off the edge of the screen, starting in top left
        if c.plane.rect.left-city_status.rect.width>self.game_plane.rect.left and c.plane.rect.top-city_status.rect.height>self.game_plane.rect.top:
            city_status.rect.bottomright = c.plane.rect.topleft
        elif c.plane.rect.right+city_status.rect.width<self.game_plane.rect.right and c.plane.rect.top-city_status.rect.height>self.game_plane.rect.top:
            city_status.rect.bottomleft = c.plane.rect.topright
        elif c.plane.rect.right+city_status.rect.width>self.game_plane.rect.right and c.plane.rect.bottom+city_status.rect.height<self.game_plane.rect.bottom:
            city_status.rect.topleft = c.plane.rect.bottomright
        else:
            city_status.rect.topright = c.plane.rect.bottomleft
        self.game_plane.sub(city_status)
        self.status_window = city_status

    def post_quit(self):
        q = pygame.event.Event(pygame.QUIT)
        pygame.event.post(q)

    def quit(self):
        pygame.quit()

    def next_turn(self, object=None):
        """The user wishes to end the turn"""
        self.selected = None
        self.advance_turn = True

    def mainloop(self):
        """The mainloop for the game, expects a controller to manage the game objects"""
        while self.controller.end != True:
            self.update()
            self.next_message = None
            last_mouse_move = None
            last_mouse_down = None
            last_mouse_up = None
            last_key_down = None
            if self.controller.G.current_player.AI:
                #print("AI for {} taking turn.".format(self.controller.G.current_player.name))
                msgs =self.controller.G.current_player.AI.next_move()
                if 'End Turn' in msgs:
                  self.next_turn()
                elif 'move' in msgs:
                    last_key_down = pygame.event.Event(pygame.KEYDOWN, key=msgs[2], mod=0)
                pygame.event.clear()

            # for m in messages:
            #     if m[1]:
            #         mb = MessageBubble(m[0].plane, m[1], float=2)
            #         mb.rect.bottomleft = m[0].plane.rect.topright
            #         self.game_plane.sub(mb)
            #Check events
            event_list = pygame.event.get()
            self.screen.process(event_list) #Let planes go first

            for e in event_list:
                if e.type == QUIT:
                    self.controller.quit()
                elif e.type == MOUSEMOTION:
                    last_mouse_move = e
                elif e.type == MOUSEBUTTONDOWN:
                    last_mouse_down = e
                elif e.type == MOUSEBUTTONUP:# and drag_dredge:
                    last_mouse_up = e
                elif e.type == KEYDOWN and last_key_down is None:
                    last_key_down = e
            if last_mouse_move:
                #self.next_message = "Moved to: {}".format(last_mouse_move.pos)
                pass
            if last_mouse_down:
                self.selected = None
                if self.status_window:
                    self.status_window.destroy()
                if self.city_bubble:
                    self.city_bubble.destroy()
                    self.city_bubble = None
                self.next_message = "Mouse click: {} {} {}".format(last_mouse_down.pos,
                                                                (last_mouse_down.pos[0]/32, last_mouse_down.pos[1]/32),
                                                                last_mouse_down.button)
                for c in self.controller.G.cities:
                    #did we click on a city?
                    if c.plane.rect.collidepoint(last_mouse_down.pos):
                        self.next_message =  "clicked on city of %s"%c.name
                        self.selected = c

                for u in self.controller.G.units:
                    #How about a unit?
                    if u.plane.rect.collidepoint(last_mouse_down.pos):
                        if u.owner is self.controller.G.current_player:
                            self.next_message = "selected {}".format(u.name)
                            self.selected = u
                        else:
                            self.next_message = "could not select {}".format(u.name)
            #             if last_mouse_down.button == 1:
            #                 drag_dredge = u
            #                 self.next_message = "dragging dredge %s"%d.name

            if last_key_down:
                if  isinstance(self.selected, BaseObjects.Unit) and\
                    last_key_down.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT,
                                          K_KP1, K_KP2, K_KP3, K_KP4,
                                          K_KP6, K_KP7, K_KP8, K_KP9]:
                    self.controller.move_unit(self.selected, last_key_down.key)
                    if self.selected.plane:
                        vector = (self.selected.coords[0] * self.image_size - self.selected.plane.rect.x,
                                  self.selected.coords[1] * self.image_size - self.selected.plane.rect.y)
                        self.selected.plane.rect.move_ip(vector)
                        if self.selected.moved >= self.selected.move_speed:
                            self.selected = self.selected.owner.next_to_move(self.selected)
                    else:
                        self.selected = self.controller.G.current_player.next_to_move()
                elif last_key_down.key in [K_n]:
                    self.selected = self.controller.G.current_player.next_to_move(self.selected)
                elif last_key_down.key in [K_END]:
                    self.next_turn()

            # # if drag_dredge:
            # #     if last_mouse_up:
            #         drag_dredge.destination = last_mouse_up.pos
            #         self.next_message = "Dredge %s moved to: %s"%(drag_dredge.name, drag_dredge.destination)
            #         drag_dredge = None
            #     else:
            #         pass
            #         #self.next_message = "dragging dredge %s to %s"%(d.name, `dredge_drag_to`)
            
            #move on with our lives
            if self.advance_turn:
                msgs = self.controller.step()
                print("\n".join(msgs))
                for m in msgs:
                    if "lost!" in m:
                        print(m)
                    if "won!" in m:
                        print(m)
                self.update()
                if self.controller.G.current_player.units:
                    self.selected = self.controller.G.current_player.units[0]
                self.advance_turn = False
            pygame.event.clear()
            if self.next_message: print(self.next_message)
