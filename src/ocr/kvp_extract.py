from ..core.generator import Generator
from .ocrsurya import OCR
from ..config import settings
import ollama
from ..core.layout import LayoutAnalyzer
from .bbox import OCRBBoxProcessor
from .ocrsurya import OCR

import re
from datetime import datetime


layout=LayoutAnalyzer()
bbox_processor = OCRBBoxProcessor()
ocr_text_extractor = OCR()

class OCRKVPExtractor:
    def __init__(self):
        self.generator = Generator()
        self.ocr=OCR()
        self.gen_model_name = settings.ollama_model_name
    
    def parse_kvp_response(self, structured_result):
        def extract_value(label, text):
            match = text.replace(label,"",1)
            if match:
                return match
            return ""

        kvpair = {}

        kvpair['Description'] = structured_result[0]['text']
        kvpair["Reference Code"] = int(extract_value("Reference Code", structured_result[1]['text']))

        date_str = extract_value("Date/Time", structured_result[2]['text'])[:-1]
        date_obj = datetime.strptime(date_str, '%d %b %Y,%I:%M %p')
        kvpair["Date/Time"] = date_obj

        kvpair["Channel"] = extract_value("Channel", structured_result[3]['text'])
        kvpair["Payment Attribute"] = extract_value("Payment Attribute", structured_result[4]['text'])
        kvpair["Service Name"] = extract_value("Service Name", structured_result[5]['text'])
        kvpair["Amount (NPR)"] = float(extract_value("Amount (NPR)", structured_result[6]['text']))
        kvpair["Initiator"] = extract_value("Initiator", structured_result[7]['text'])
        kvpair["Qr Merchant Name"] = extract_value("Qr Merchant Name", structured_result[8]['text'])

        kvpair["Remarks"] = extract_value("Remarks", structured_result[9]['text'])
        kvpair["Status"] = extract_value("Status", structured_result[10 ]['text'])
        
        return kvpair

    def ocr_kvp_extraction(self, image_path:str="/home/sinju/Documents/Money_tracker/tes1.jpg"):
        text=self.ocr.extract_text(image_path=image_path)
        response = self.generator.text_kvp_extraction(text=text)
        return response
    
    def ocr_kvp_extraction_with_model(self, image_path:str="/home/sinju/Documents/Money_tracker/tes1.jpg"):
        response = self.generator.ocr_kvp_extraction(image_path=image_path)
        return response

    def ocr_kvp_extraction_with_layout(self, image_path:str="/home/sinju/Documents/Money_tracker/tes1.jpg"):
        layout_predictions = layout.analyze_layout(image_path=image_path)
        boxes = [box.bbox for box in layout_predictions[0].bboxes if box.label == "Text"]
        merged_boxes = bbox_processor.merge_boxes_iterative(boxes, iou_threshold=0.5, proximity_threshold=20)
        final_bbox=bbox_processor.expand_boxes_y(merged_boxes, y_expand=6, x_expand=10)
        output_dict=ocr_text_extractor.ocr_bbox_(image_path=image_path,bboxes=final_bbox)
        kvp_extract = self.parse_kvp_response(output_dict)
        return kvp_extract

if __name__ == "__main__":
    ocr_extractor = OCRKVPExtractor()
    result = ocr_extractor.ocr_kvp_extraction_with_layout()
    print("Extracted Key-Value Pairs:", result)
