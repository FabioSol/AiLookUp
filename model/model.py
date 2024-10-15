from sentence_transformers import SentenceTransformer
from model import model_path


class Model:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'model'):
            self.model = SentenceTransformer.load(model_path)

    def encode(self, sentences):
        return self.model.encode(sentences)


if __name__=='__main__':
    model = Model()
    print(model.encode(["sdfghjkl"]).shape)