# Hello, this is science website  

### To start working:
miniconda -> https://docs.conda.io/en/latest/miniconda.html (python 3.7)

**Start miniconda terminal and create virtual enviroment in which packages will live and copulate together:**  
conda create -n scihub

**Activate the enviroment(you can also just start SetUpEnv.CMD):**  
conda activate scihub

**To see what packages you have installed and where do:**  
conda list

**!!! download packagesLatest.rar and copy everything from packagesLatest/scihub to your enviroment location from last command !!!**  
**Link:** https://drive.google.com/file/d/1JLOgLo7qv_KUIX51ps036PioIHQVzIE6/view?usp=sharing  
Probably you should copy it to (\AppData\Local\conda\conda\envs\scihub)

### Get this project:  
**Go to location of your project, can be anywhere, (cd ...) go to it and do this commands**  
git clone https://github.com/Mejval5/SciHub.git

**Set up git, there will be two commands which you do displayed**  

### Set up Flask  

**To set starting file for the server do these two commands:**  
set FLASK_APP=runserver.py
set FLASK_ENV=development

###To initialize sql
**Go to sql/init.sql and add your password to the file at this line:**  
(SELECT crypt('PutYourPasswordHere', salt) FROM salt)

**Then run these commands**  
pg_ctl -D database -l logs/dbLog.log start  
psql -d sciencedata -a -f sql/init.sql

**Now you can start the server by command:**  
start.bat

**Have fun :)**  
