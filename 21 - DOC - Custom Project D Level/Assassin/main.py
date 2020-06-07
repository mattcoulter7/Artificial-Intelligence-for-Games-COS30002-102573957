from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from point2d import Point2D

from math import pi
from random import randrange

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720

def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol == KEY.I:
        world.show_info = not world.show_info

def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        pt = Vector2D(x,y)
        world.target = world.graph.fit_pos_to(pt.copy(),type = 'center',relative = True)
        world.assassin.update_path()
        world.assassin.guard = world.click_on(pt,'guards') #Set assassin guard to a guard that was clicked, is None if none were clicked on

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy

if __name__ == '__main__':
    # create a pyglet window and set glOptions
    win = window.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, vsync=False, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = window.FPSDisplay(win)
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_resize)
    win.push_handlers(on_mouse_press)
    # create a world for agents
    map = 'maps/map{}.csv'.format(randrange(0,99))
    #map = 'maps/map82.csv'
    print(map)
    world = World(SCREEN_WIDTH, SCREEN_HEIGHT,map)
    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_display.draw()
        # swap the double buffer
        win.flip()


