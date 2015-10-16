
import cv2
import numpy as np
from GraphMaker import GraphMaker


class CutUI:

    def __init__(self, filename):
        self.graph_maker = GraphMaker(cv2.imread(filename))
        self.display_image = np.array(self.graph_maker.image)
        self.window = "Graph Cut"
        self.mode = self.graph_maker.foreground
        self.started_click = False

    def run(self):
        cv2.namedWindow(self.window)
        cv2.setMouseCallback(self.window, self.draw_line)

        while 1:
            display = cv2.addWeighted(self.display_image, 0.9, self.graph_maker.get_overlay(), 0.4, 0.1)
            cv2.imshow(self.window, display)
            key = cv2.waitKey(20) & 0xFF
            if key == 27:
                break
            elif key == ord('c'):
                self.graph_maker.clear_seeds()
            elif key == ord('g'):
                self.graph_maker.create_graph()
                self.graph_maker.swap_overlay(self.graph_maker.segmented)
            elif key == ord('t'):
                self.mode = 1 - self.mode
                self.graph_maker.swap_overlay(self.graph_maker.seeds)

        cv2.destroyAllWindows()

    def draw_line(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.started_click = True
            self.graph_maker.add_seed(x - 1, y - 1, self.mode)

        elif event == cv2.EVENT_LBUTTONUP:
            self.started_click = False

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.started_click:
                self.graph_maker.add_seed(x - 1, y - 1, self.mode)
