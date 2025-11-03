from ..config import settings


from PIL import Image
from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
import re

class OCR:
    def __init__(self):
        self.model = settings.ocr_model_path

    def extract_text(self, image_path):
        TEST_IMAGE_PATH = image_path
        MODEL_PATH = self.model

        foundation_predictor  = FoundationPredictor(checkpoint=MODEL_PATH)
        recognition_predictor = RecognitionPredictor(foundation_predictor)
        detection_predictor = DetectionPredictor()

        image = Image.open(TEST_IMAGE_PATH).convert("RGB")
        predictions = recognition_predictor([image], det_predictor=detection_predictor)

        txt=""
        for line in predictions[0].text_lines:
            txt+= line.text
        return txt
    
    
    def ocr_bbox_(self, image_path,bboxes):
        image = Image.open(image_path)
        structured_result = []

        foundation_predictor = FoundationPredictor()
        recognition_predictor = RecognitionPredictor(foundation_predictor)
        detection_predictor = DetectionPredictor()

        for box in bboxes:
            x1, y1, x2, y2 = box
            cropped = image.crop((x1, y1, x2, y2))

            # det = detection_predictor([cropped])
            rec = recognition_predictor([cropped], det_predictor=detection_predictor)

            text = " ".join([line.text for line in rec[0].text_lines])
            structured_result.append({
                "text":  re.sub(r'<.*?>', '', text)
            })
            
        return structured_result