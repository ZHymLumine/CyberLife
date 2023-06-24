from sentence_transformers import SentenceTransformer, util

from termcolor import colored

class STEmbedding():
    '''Wraper of Sentence Transformer Eembedding'''

    def __init__(self):
        try:
            self.model = SentenceTransformer('./st_model/')
        except:
            print(colored('Sentence Transformer failed to load model!', 'red'))


    def embed_documents(self, documents: list):
        '''return embedding vector'''
        return list(self.model.encode(documents).tolist())


    def embed_query(self, text: str):
        return self.model.encode(text, show_progress_bar=False).tolist()