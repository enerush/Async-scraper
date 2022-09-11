Scraper DATA from website
===========================


############ HOW TO RUN THE SCRAPER
1. Install GIT for your system (https://github.com/git-guides/install-git)

3. Download the project from Github. Run following command in terminal:
  - $ git clone https://github.com/enerush/task-DataOx.git
  - $ cd ~/task-DataOx

4. Run script:
    - 

4. Check result in DB or in Google Sheets(https://docs.google.com/spreadsheets/d/1OaclRBnBQcUqmUw778KplyEhKV5kLkoDF31V2NteukA/edit?usp=sharing) 


############# Описание структуры каталога
│
├── Model
│     ├── __init__.py 
│     ├── database.py
│     └── dump.sql
├── Sheets
│     ├── google_sheets.py
│     └──service_account.json
│
├── README.md
├── .gitignore   
├── config.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── scraper.py
├── scraper_async.py



