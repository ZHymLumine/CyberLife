"""
Store memory vector, and extract top_n relevant memories
"""
import pandas as pd
import os
import ast
from scipy import spatial
import timeit


class SimpleDB:
    def __init__(self, embedding, save_path):
        self.save_path = save_path
        self.embedding = embedding
        self.chunks    = []


    def store(self, text: str | list):
        '''save vector'''
        #start_time = timeit.default_timer()
        if isinstance(text, str):
            if text == '':
                return
            vector = self.embedding.embed_documents([text])
            df = pd.DataFrame({"text": text, "embedding": vector})
        elif isinstance(text, list):
            if len(text) == 0:
                return
            vector = self.embedding.embed_documents(text)
            df = pd.DataFrame({"text": text, "embedding": vector})
        else:
            raise TypeError('text must be str or list')
        df.to_csv(self.save_path, mode='a', header=not os.path.exists(self.save_path), index=False)
        # end_time = timeit.default_timer()
        # execution_time = end_time - start_time
        # print(f"SimpleDB store ran for {execution_time} seconds.")
        

    def query(self, text: str, top_n: int, threshold: float = 0.7):
        #start_time = timeit.default_timer()
        if text == '':
            return ['']
        relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y)

        # Load embeddings data
        if not os.path.isfile(self.save_path):
            return ['']
        df = pd.read_csv(self.save_path)

        row = df.shape[0]
        top_n = min(top_n, row)
        
        # Convert 'embedding' column (vectors in the form of strings) back to the original vector
        df['embedding'] = df['embedding'].apply(ast.literal_eval) 

        # Make query
        query_embedding = self.embedding.embed_query(text)
        strings_and_relatednesses = [
            (row["text"], relatedness_fn(query_embedding, row["embedding"]))
            for i, row in df.iterrows()
        ]

        # Rank
        strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
        strings, relatednesses = zip(*strings_and_relatednesses)
        for i in range(len(relatednesses)):
            if relatednesses[i] < threshold:
                break
        # end_time = timeit.default_timer()
        # execution_time = end_time - start_time
        # print(f"SimpleDB query ran for {execution_time} seconds.")
        return strings[:min(i+1, top_n)], relatednesses[:min(i+1, top_n)]