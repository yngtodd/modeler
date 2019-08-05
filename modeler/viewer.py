import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from modeler.api.scene import Scene

from modeler.primitives import Cube, Sphere
from modeler.composites import Snowman


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
        glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0, 0, -1))
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
        """ Initialize user interaction and callbacks """
        self.interaction = Interaction()
        self.interaction.register_callback('pick', self.pick)
        self.interactino.register_callback('move', self.move)
        self.interaction.register_callback('place', self.place)
        self.interaction.register_callback('rotate_color', self.rotate_color)
        self.interaction.register_callback('scale', self.scale)

    def render(self):
        """ The render pass for the scene """
        self.init_view()

        glEnable(GL_LIGHTING)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Load the modelview matrix from the current state of the trackball
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        loc = self.interaction.translation
        glTranslated(loc[0], loc[1], loc[2])
        glMultMatrixf(self.interaction.trackball.matrix)

        # Store the inverse of the current modelview
        current_model_view = np.array(glGetFloatv(GL_MODELVIEW_MATRIX))
        self.model_view = np.transpose(current_model_view)

        # Render all objects
        self.scene.render()

        glDisable(GL_LIGHTING)
        glCallList(G_OBJ_PLANE)
        glPopMatrix()

        # Flush the buffers so that the scene can be drawn.
        glFlush()

    def init_view(self):
        """ Initialize the projection matrix """
        x_size, y_size = glutGet(GLUT_WINDOW_WIDTH, glutGet(GLUT_WINDOW_HEIGHT))
        aspect_ratio = float(x_size) / float(y_size)

        # Load the projection matrix (always the same).
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glViewPort(0, 0, x_size, y_size)
        gluPerspective(70, aspect_ratio, 0.1, 1000.0)
        glTranslated(0, 0, -15)

    def get_ray(self, x, y):
        """ Generate a ray

        Ray will be begin at the near plane,
        in the direction of the x, y coordinates.

        Parameters
        ----------
        x : float
            X-coordinate of mouse position

        y : float
            Y-coordinate of mouse position

        Returns
        -------
        start : np.ndarray
            Start position of the ray

        direction : np.ndarray
            Direction of the array
        """
        self.init_view()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Get two points on the line
        start = np.array(gluUnProject(x, y, 0.001))
        end = np.array(dluUnProject(x, y, 0.999))

        # Convert start and end points to a ray
        direction = end - start
        direction = direction / norm(direction)

        return (start, direction)

    def pick(self, x, y):
        """ Execute pick of an object """
        start, direction = self.get_ray(x, y)
        self.scene.pick(start, direction, self.model_view)

    def move(self, x, y):
        """ Move an object in the scene """
        start, direction = self.get_ray(x, y)
        self.scene.move_selected(start, direction, self.inverse_model_view)

    def rotate_color(self, forward=True):
        """ Rotate the color of the selected node

        Parameters
        ----------
        forward : bool
            Indicates direction of the rotation
        """
        self.scene.rotate_selected_color(forward)

    def scale(self, up):
        """ Scale the selected node

        Parameters
        ----------
        up : bool
            Whether to increase the scale of the object
        """
        self.scene.scale_selected(up)

    def place(self, shape, x, y):
        """ Place a new primitive in the scene """
        start, direction = self.get_ray(x, y)
        self.scene.place(shape, start, direction, self.inverse_model_view)

    def main_loop():
        glutMainLoop()


if __name__=='__main__':
    viewer = Viewer()
    viewer.main_loop()
