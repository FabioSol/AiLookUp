
if __name__ == '__main__':
    from app.db.build import build
    from app.model.downloader import download

    build()
    download()
