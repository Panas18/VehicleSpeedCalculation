import math


class EuclideanDistanceTracker:
    def __init__(self):
        self.count_id = 0
        self.center_dict = {}
        self.final_dict = {}
        self.final_dict_copy = {}

    def update(self, centers):
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
            #print(f"After{after}, Prev:{ptx}")
            if after == ptx:
                print(f"Vehicle {id} took {after[2]} Frame")
                self.final_dict.pop(id)
        # print(self.final_dict)
        self.final_dict_copy = self.final_dict.copy()
        self.center_dict = new_center_point.copy()

        return object_center_ids
