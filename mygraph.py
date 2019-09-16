from pydotplus import Dot, Edge, Node, Cluster
from io import BytesIO
from PIL import Image
from os import path


class MyGraph:

    def __init__(self, *args, **kwargs):
        self._drawing = Dot(*args, **kwargs)
        self._frames = []
    
    def get_node(self, name):
        return self._drawing.get_node(str(name))[0]

    def make_node(self, name):
        return Node(
            name,
            style='filled',
            color='turquoise',
            labelloc='b',
            fontname="Times-Roman:bold",
            fontcolor='black',
            fontsize=40,
        )

    def add_nodes(self, *nodes_names):
        #this_path = path.dirname(__file__)
        #this_path = path.join(this_path, 'images', 'voter.png')

        #self._drawing.shape_files = [this_path]
        
        for name in nodes_names:
            node = self.make_node(name)

            self._drawing.add_node(node)

    def link(self, src, dst, label_edge):
        if label_edge is "any":
            font_color = "darkgreen"
        elif label_edge is "none":
            font_color = "red"
        else:
            font_color = "indigo"

        self._drawing.add_edge(Edge(src, dst, label=label_edge, fontcolor=font_color, fontsize=40))


    def get_image(self):
        img = self._drawing.create_png()
        stream = BytesIO(img)
        img = Image.open(stream)

        return img

    def save_img(self, img_name):
        self._frames.append(self.get_image())
        self._frames[-1].save(
            img_name + '.png',
            format="PNG",
        )

