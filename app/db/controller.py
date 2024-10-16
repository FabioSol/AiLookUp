import os.path

import numpy as np
import pandas as pd
from peewee import JOIN, Database

from app.db.schema import File,FileRow,Vector
from app.db import files_path
from app.model.model import Model
import ast


class FileController:
    def __init__(self, df,file_name, file_type, description_cols, file_id):
        self.df = df
        self.file_name = file_name
        self.file_type = file_type
        self.description_cols = description_cols
        self.file_id = file_id
        self.embeddings_model = None

    @classmethod
    def find(cls, file_name):
        if os.path.exists(files_path + file_name):
            if file_name.endswith('.csv'):
                file_type = "csv"
                df = pd.read_csv(files_path + file_name,index_col=0)
            elif file_name.endswith('.xlsx'):
                file_type = "xlsx"
                df = pd.read_excel(files_path + file_name,index_col=0)
            else:
                raise ValueError("File name should include extension csv or xlsx")
        else:
            raise FileNotFoundError("File not found")

        query = File.select().where(File.name == file_name)
        if query.exists():
            file = query.get()
            description_cols = ast.literal_eval(file.description_col)
            file_id = file.id
        else:
            raise FileNotFoundError("File not found")
        return cls(df, file_name, file_type, description_cols, file_id)


    @classmethod
    def new(cls, path:str, description_cols:list[str]):
        if not File.select().where(File.name == path.split("/")[-1]).exists():
            file_name= path.split('/')[-1]
        else:
            slash='/'
            raise ValueError(f'File name "{path.split(slash)[-1]}" already in use')
        if path.endswith('.csv'):
            file_type = "csv"
            df = pd.read_csv(path)
        elif path.endswith('.xlsx'):
            file_type = "xlsx"
            df = pd.read_excel(path)
        else:
            dot = '.'
            raise NotImplementedError(f'File type "{path.split(dot)[-1]}" not supported')

        if all([description_col in df.columns for description_col in description_cols]):
            description_cols = description_cols
        else:
            raise ValueError(f'Column "{description_cols}" not found in dataframe')

        file_id = None
        return cls(df, file_name, file_type, description_cols,file_id)


    def save_file(self):
        if self.file_type == "csv":
            self.df.to_csv(files_path+self.file_name)
        elif self.file_type == "xlsx":
            self.df.to_excel(files_path+self.file_name)
        else:
            raise NotImplementedError(f'File type {self.file_type} not supported')

    def save_filename(self):
        self.file_id = File.create(name=self.file_name, description_col = str(self.description_cols))

    def save_rows(self):
        description_series = self.df.apply(lambda row: " ".join([row[description_col] for description_col in self.description_cols]), axis=1)
        if self.embeddings_model is None:
            self.embeddings_model = Model()
        embeddings = self.embeddings_model.encode(description_series.values)
        for idx, vec in enumerate(embeddings):
            v_id = Vector.create(vector=vec)
            FileRow.create(file_id=self.file_id, row_id=idx, vector_id=v_id)

    def save(self):
        self.save_filename()
        self.save_file()
        self.save_rows()

    def get_vectors(self):
        query = (
            Vector
            .select(Vector.vector)
            .join(FileRow, JOIN.LEFT_OUTER, on=FileRow.vector_id == Vector.id)
            .where(FileRow.file_id == self.file_id)
            .order_by(FileRow.row_id.asc())
        )
        return np.array([np.frombuffer(row.vector, dtype=np.float32) for row in query])

    def get_similarity(self,prompt):
        if self.embeddings_model is None:
            self.embeddings_model = Model()
        v1 = self.embeddings_model.encode([prompt])[0]
        v1_norm = np.linalg.norm(v1)

        def similarity(v2):
            return np.dot(v1,v2)/(v1_norm*np.linalg.norm(v2))

        result =np.apply_along_axis(similarity,axis=1,arr=self.get_vectors())
        return result

    def similarity_rank(self, prompt):
        new_df = self.df.copy()
        new_df['similarity'] = self.get_similarity(prompt)
        return new_df.sort_values(by=['similarity'], ascending=False)

    @staticmethod
    def get_files():
        return [(file.id,file.name) for file in File.select()]

    @staticmethod
    def delete_file(file_id):
        file_query = File.select().where(File.id ==file_id)
        if file_query.exists():
            file_name = file_query.get().name
            Vector.delete().where(Vector.id in FileRow.select(FileRow.vector_id).where(FileRow.file_id == file_id)).execute()
            FileRow.delete().where(FileRow.file_id == file_id).execute()
            File.delete().where(File.id == file_id).execute()
            os.remove(files_path + file_name)

