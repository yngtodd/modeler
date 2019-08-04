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

    def pick(self, start, direction, mat):
        """ Determine whether a ray hits the object 

        Parameters
        ----------
        start : np.ndarray
            Start of the ray

        direction : np.ndarray
            Direction of the ray

        mat : np.ndarray
            model_view matrix used to transform the ray

        Returns
        -------
        results : 
        """
        new_mat = np.dot(
            np.dot(mat, self.translation_matrix),
            np.linalg.inv(self.scaling_matrix)
        )

        results = self.aabb.ray_hit(start, direction, mat)
        return results

    def select(self, select=None):
        """ Toggles or sets selected state """
        if select is not None:
            self.selected = select
        else:
            self.selected not self.selected


class HierarchicalNode(Node):
    """ Node composed of multiple primitives """

    def __init__(self):
        super().__init__()
        self.child_nodes = []

    def render_self(self):
        for child in child_nodes:
            child.render()

    def compose(self):
        raise NotImplementedError(
            "Hierarchical nodes must define a way of composing primitives."
        )