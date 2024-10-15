

def build():
    import peewee
    from schema import File,FileRow,Vector
    from db import data_path
    db = peewee.SqliteDatabase(data_path+'vectors.db')
    db.connect()
    if not db.table_exists('files'):
        db.create_tables([File, Vector, FileRow])

if __name__ == '__main__':
    build()