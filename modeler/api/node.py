import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Node:
    """ Base class for scene elements """

    def __init__(self):
        self.color_index = random.randint(color.MIN_COLOR, color.MAX_COLOR)
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])
        self.translation_matrix = np.identity(4)
        self.scaling_matrix = np.identity(4)
        self.selected = False

    def render(self):
        """ Render the item to the scene """
        glPushMatrix()
        glMultMatrixf(np.transpose(self.translation_matrix))
        glMultMatrixf(self.scaling_matrix)
        color = self.color.COLORS[self.color_index]
        glColor3f(color[0], color[1], color[2])

        if self.selected:
            # Emit light
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0])

        glPopMatrix()

    def render_self(self):
        raise NotImplementedError(
            "The abstract node class doesn't define `render_self`"
        )
