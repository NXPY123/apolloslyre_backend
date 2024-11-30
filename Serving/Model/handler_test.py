from bigbird_handler import BigBirdHandler

handler = BigBirdHandler()
# Simulate `ctx` initialization
class FakeContext:
    def __init__(self):
        self.system_properties = {"model_dir": "./big-bird"}

handler.initialize(FakeContext())
data = [{'body': [['Chapter1', 'Your input text goes here.'], ['Chapter2', 'Another input text.']]}]
result = handler.handle(data, None)
print(result)
