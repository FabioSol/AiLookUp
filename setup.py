from distutils.core import setup
from py2exe import freeze
import os

# Function to gather files in a directory
def gather_files(src_dir):
    files = []
    for dirpath, _, filenames in os.walk(src_dir):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files

# Include the directories you want to package
data_files = []

# Include the static files
data_files.append(('static', gather_files('app/static')))

# Include the db/data folder
data_files.append(('db/data', gather_files('app/db/data')))
data_files.append(('db/data/files', gather_files('app/db/data/files')))

# Include the model files
data_files.append(('model/model', gather_files('app/model/model')))

# Setup configuration
freeze(
    windows=[{
        'script': 'app/main.py'
    }],
    data_files=data_files,
    options={'packages':['PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets']}
)
