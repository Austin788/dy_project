import os
import cv2
import json


def illgeal(mask, index_x, index_y):
    if index_y >= 0 and index_y < mask.shape[0] and index_x >= 0 and index_x < mask.shape[1]:
        return True
    return False

def search_box(mask):
    for index_x1 in range(0, mask.shape[1]):
        for index_y1 in range(0, mask.shape[0]):
            if mask[index_y1, index_x1] == 255:
                for index_x2 in range(index_x1 + 1, mask.shape[1]):
                    if mask[index_y1, index_x2] == 0:
                        index_x2 = index_x2-1
                        for index_y2 in range(index_y1 + 1, mask.shape[0]):
                            if mask[index_y2, index_x2] == 0:
                                index_y2 = index_y2 - 1
                                return index_x1, index_y1, index_x2, index_y2

    return -1, -1, -1, -1


def make_config(template_path, template_mask_path):
    template_mask = cv2.imread(template_mask_path, cv2.IMREAD_UNCHANGED)
    _, mask_blur = cv2.threshold(template_mask[:, :, -1], 200, 255, cv2.THRESH_BINARY)

    template = cv2.imread(template_path)
    template2 = template.copy()
    boxes = []
    while True:
        x1, y1, x2, y2 = search_box(mask_blur)
        print(x1, y1, x2, y2)
        if x1 == -1:
            break
        boxes.append([x1, y1, x2, y2])
        mask_blur[y1:y2+1, x1:x2+1] = 0

    for i, box in enumerate(boxes):
        cv2.putText(template, str(i + 1), (int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))

    template_show = cv2.resize(template, (500, 800))
    cv2.imshow("box order", template_show)
    order = []
    for i in range(len(boxes)):
        key = cv2.waitKey(-1)
        order.append(int(key) - 48)

    boxes_new = []
    for index in order:
        boxes_new.append(boxes[index - 1])

    for i, box in enumerate(boxes_new):
        cv2.putText(template2, str(i + 1), (int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
    template_show2 = cv2.resize(template2, (500, 800))
    cv2.imshow("image index", template_show2)

    image_indexes = []
    for i in range(len(boxes)):
        key = cv2.waitKey(-1)
        image_indexes.append(int(key) - 49)

    with open(template_path[:-4]+".config", "w") as f:
        data = {}
        data['img_num'] = len(set(image_indexes))
        boxes = []
        for image_index, box in zip(image_indexes, boxes_new):
            boxes.append({"box": box, "image_index": image_index})
        data['boxes'] = boxes

        json.dump(data, f, indent=4)

if __name__ == "__main__":
    template_path = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/template/情侣6图.png"
    template_box_path = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/template/情侣6图_box.png"

    make_config(template_path, template_box_path)
