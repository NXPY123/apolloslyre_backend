import json
import torch
from transformers import BigBirdForSequenceClassification, BigBirdTokenizer

class BigBirdHandler:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def initialize(self, ctx):
        model_dir = ctx.system_properties.get("model_dir")
        self.model = BigBirdForSequenceClassification.from_pretrained(model_dir)
        self.tokenizer = BigBirdTokenizer.from_pretrained(model_dir)
        self.model.eval()

    def preprocess(self, data):
        print("PREPROCESSING")
        print(data)
        texts = [item["data"] for item in data[0]["body"]]
        return self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

    def inference(self, inputs):
        print("INFERENCE")
        print(inputs)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)
        return predictions.tolist()

    def postprocess(self, inference_output):
        print("POSTPROCESSING")
        print(inference_output)
        return [{"label": pred} for pred in inference_output]

    def handle(self, data, context):
        """Handle the incoming request."""
        try:
            print("HANDLING")
            print(data)
            # Step 1: Preprocess the input data
            inputs = self.preprocess(data)
            
            # Step 2: Perform inference
            outputs = self.inference(inputs)
            
            # Step 3: Postprocess the results
            return [self.postprocess(outputs)]
        except Exception as e:
            raise ValueError(f"Error during model inference: {e}")
