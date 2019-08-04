import sys


class Scene:
    """ Base class for scenes """

    # Default depth for the camera
    PLACE_DEPTH = 15

    def __init__(self):
        self.reset()

    def reset(self):
        self.node_list = []
        self.selected_node = None

    def add_node(self, node):
        self.node_list.append(node)

    def render(self):
        """ Render the scene """
        for node in self.node_list:
            node.render()

    def pick(self, start, direction, mat):
        """ Execute selection

        Parameters
        ----------
        start : np.ndarray
            Starting point of a ray
        
        direction : np.ndarray
            Direction of the ray

        mat : np.ndarray
            Inverse of the current model_view matrix of the scene
        """
        if selected_node is not None:
            self.selected_node.select(False)
            self.selected_node = None

        # Keep track of the closest ray intersection
        min_dist = sys.maxint
        nearest_node = None
        for node in self.node_list:
            hit, distance = node.pick(start, direction, mat)
            if hit and distance < min_dist:
                min_dist, nearest_node = distance, node
        
        # If we hit something, keep track of it
        if nearest_node is not None:
            nearest_node.select()
            nearest_node.depth = min_dist
            nearest_node.selected_loc = start + direction * min_dist
            self.selected_node = nearest_node
    
    def rotate_selected_color(self, forwards):
        """ Rotate the color of the currently selected node """
        if self.selected_node is None: return
        self.selected_node.rotate_color(forwards)

    def scale_selected(self, up):
        """ Scale the current selection """
        if self.selected_node is None: return
        self.selected_node.scale(up)

    def move_selected(self, start, direction, inv_model_view):
        """ Move the selected object in the scene 

        Parameters
        ----------
        start : np.ndarray
            Starting point of the ray to move along

        direction : np.ndarray
            Direction of the ray to move along

        inv_model_view:
            inverse of the modelview matrix for the scene
        """
        if self.selected_node is None: return

        # Find the current location and depth of the selected node
        node = self.selected_node
        dept = node.depth
        old_loc = node.selected_loc

        # The location of the node is the same depth along the new ray
        new_loc = (start + direction * depth)

        # Transform the translation with the model_view_matrix
        translation = new_loc - old_loc
        pre_translation = np.array([translation[0], translation[1], translation[2]])
        translation = inv_model_view.dot(pre_translation)

        # Translate the node and track its location
        node.translate(translation[0], translation[1], translation[2])
        node.selected_loc(new_loc)