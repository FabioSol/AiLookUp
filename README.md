# My Application

This project contains a Python application that can be built into an executable using PyInstaller. Follow the steps below to clone the project, set up a virtual environment, install the necessary dependencies, and finally build the application.

## Prerequisites

Make sure you have the following installed:

- **Python 3.x**: Download from [here](https://www.python.org/downloads/).
- **Git**: Download from [here](https://git-scm.com/downloads).
- **PyInstaller**: Install via `pip` as shown in the steps below.

## Build Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <repository-url>
```

### 2. Create and Activate a Virtual Environment

```bash
cd <your-project-folder>
python -m venv venv
venv\Scripts\activate
```

### 3. Install the Required Packages

```bash
pip install -r requirements.txt
```

### 4. Build the Application
```bash
python app/build.py
```


### Generate the Executable
```bash
pyinstaller --onefile app/main.py --add-data "app/model/model;app/model/model" --add-data "app/db/data;app/db/data" --icon=app/static/logo.ico --name AiLookUp
```