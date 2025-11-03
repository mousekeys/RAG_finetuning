import numpy as np

class OCRBBoxProcessor:
    # def __init__(self, ocr):
    #     self.ocr = ocr


    def expand_boxes_y(self, boxes: list[list[float]], y_expand:int =5, x_expand:int =3, img_height:int =None):
        """
        Expands each box vertically by y_expand pixels.
        
        Args:
            boxes (List[List[float]]): List of [x1, y1, x2, y2] boxes.
            y_expand (float): Pixels to expand upward and downward.
            img_height (float, optional): If provided, ensures boxes stay within image height.

        Returns:
            List[List[float]]: Vertically expanded boxes.
        """
        expanded = []
        for box in boxes:
            x1, y1, x2, y2 = box
            new_x1 = max(0, x1 - x_expand)
            new_x2 = x2 + x_expand
            new_y1 = max(0, y1 - y_expand)
            new_y2 = y2 + y_expand
            
            if img_height is not None:
                new_y2 = min(img_height, new_y2)

            expanded.append([new_x1, new_y1, new_x2, new_y2])

        return expanded

    def merge_boxes_iterative(self, boxes: list[list[float]], iou_threshold:int =0.5, proximity_threshold:int =2):
        """
        Iteratively merge boxes that overlap or are vertically close until stable.
        
        Args:
            boxes (List[List[float]]): List of [x1, y1, x2, y2] boxes.
            iou_threshold (float): IOU threshold for merging.
            proximity_threshold (float): Vertical proximity threshold (px).
        
        Returns:
            List[List[float]]: List of merged boxes.
        """
        
        
        def iou(boxA, boxB):
            # Intersection
            xA = max(boxA[0], boxB[0])
            yA = max(boxA[1], boxB[1])
            xB = min(boxA[2], boxB[2])
            yB = min(boxA[3], boxB[3])
            interW = max(0, xB - xA)
            interH = max(0, yB - yA)
            interArea = interW * interH
            
            # Union
            boxAArea = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
            boxBArea = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])
            unionArea = boxAArea + boxBArea - interArea
            
            return interArea / unionArea if unionArea > 0 else 0
        
        boxes = [list(b) for b in boxes]  # copy
        changed = True
        
        while changed:
            changed = False
            new_boxes = []
            used = [False] * len(boxes)
            
            for i, boxA in enumerate(boxes):
                if used[i]:
                    continue
                merged = boxA.copy()
                for j, boxB in enumerate(boxes):
                    if i == j or used[j]:
                        continue
                    if iou(merged, boxB) > iou_threshold or \
                    abs(merged[1] - boxB[3]) < proximity_threshold or \
                    abs(merged[3] - boxB[1]) < proximity_threshold:
                        merged[0] = min(merged[0], boxB[0])
                        merged[1] = min(merged[1], boxB[1])
                        merged[2] = max(merged[2], boxB[2])
                        merged[3] = max(merged[3], boxB[3])
                        used[j] = True
                        changed = True
                new_boxes.append(merged)
                used[i] = True
            boxes = new_boxes
        return boxes
