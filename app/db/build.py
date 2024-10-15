

def build():
    import peewee
    from app.db.schema import File,FileRow,Vector
    from app.db import data_path,files_path
    import os

    os.makedirs(data_path, exist_ok=True)
    os.makedirs(files_path, exist_ok=True)

    with open(os.path.join(files_path, '.keep'), 'w') as keep_file:
        keep_file.write('# This file is to keep the directory structure intact.\n')

    db = peewee.SqliteDatabase(data_path+'vectors.db')
    db.connect()
    if not db.table_exists('files'):
        db.create_tables([File, Vector, FileRow])

if __name__ == '__main__':
    build()