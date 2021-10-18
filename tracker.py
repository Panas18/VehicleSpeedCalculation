import math
import cv2
DISTANCE = 10


class EuclideanDistanceTracker:
    def __init__(self):
        self.count_id = 0
        self.center_dict = {}
        self.final_dict = {}
        self.final_dict_copy = {}

    def update(self, centers, img):
        object_center_ids = []

        for center in centers:
            same_object = False
            cx = center[0]
            cy = center[1]
            for id, ptx in self.center_dict.items():
                eculi_distance = math.hypot(cx - ptx[0], cy - ptx[1])
                if eculi_distance < 10:
                    self.center_dict[id] = (cx, cy)
                    object_center_ids.append([cx, cy, id])
                    same_object = True
                    break

            if same_object == False:
                self.center_dict[self.count_id] = (cx, cy)
                object_center_ids.append([cx, cy, self.count_id])
                self.count_id += 1
        new_center_point = {}
        for obj_center_id in object_center_ids:
            count = 1
            cx, cy,  obj_id = obj_center_id
            center = (cx, cy)
            new_center_point[obj_id] = (cx, cy)
            if obj_id in self.final_dict.keys():
                _, _, count = self.final_dict[obj_id]
                count += 1
                self.final_dict[obj_id] = (cx, cy, count)
            else:
                self.final_dict[obj_id] = (cx, cy, count)
        for id, ptx in self.final_dict_copy.items():
            after = self.final_dict[id]
            if after == ptx:
                time = (after[2]/29.7)/3600
                speed = round((10/1000)/time)
                text = f"{speed} Km/hr"
                print(f"Speed of the vehicle {id}: {speed:>2f}")
                cv2.putText(img, text, (ptx[0], ptx[1]),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255))
                self.final_dict.pop(id)
        self.final_dict_copy = self.final_dict.copy()
        self.center_dict = new_center_point.copy()

        return object_center_ids
