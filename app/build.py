
if __name__ == '__main__':
    from db.build import build
    from model.downloader import download

    build()
    download()
