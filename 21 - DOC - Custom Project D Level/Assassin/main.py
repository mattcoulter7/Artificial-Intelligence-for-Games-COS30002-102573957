from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from block import Block
from point2d import Point2D
from assassin import Assassin
from guard import Guard

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720

def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol == KEY.A:
        world.guards.append(Guard(world))
    elif symbol == KEY.UP:
        world.move_screen('up')
    elif symbol == KEY.DOWN:
        world.move_screen('down')
    elif symbol == KEY.LEFT:
        world.move_screen('left')
    elif symbol == KEY.RIGHT:
        world.move_screen('right')

def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        pt = Point2D(x,y)
        world.target = world.graph.fit_pos(pt,'center')
        world.assassin.update_path()
        for guard in world.guards:
            if world.graph.get_node(pt) == world.graph.get_node(guard.pos):
                world.assassin.guard = guard

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy

if __name__ == '__main__':
    # create a pyglet window and set glOptions
    win = window.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, vsync=True, resizable=False)
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
    map = 'maps/map11.csv'
    world = World(SCREEN_WIDTH, SCREEN_HEIGHT,map)
    world.assassin = Assassin(world)
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


