from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import modeler.api.functional as F
from modeler.api import HierarchicalNode
from modeler.primitives.sphere import Sphere


class Snowman(HierarchicalNode):
    """ Composed of three spheres """

    def __init__(self):
        self.child_nodes = [Sphere(), Sphere(), Sphere()]
        self.compose()

    def compose(self):
        """ Compose the spheres to make the shape """
        # Stack the spheres on top of one another
        self.child_nodes[0].translate(0, -0.6, 0)
        self.child_nodes[1].translate(0, 0.1, 0)
        self.child_nodes[2].translate(0, 0.75, 0)

        # Shrink the middle sphere to 80%
        self.child_nodes[1].scaling_matrix = np.dot(
            self.scaling_matrix,
            F.scaling([0.8, 0.8, 0.8])
        )

        # Scale the top sphere to 70%
        self.child_nodes[2].scaling_matrix = np.dot(
            self.scaling_matrix,
            F.scaling([0.7, 0.7, 0.7])
        )

        # Color the spheres white
        for child in self.child_nodes:
            child.color_index = color.MIN_COLOR

        # Create a bounding box around the shapes
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 1.1, 0.5])
