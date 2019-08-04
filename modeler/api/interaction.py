from collections import defaultdict

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Interaction:
    """ User interaction callback system for GLUT """

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

    def register_callback(self, name, func):
        self.callbacks[name].append(func)

    def trigger(self, name, *args, **kwargs):
        for func in self.callbacks[name]:
            func(*args, **kwargs)
    
    def translate(self):
        """ Translate the camera """
        self.translation[0] += x
        self.translation[1] += y 
        self.translation[2] += z 

    def handle_mouse_button(self, button, mode, x, y):
        """ Handle mouse button press and releases """
        x_size, y_size = self._get_window_size() 
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
    
    def handle_mouse_move(self, x, screen_y):
        """ Callback for mouse movement """
        x_size, y_size = self._get_window_size()
        # Invert the y-coordinate
        y = y_size - screen_y

        if self.pressed is not None:
            dx = x - self.mouse_loc[0]
            dy = y - self.mouse_loc[1]

            if self.pressed == GLUT_RIGHT_BUTTON and self.trackball is not None:
                # Ignore the updated camera location, we want to always rotate around origin
                self.trackball.drag_to(self.mouse_loc[0], self.mouse_loc[1], dx, dy)
            elif self.pressed == GLUT_LEFT_BUTTON:
                self.trigger('move', x, y)
            elif self.pressed == GLUT_MIDDLE_BUTTON:
                self.translate(dx/60.0, dy/60.0, 0)
            else:
                pass
            
            glutPostRedisplay()
        
        self.mouse_loc = (x, y)

    def handle_keystroke(self, key, x, screen_y):
        """ Callback for keyboard input """
        x_size, y_size = self._get_window_size()
        # Invert the y_coordinate
        y = y_size - screen_y

        if key == 's':
            self.trigger('place', 'sphere', x, y)
        elif key == 'c':
            self.trigger('place', 'cube', x, y)
        elif key == GLUT_KEY_UP:
            self.trigger('scale', up=True)
        elif key == GLUT_KEY_DOWN:
            self.trigger('scale', up=False)
        elif key == GLUT_KEY_LEFT:
            self.trigger('rotate_color', forward=True)
        elif key == GLUT_KEY_RIGHT:
            self.trigger('rotate_color', forward=False)
        
        glutPostRedisplay()

    def _get_window_size(self):
        x_size = glutGet(GLUT_WINDOW_WIDTH)
        y_size =  glutGet(GLUT_WINDOW_HEIGHT)
        return x_size, y_size
