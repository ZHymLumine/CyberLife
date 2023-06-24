import pinecone
import os
import pandas as pd
import ast
import timeit


class VectorDB:
    '''CyberWaifu's Brain, actually the interface of LLM.'''

    def __init__(self, embedding, save_path, vectorDB_api, vectorDB_env):
        self.embedding = embedding
        self.save_path = save_path
        pinecone.init(api_key=vectorDB_api, environment=vectorDB_env)
        active_indexes = pinecone.list_indexes()
        if not active_indexes:
            pinecone.create_index("cyberlife", dimension=384, metric="euclidean")
        self.index = pinecone.Index("cyberlife")
        #self.__initDB__()
    
    def __initDB__(self):
        # Load embeddings data
        if not os.path.isfile(self.save_path):
            return ['']
        memories = []
        with open(self.save_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                # 使用 rpartition 方法按照最后一个逗号进行分割
                before, sep, after = line.rpartition('|')
                print(f"Before the last comma: {before}")
                print(f"After the last comma: {after}")
                after = ast.literal_eval(after)
                memories.append((before, after))

        # Convert 'embedding' column (vectors in the form of strings) back to the original vector
        #df['embedding'] = df['embedding'].apply(ast.literal_eval) 
        for text, embedding in memories:
            print(type(text), type(embedding))
        # self.index.upsert(
        #     (memory[0], memory[1]) for memory in memories
        # )


    def store(self, text: str | list):
        #start_time = timeit.default_timer()
        print(text)
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
        
        self.index.upsert([
                (row['text'], row['embedding']) for i, row in df.iterrows()
            ])
        df.to_csv(self.save_path, mode='a', header=not os.path.exists(self.save_path), index=False)
        #end_time = timeit.default_timer()
        #execution_time = end_time - start_time


    def query(self, text: str, top_n: int, threshold: float = 0.7):
         # Make query
        #start_time = timeit.default_timer()
        query_embedding = self.embedding.embed_query(text)
        matches = self.index.query(
            vector=query_embedding,
            top_k=top_n,
            include_values=False
        )
        matches = matches['matches']
        strings = []
        relatednesses = []
        for match in matches:
            strings.append(match['id'])
            relatednesses.append(match['values'])

        #end_time = timeit.default_timer()
        #execution_time = end_time - start_time
        #print(f"VectorDB store ran for {execution_time} seconds.")
        return strings, matches
