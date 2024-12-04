from bigbird_handler import BigBirdHandler

handler = BigBirdHandler()
# Simulate `ctx` initialization
class FakeContext:
    def __init__(self):
        self.system_properties = {"model_dir": "/Users/neeraj_py/Desktop/ApollosLyre/Backend/Serving/Model/big-bird"}

handler.initialize(FakeContext())
data = [{'body': [{'data': 'Your input text goes here.', "chapter": "Chapter1"}, {'data': 'Another input text.', "chapter": "Chapter2"}]}]
preprocessed = handler.preprocess(data)
outputs = handler.inference(preprocessed)
result = handler.postprocess(outputs, data)
print(result)
