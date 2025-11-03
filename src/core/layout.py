from PIL import Image
from surya.foundation import FoundationPredictor
from surya.layout import LayoutPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
from surya.settings import settings


class LayoutAnalyzer:
    
    def __init__(self):
        self.model_checkpoint = settings.LAYOUT_MODEL_CHECKPOINT
    
    
    def analyze_layout(self, image_path):
        image = Image.open(image_path)
        layout_predictor = LayoutPredictor(FoundationPredictor(checkpoint=self.model_checkpoint))
        layout_predictions = layout_predictor([image])
        return layout_predictions
