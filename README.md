# AiLookUp

This project is a standalone, overpowered VLOOKUP powered by Sentence-BERT. It allows users to perform advanced lookup operations based on natural language input, leveraging the power of Sentence-BERT for semantic understanding.


## Prerequisites

Make sure you have the following installed:

- **Python 3.11**: Download from [here](https://www.python.org/downloads/).
- **Git**: Download from [here](https://git-scm.com/downloads).

## Build Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/FabioSol/AiLookUp.git
```

### 2. Create and Activate a Virtual Environment
Go to the cloned repository, create the venv and activate it:
```bash
cd AiLookUp
python -m venv venv #if you have multiple python versions use py -3.11 -m venv venv 
source venv/Scripts/activate
```

### 3. Install the Required Packages
Use pip to install the required packages listed in requirements.txt :
```bash
pip install -r requirements.txt
```

### 4. Build the Application
This will create and download the necessary files for the app tu run
```bash
python -m app.build
```
At this point you should be able to run the app in the repo with this command:

```bash
python -m app
```
feel free to load information so your build has it by default or edit the static file for styling


### Generate the Executable
```bash
pyinstaller --onefile app/__main__.py --add-data "app/model/model;app/model/model" --add-data "app/db/data;app/db/data" --add-data "app/static;app/static" --icon=app/static/logo.ico --name AiLookUp --noconsole
```