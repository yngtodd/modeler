from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from modeler.api.primitives import Primitive


class Sphere(Primitive):
    """ Sphere primitive """

    def __init__(self):
        super().__init__()
        self.call_list = G_OBJ_SPHERE