from ..config import settings
import ollama

class Generator:
    def __init__(self,gen_model_name:str=settings.ollama_model_name):
        self.gen_model_name = gen_model_name
        
    def generate_respose(self,context:str, prompt:str):
        prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"
        gen_response=ollama.generate(model=self.gen_model_name, prompt=prompt)
        if gen_response['response'] is None:
            raise ValueError("Response generation failed.")
        return gen_response['response']
