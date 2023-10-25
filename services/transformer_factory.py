from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoModelForSeq2SeqLM, AutoModelForCausalLM, T5ForConditionalGeneration, BartForConditionalGeneration, AutoTokenizer


class TransformerFactory:
    factory_funcs = {
        'sentence_transformer': SentenceTransformer,
        'auto_model': AutoModel.from_pretrained,
        'auto_model_seq_2_seq': AutoModelForSeq2SeqLM.from_pretrained,
        'auto_model_causal': AutoModelForCausalLM.from_pretrained,
        'bart_for_conditional_generation': BartForConditionalGeneration.from_pretrained,
        't5_for_conditional_generation': T5ForConditionalGeneration.from_pretrained
    }
    models = {factory_func_name: {} for factory_func_name in factory_funcs.keys()}
    tokenizers = {}

    @classmethod
    def create_model(cls, factory_func_name: str, model_name: str) -> object:
        if factory_func_name not in cls.factory_funcs.keys():
            raise ValueError(f'Invalid Parameter: factory_func_name should be one of the following: {cls.factory_funcs.keys()}')
        
        try:
            model = cls.factory_funcs.get(factory_func_name)(model_name)
        except:
            raise ValueError(f'Invalid Parameter: model_name')
        
        return model
    
    @classmethod
    def get_model(cls, factory_func_name: str, model_name: str) -> object:
        model = cls.models.get(factory_func_name, {}).get(model_name)

        if not model:
            model = cls.create_model(factory_func_name, model_name)
            cls.models[factory_func_name][model_name] = model

        return model

    @classmethod
    def create_tokenizer(cls, model_name):
        return AutoTokenizer.from_pretrained(model_name)
    
    @classmethod
    def get_tokenizer(cls, model_name):
        tokenizer = cls.tokenizers.get(model_name)

        if not tokenizer:
            tokenizer = cls.create_tokenizer(model_name)
            cls.tokenizers[model_name] = tokenizer

        return tokenizer
    

