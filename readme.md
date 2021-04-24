# just_meme
Repo for meme sharing application built using Django
## Production URL
```
https://just-meme.herokuapp.com/
```
## setup project locally

- Install Python 3.7, Postgres,  virtualenv in your system
- Create postgres server and database
- Clone the just_meme repo
- Create virtual environment using ```virtualenv -p python3.7 venv```
- Activate venv ```source ./venv/bin/activate```
- Install required packages ```pip install -r requirements.txt```
- Add .env file inside config directory and add environment related keys which are specified in settings.py like ```DB_NAME=just_meme``` etc
- Start server and you are good to go :)

