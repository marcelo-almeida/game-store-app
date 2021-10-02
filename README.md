# game-store-app
A project to apply knowledge about python using the connexion framework

# Requirements
* Latest python version [available](https://www.python.org/downloads/)
* [Pip](https://pypi.org/project/pip/)
* [Docker](https://www.docker.com/get-started)

# Setup
* Clone this project using these git commands
    `git init`

    `git clone https://github.com/marcelo-almeida/game-store-app.git`

* Install all dependencies from the `requirements.txt` file, found in this project using the command below:

    `pip install -r requirements.txt`

# Run
* It's necessary run the dynamodb before starting the application, 
this can be done using the `execute.py` file found in this repository
use these commands below:

    `python deploy/execute.py -t ddb`

    `python deploy/ddb_create.py`

* Run the project using this command:

    `python deploy/execute.py -t app`