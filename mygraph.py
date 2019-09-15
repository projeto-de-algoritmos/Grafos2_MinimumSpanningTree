from pydotplus import Dot, Edge, Node, Cluster
from io import BytesIO
from PIL import Image
from os import path


class MyGraph:

    def __init__(self, *args, **kwargs):
        self._drawing = Dot(*args, **kwargs)
        self._adjs = {}
        self._marked = {}
        self._frames = []
    
    def get_node(self, name):
        return self._drawing.get_node(str(name))[0]

    def make_node(self, name):
        return Node(
            name,
            shape='none',
            style='filled',
            color='azure2',
            image='voter.png',
            labelloc='b',
            fontname="Times-Roman:bold",
            fixedsize='true',
            width=1.0,
            height=1.0,
            fontcolor='white',
            fontsize=15,
        )

    def add_nodes(self, *nodes_names):
        this_path = path.dirname(__file__)
        this_path = path.join(this_path, 'images', 'voter.png')

        self._drawing.shape_files = [this_path]
        
        for name in nodes_names:
            node = self.make_node(name)

            self._drawing.add_node(node)
            self._adjs[name] = []
            self._marked[name] = False

    def link(self, src, dst):
        self._adjs[src].append(dst)
        self._adjs[dst].append(src)

        src = self.get_node(src)
        dst = self.get_node(dst)
        self._drawing.add_edge(Edge(src, dst))

        self._frames.append(self.get_image())

    def get_image(self):
        img = self._drawing.create_png()
        stream = BytesIO(img)
        img = Image.open(stream)

        return img

    def save_img(self, img_name):
        self._frames[-1].save(
            img_name + '.png',
            format="PNG",
        )

