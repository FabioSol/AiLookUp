

def build():
    import peewee
    from db.schema import File,FileRow,Vector
    from db import data_path,files_path
    import os

    os.makedirs(data_path, exist_ok=True)
    os.makedirs(files_path, exist_ok=True)

    db = peewee.SqliteDatabase(data_path+'vectors.db')
    db.connect()
    if not db.table_exists('files'):
        db.create_tables([File, Vector, FileRow])

if __name__ == '__main__':
    build()