from pyexpat.errors import messages
from ..config import settings
import ollama
from PIL import Image
from ollama import chat


class Generator:
    def __init__(self,gen_model_name:str=settings.ollama_model_name):
        self.gen_model_name = gen_model_name
        
    def generate_respose(self,context:str, prompt:str):
        prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"
        gen_response=ollama.generate(model=self.gen_model_name, prompt=prompt)
        # if gen_response['response'] is None:
        #     raise ValueError("Response generation failed.")
        return gen_response['response']
    
    def ocrimg_kvp_extraction(self,image_path:str):
        image = Image.open(image_path).convert("RGB")
        messages = [
        {
                "role": "user",
                "content":  "Extract key-value pairs from the above image of a transaction. Provide the output in JSON format with keys",
                "image": image  
                
            }
        ]

        gen_response = chat(model=self.gen_model_name, messages=messages)
        return gen_response['message']['content']

    def text_kvp_extraction(self,text:str):
        prompt = f"Extract key-value pairs from the following text of a transaction. Provide the output in JSON format with keys. Provide only the json formatted output.\n\nText: {text}"
        gen_response=ollama.generate(model=self.gen_model_name, prompt=prompt)
        return gen_response['response']
        
        
        

