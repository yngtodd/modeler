import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *


class Viewer:
    """ Manage window creation and rendering """

    def __init__(self):
        self.init_interface()
        self.init_opengl()
        self.init_scene()
        self.init_interaction

    def init_interface(self):
        """ Initialize the window and register the render function """
        glutInit()
        glutInitWindowSize(640, 480)
        glutCreateWindow("3D Modeler")
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutDisplayFunc(self.render)

    def init_opengl(self):
        """ Initialize OpenGL settings """
        self.model_view = np.identity(4)
        self.inverse_model_view = np.identity(4)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, GL_float(0, 0, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat(0, 0, -1))
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glClearColor(0.4, 0.4, 0.4, 0.4)

    def init_scene(self):
        """ Initialize the scene object and initial scene """
        self.scene = Scene()
        self.create_sample_scene()

    def create_sample_scene(self):
        cube = Cube()
        cube.translate(2, 0, 2)
        cube.color_index = 2
        self.scene.add_node(cube)

        sphere = Sphere()
        sphere.translate(-2, 0, 2)
        sphere.color_index = 3
        self.scene.add(sphere)

        snowman = Snowman()
        snowman.translate(-2, 0, -2)
        self.scene.add(snowman)

    def init_interaction(self):
        pass


if __name__=='__main__':
    viewer = Viewer()
