import peewee
from app.db import data_path

class BaseModel(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(data_path+'vectors.db')

class File(BaseModel):
    name = peewee.CharField()
    description_col = peewee.CharField()

class Vector(BaseModel):
    vector = peewee.BlobField()

class FileRow(BaseModel):
    file_id = peewee.ForeignKeyField(File, related_name='rows')
    row_id = peewee.IntegerField()
    vector_id = peewee.ForeignKeyField(Vector, related_name='rows')
    class Meta:
        primary_key = peewee.CompositeKey('file_id', 'row_id')
        database = peewee.SqliteDatabase(data_path+'vectors.db')

