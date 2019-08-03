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
