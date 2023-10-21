from sentence_transformers import SentenceTransformer


class SentenceTransformerProvider:
    models = {}

    @classmethod
    def get_model(cls, model_name) -> SentenceTransformer:
        model = cls.models.get(model_name)

        if not model:
            model = SentenceTransformer(model_name)
            cls.models[model_name] = model

        return model