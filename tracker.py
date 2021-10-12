import math
import sys


class EuclideanDistanceTracker:
    def __init__(self):
        self.count_id= 0
        self.center_dict = {}

    def update(self, centers):
        same_object = False
        for center in centers:
            cx = center[0]
            cy = center[1]
            for id, ptx in self.center_dict.items():
                eculi_distance = math.hypot(cx - ptx[0], cy - ptx[1])
                #print(eculi_distance)

                if eculi_distance < 7.5:
                    self.center_dict[id] = (cx, cy) 
                    print(self.center_dict)
                    print("\n")
                    same_object = True
                    break

            if same_object == False:
                self.center_dict[self.count_id] = (cx, cy)
                self.count_id += 1
        