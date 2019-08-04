from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from modeler.api import Node


class Primitive(Node):
    """ Base class for types of nodes """

    def __init__(self):
        super().__init__()
        self.call_list = None

    def render_self(self):
        glCallList(self.call_list)