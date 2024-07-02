from transformers import BigBirdForSequenceClassification, BigBirdTokenizer

model = None
tokenizer = None

def init_model_and_tokenizer(model_path):
    global model
    global tokenizer
    model = BigBirdForSequenceClassification.from_pretrained(model_path)
    tokenizer = BigBirdTokenizer.from_pretrained(model_path)