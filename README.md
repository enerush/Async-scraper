Project: task-DataOx
===========================
Scraper DATA from the website https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273

Stack: requests, aiohttp, lxml, beautifulsoup4, SQLAlchemy, google-api, gspread, docker, git

Parsing DATA: Image URL, Title, Location, Date publish, Price, Description, Beds count
Saving DATA to: Postgres DB, Google Sheets


############ HOW TO RUN THE SCRAPER
1. Install GIT for your system (https://github.com/git-guides/install-git)

2. Download the project from Github:
  - $ git clone https://github.com/enerush/task-DataOx.git

4. Steps to run script without DOCKER:
   - $ cd ~/task-DataOx
   - $ python3.10 -m venv venv
   - $ source venv/bin/activate
   - $ pip install -r requirements.txt
   - open config.py and add your DB access.
     Exemple:
           - USER_NAME = <user name>
           - USER_PASSWORD = 'postgres'
           - DB_HOST = 'localhost'
           - DB_PORT = '5432'
           - DB_NAME = 'postgres'
  
   - $ python3 scraper_async.py  (for asynchronous requests)
   - or $ python3 scraper.py  (for synchronous requests)

5. Steps to run script with DOCKER:
    - Install docker (https://docs.docker.com/engine/install/)
    - $ cd ~/task-DataOx
    - $ docker-compose up

6. Check result in DB or in Google Sheets:
   - https://docs.google.com/spreadsheets/d/1OaclRBnBQcUqmUw778KplyEhKV5kLkoDF31V2NteukA/edit?usp=sharing

