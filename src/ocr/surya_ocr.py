from config import settings

import surya_ocr
from PIL import Image
from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
import os

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