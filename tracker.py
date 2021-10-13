import math
import cv2
import sys


class EuclideanDistanceTracker:
    def __init__(self):
        self.count_id = 0
        self.center_dict = {}
        self.frame_count = 0

    def update(self, centers):
        same_object = False
        object_center_ids = []
        for center in centers:
            cx = center[0]
            cy = center[1]
            for id, ptx in self.center_dict.items():
                eculi_distance = math.hypot(cx - ptx[0], cy - ptx[1])
                if eculi_distance < 10:
                    self.center_dict[id] = (cx, cy)
                    #print(self.center_dict)
                    object_center_ids.append([cx, cy, id])
                    same_object = True
                    break

            if same_object == False:
                self.center_dict[self.count_id] = (cx, cy)
                object_center_ids.append([cx, cy, self.count_id])
                self.count_id += 1

        new_center_point = {}
        for obj_center_id in object_center_ids:
            cx, cy,  obj_id = obj_center_id
            center = (cx, cy)
            new_center_point[obj_id] = (cx, cy)

        self.center_dict = new_center_point.copy()
        return object_center_ids
