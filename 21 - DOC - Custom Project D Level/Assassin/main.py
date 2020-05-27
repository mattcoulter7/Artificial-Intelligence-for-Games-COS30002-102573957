from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from block import Block
from point2d import Point2D
from assassin import Assassin
from guard import Guard

display = pyglet.canvas.Display()
screen = display.get_default_screen()
SCREEN_WIDTH = screen.width
SCREEN_HEIGHT = screen.height

def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol == KEY.A:
        world.blocks.append(Block(world,0))
    elif symbol == KEY.S:
        world.assassins.append(Assassin(world))
    elif symbol == KEY.D:
        world.guards.append(Guard(world))

def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        pt = Point2D(x,y)
        world.target = world.graph.fit_pos(pt,'center')
        for assassin in world.assassins:
            assassin.update_path()

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy

if __name__ == '__main__':
    # create a pyglet window and set glOptions
    win = window.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, vsync=True, resizable=True)
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
    world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
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


