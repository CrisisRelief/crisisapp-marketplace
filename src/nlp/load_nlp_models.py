from src.common.fricles_logger import *
from singleton_decorator import singleton
from sent2vec import Sent2vecModel

@singleton
class load_models(object):

    def __init__(self):
        return

    def load_sent2vec_model(self):

        model_path = "/Users/cganjihal/repo/QBit/models/torontobooks_unigrams.bin"

        fricles_logger.info('Loading sent2vec model ' + model_path)
        model = Sent2vecModel()
        # This will exit the process if the model can't be loaded; no Exception to catch.
        try:
            model.load_model(model_path)
        except Exception as e:
            fricles_logger.debug(f'Failed to load sent2vec model')
        return model
