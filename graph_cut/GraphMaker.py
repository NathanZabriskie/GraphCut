
import cv2
import numpy as np
import maxflow


class GraphMaker:

    foreground = 1
    background = 0
    default = 0.5
    MAXIMUM = 1000000000

    def __init__(self, image):
        self.image = image
        self.graph = np.zeros_like(self.image.shape)
        self.overlay = np.zeros_like(self.image)
        self.background_seeds = []
        self.foreground_seeds = []
        self.background_average = np.array(3)
        self.foreground_average = np.array(3)
        self.nodes = []
        self.edges = []
        self.segmented = np.zeros_like(self.image)

    def add_seed(self, x, y, type):
        if type == self.background:
            if not self.background_seeds.__contains__((x, y)):
                self.background_seeds.append((x, y))
                cv2.rectangle(self.overlay, (x-1, y-1), (x+1, y+1), (0, 0, 255), -1)
        elif type == self.foreground:
            if not self.foreground_seeds.__contains__((x, y)):
                self.foreground_seeds.append((x, y))
                cv2.rectangle(self.overlay, (x-1, y-1), (x+1, y+1), (0, 255, 0), -1)

    def clear_seeds(self):
        self.background_seeds = []
        self.foreground_seeds = []
        self.overlay = np.zeros_like(self.overlay)

    def create_graph(self):
        if len(self.background_seeds) == 0 or len(self.foreground_seeds) == 0:
            print "Please enter at least one foreground and background seed."
            return

        print "Making graph"
        print "Finding foreground and background averages"
        self.find_averages()

        print "Populating nodes and edges"
        self.populate_graph()

        print "Cutting graph"
        self.cut_graph()

    def find_averages(self):
        self.graph = np.zeros((self.image.shape[0], self.image.shape[1]))
        self.graph.fill(self.default)
        self.background_average = np.zeros(3)
        self.foreground_average = np.zeros(3)

        for coordinate in self.background_seeds:
            self.graph[coordinate[1], coordinate[0]] = 0
            self.background_average += self.image[coordinate[1], coordinate[0]]

        self.background_average /= len(self.background_seeds)

        for coordinate in self.foreground_seeds:
            self.graph[coordinate[1], coordinate[0]] = 1
            self.foreground_average += self.image[coordinate[1], coordinate[0]]

        self.foreground_average /= len(self.foreground_seeds)

    def populate_graph(self):
        self.nodes = []
        self.edges = []

        # make all s and t connections for the graph
        for (y, x), value in np.ndenumerate(self.graph):
            # this is a background pixel
            if value == 0.0:
                self.nodes.append((self.get_node_num(x, y, self.image.shape), self.MAXIMUM, 0))

            # this is a foreground node
            elif value == 1.0:
                self.nodes.append((self.get_node_num(x, y, self.image.shape), 0, self.MAXIMUM))

            else:
                d_f = np.power(self.image[y, x] - self.foreground_average, 2)
                d_b = np.power(self.image[y, x] - self.background_average, 2)
                d_f = np.sum(d_f)
                d_b = np.sum(d_b)
                e_f = d_f / (d_f + d_b)
                e_b = d_b / (d_f + d_b)
                self.nodes.append((self.get_node_num(x, y, self.image.shape), e_f, e_b))

                if e_f > e_b:
                    self.graph[y, x] = 1.0
                else:
                    self.graph[y, x] = 0.0

        for (y, x), value in np.ndenumerate(self.graph):
            if y == self.graph.shape[1] - 1 or x == self.graph.shape[0] - 1:
                continue
            my_index = self.get_node_num(x, y, self.image.shape)

            neighbor_index = self.get_node_num(x+1, y, self.image.shape)
            g = 1 / (1 + np.sqrt(np.sum(np.power(self.image[y, x] - self.image[y, x+1], 2))))
            self.edges.append((my_index, neighbor_index, np.abs(self.graph[y, x] - self.graph[y, x+1]) * g))

            neighbor_index = self.get_node_num(x, y+1, self.image.shape)
            g = 1 / (1 + np.sqrt(np.sum(np.power(self.image[y, x] - self.image[y+1, x], 2))))
            self.edges.append((my_index, neighbor_index, np.abs(self.graph[y, x] - self.graph[y+1, x]) * g))

    def cut_graph(self):
        g = maxflow.Graph[float](len(self.nodes), len(self.edges))
        nodelist = g.add_nodes(len(self.nodes))

        for node in self.nodes:
            g.add_tedge(nodelist[node[0]], node[1], node[2])

        for edge in self.edges:
            g.add_edge(edge[0], edge[1], edge[2], edge[2])

        flow = g.maxflow()

        self.segmented = np.zeros((self.image.shape[0], self.image.shape[1]))
        for index in nodelist:
            self.segmented[self.get_xy(index, self.image.shape)] = g.get_segment(nodelist[index])

        cv2.imwrite("output/cool.png", self.segmented)

    @staticmethod
    def get_node_num(x, y, array_shape):
        return y * array_shape[0] + x

    @staticmethod
    def get_xy(nodenum, array_shape):
        return nodenum % array_shape[0], nodenum / array_shape[0]