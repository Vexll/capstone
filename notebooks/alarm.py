from queue import Queue


class AlarmDetector:
    def __init__(self, model, max_frames, limit):
        self.q = Queue()
        self.drowning_dict = dict()
        self.model = model
        self.max_frames = max_frames
        self.limit = limit
        self.frames = 0

    def check_alarm(self):
        for num_frames in self.drowning_dict.values():
            if num_frames > self.limit:
                return True
        return False

    def remove_excess(self):
        if self.frames > self.max_frames:
            self.frames -= 1
            objects = self.q.get()
            for obj_id, obj_class in objects.items():
                name = self.model.names[obj_class]
                print(name)
                if name == 'drowning':
                    self.drowning_dict[obj_id] -= 1

    def add(self, objects):
        self.q.put(objects)
        self.frames += 1
        for obj_id, obj_class in objects.items():
            name = self.model.names[obj_class]
            print(name)
            if name == 'Drowning':
                if obj_id not in self.drowning_dict:
                    self.drowning_dict[obj_id] = 1
                else:
                    self.drowning_dict[obj_id] += 1

    def add_boxes(self, boxes):
        objects = dict()
        for box in boxes:
            obj_id, obj_cls = box.id, int(box.cls)
            name = self.model.names[obj_cls]
            if name == 'Drowning':
                objects[1] = obj_cls
                break
        self.add(objects)
        self.remove_excess()
