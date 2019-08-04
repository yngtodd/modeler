from collections import defaultdict

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Interaction:
    """ User interaction """

    def __init__(self):
        self.reset()

    def reset(self):
        self.pressed = None
        # Default location of the camera
        self.translation = [0, 0, 0, 0]
        # Trackball to calculate rotation
        self.trackball = trackball.Trackball(theta = -25, distance = 15)
        # Current mouse location
        self.mouse_loc = None
        # register Callbacks
        self.register()

    def register(self):
        """ Register callbacks with Glut """
        self.callbacks = defaultdict(list)
        glutMouseFunc(self.handle_mouse_button)
        glutMotionFunc(self.handle_mouse_move)
        glutKeyboardFunc(self.handle_keystroke)
        glutSpecialFunc(self.handle_keystroke)
    
    def translate(self):
        """ Translate the camera """
        self.translation[0] += x
        self.translation[1] += y 
        self.translation[2] += z 

    def handle_mouse_button(self, button, mode, x, y):
        """ Handle mouse button press and releases """
        x_size, y_size = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        # Invert the y-coordinate, OpenGL uses an inverted layout
        y = y_size - y
        self.mouse_loc = (x, y)

        if mode == GLUT_DOWN:
            self.pressed = button
            if button == GLUT_RIGHT_BUTTON:
                # Do nothing for now
                pass
            elif button == GLUT_LEFT_BUTTON:
                # Pick
                self.trigger('pick', x, y)
            elif button == 3:
                # Scroll up
                self.translate(0, 0, 1.0)
            elif button == 4:
                # Scroll down
                self.translate(0, 0, -1.0)
        else:
            # Mouse button released
            self.pressed = None

        glutPostRedisplay()