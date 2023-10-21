from sentence_transformers import SentenceTransformer


class SentenceTransformerProvider:
    ml_models = {}

    @classmethod
    def get_model(cls, model_name) -> SentenceTransformer:
        model = cls.ml_models.get(model_name)

        if not model:
            model = SentenceTransformer(model_name)
            cls.ml_models[model_name] = model

        return model