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



import pygame, os
from pygame.locals import Rect
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.locals import K_KP1, K_KP2, K_KP3, K_KP4, K_KP6, K_KP7, K_KP8, K_KP9
from GraphicUtils import tile_texture
import clickndrag
import clickndrag.gui
from GraphicUtils import colors
import BaseObjects, GroundUnits, Cities

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
class MessageBubble(clickndrag.gui.OutlinedText):
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
        clickndrag.gui.OutlinedText.__init__(self, name, text, text_color)
        self.clock = pygame.time.Clock()
        self.life = res_time*1000.
        self.float = (float, float*-1)
        
    def update(self):
        """Call the base class update, then check for end-of-life.
        """
        self.rect.move_ip(self.float)
        clickndrag.gui.Label.update(self)
        self.life -= self.clock.tick()
        if self.life <= 0:
            bubble_nos.add(self.num)
            self.destroy()
        return

class CityStatus(clickndrag.gui.Container):
    """
    CityStatus - Class to wrap a status window for a city that updates each turn
    """
    def __init__(self, city, msgs=[] ,padding = 0, background_color = None):
        """
        initialize.  Initialized with a name, destroy button in upper right, and
        basic city information.
        """
        clickndrag.gui.Container.__init__(self, "{}_status".format(city.name), padding, background_color)
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
            name_label=clickndrag.gui.Label(s[0],
                                            s[1],
                                            Rect(0, 0, name_length, 15),
                                            background_color=teal)
            self.sub(name_label)

        destroy_button = clickndrag.gui.Button('X',
                                               Rect(name_label.rect.width-char_width, 0, char_width, 15),
                                               lambda x: x.parent.parent.destroy(),
                                               background_color=teal)
        name_label.sub(destroy_button)


    def update(self):
        """
        Update the labels for the city.
        """
        clickndrag.gui.Container.update(self)

class GameWindow(object):
    """
    GameWindow - Class to wrap the graphical display for the game.
    """
    def __init__(self, width=32*25, height=32*20, timeScale=1):
        
        self.max_frame_rate = 10    #max frame rate in frames-per-second
        self.clock = pygame.time.Clock()
        
        pygame.init()
        self.screenSize = width+15, height+30
        self.w32windowClass = "pygame"  #The win32 window class for this object
        self.screen = clickndrag.Display(self.screenSize) #pygame.display.set_mode(self.screenSize)
        self.windowCaption = "mPyre"
        pygame.display.set_caption(self.windowCaption)        
        self.white = pygame.Color("white")
        self.screen.image.fill(self.white)
        pygame.display.flip()
        
        # #The game screen
        plains_tile = pygame.image.load(os.path.join('graphics', 'plains_tile_32x32.png')).convert()
        self.tiles = [plains_tile]*100
        menu_margin = width#*.75
        self.game_plane = clickndrag.Plane("game screen", Rect(0, 0, menu_margin, height))
        self.game_background = tile_texture(self.game_plane.image, self.tiles)
        self.game_plane.image.blit(self.game_background, (0,0))
        self.screen.sub(self.game_plane)
        
        #The main status display - Date and player $$
        self.turn_status = clickndrag.gui.Button("Turn: 1",
                                                Rect(0, self.screenSize[1]-30, 150, 30),
                                                self.next_turn) #callback placeholder
        self.screen.sub(self.turn_status)
        self.player_status = clickndrag.gui.Button("Player: player_1",
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
                self._selected.plane.render()
            if not isinstance(self._selected, Cities.City) and self._selected.plane:
                self.game_plane.sub(self._selected.plane, 0)
        self._selected = s
        if isinstance(s, BaseObjects.Unit):
            self.show_city_status(s)
            img = s.plane.image.copy()
            pygame.draw.rect(img, red, [0, 0, 31, 31], 3)
            outlined = clickndrag.Plane("outlined_selection", Rect([0, 0, 31, 31]))
            outlined.image.blit(img, (0,0))
            s.plane.sub(outlined)
            self.game_plane.sub(s.plane)
        else:
            pass

    def update(self, game):
        """update - update the game window"""
        self.game_plane.image.blit(self.game_background, (0,0)) #reset background drawing
        for c in game.cities:
            if not c.plane:
                c.plane = clickndrag.Plane("City of {}".format(c.name), Rect(c.coords, c.image_size))
                c.plane.image.blit(c.image, (0,0))
                c.plane.sub(c.plane)
                self.game_plane.sub(c.plane)

        for u in game.units:
            if not u.plane:
                u.plane = clickndrag.Plane("Unit {}".format(u.name), Rect(u.coords, u.image_size))
                u.plane.image.blit(u.image, (0,0))
                self.game_plane.sub(u.plane, 0)
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

    def mainloop(self, controller):
        """The mainloop for the game, expects a controller to manage the game objects"""
        drag_dredge = False
        while controller.end != True:
            self.update(controller.G)
            # for m in messages:
            #     if m[1]:
            #         mb = MessageBubble(m[0].plane, m[1], float=2)
            #         mb.rect.bottomleft = m[0].plane.rect.topright
            #         self.game_plane.sub(mb)
            #Check events
            event_list = pygame.event.get()
            self.screen.process(event_list) #Let clickndrag go first
            self.next_message=None
            last_mouse_move = None
            last_mouse_down = None
            last_mouse_up = None
            last_key_down = None
            for e in event_list:
                if e.type == QUIT:
                    controller.quit()
                elif e.type == MOUSEMOTION:
                    last_mouse_move = e
                elif e.type == MOUSEBUTTONDOWN:
                    last_mouse_down = e
                elif e.type == MOUSEBUTTONUP:# and drag_dredge:
                    last_mouse_up = e
                elif e.type == KEYDOWN:
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
                #self.next_message = "Mouse click: %s %s"%(`last_mouse_down.pos`, `last_mouse_down.button`)
                for c in controller.G.cities:
                    #did we click on a city?
                    if c.plane.rect.collidepoint(last_mouse_down.pos):
                        self.next_message =  "clicked on city of %s"%c.name
                        self.selected = c

                for u in controller.G.units:
                    #How about a unit?
                    if u.plane.rect.collidepoint(last_mouse_down.pos):
                        if u.owner is controller.G.current_player:
                            self.next_message = "selected {}".format(u.name)
                            self.selected = u
                        else:
                            self.next_message = "could not select {}".format(u.name)
            #             if last_mouse_down.button == 1:
            #                 drag_dredge = u
            #                 self.next_message = "dragging dredge %s"%d.name

            if last_key_down and isinstance(self.selected, BaseObjects.Unit):
                if last_key_down.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT,
                                         K_KP1, K_KP2, K_KP3, K_KP4,
                                         K_KP6, K_KP7, K_KP8, K_KP9]:
                    self.selected = controller.move_unit(self.selected, last_key_down.key)
                    if self.selected:
                        if self.selected.moved >= self.selected.move_speed:
                            self.selected = self.selected.owner.next_to_move(self.selected)
                    else:
                        self.selected = controller.G.current_player.next_to_move()

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
                msgs = controller.step()
                print("\n".join(msgs))
                for m in msgs:
                    if "lost!" in m:
                        print(m)
                    if "won!" in m:
                        print(m)
                self.update(controller.G)
                if controller.G.current_player.units:
                    self.selected = controller.G.current_player.units[0]
                self.advance_turn = False
            pygame.event.clear()
            if self.next_message: print(self.next_message)
            elapsed = self.clock.tick(self.max_frame_rate)
