'''Autonomous Agent Movement: Paths and Wandering

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

This code is essentially the same as the base for the previous steering lab
but with additional code to support this lab.

'''
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent
from hiding_object import HideObject

def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused

    # Toggle debug force line info on the agent
    elif symbol == KEY.I:
        world.show_info = not world.show_info
    elif symbol == KEY.A:
        world.agents.append(Agent(world,'hunter'))
    elif symbol == KEY.S:
        world.agents.append(Agent(world,'prey'))
    elif symbol == KEY.D:
        world.hiding_objects.append(HideObject(world))

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy


if __name__ == '__main__':

    # create a pyglet window and set glOptions
    win = window.Window(width=500, height=500, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)

    # prep the fps display
    fps_display = window.FPSDisplay(win)

    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(500, 500)

    # add hunter and pray agents
    world.agents.append(Agent(world,'hunter'))
    world.agents.append(Agent(world,'prey'))

    # add world objects to hide behind
    world.hiding_objects.append(HideObject(world))
    world.hiding_objects.append(HideObject(world))

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

