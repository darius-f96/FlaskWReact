npm -g update

#install python
python --version if it's not 3.7.x or not installed
#Linux users:
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8

#Windows users:
Open powershell as administrator and run 
To install choco https://chocolatey.org/install
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
Install python:
choco install -y python3

#Backend installation
Navigate to semantic-backend-server

pip3 install virtualenv
Sudo apt-get install virtualenv(for linux users)
python -m venv venv
source venv/bin/activate (linux)

For windows switch to command prompt and run the following
.\venv\Scripts\activate.bat (windows)
pip install Flask
pip3 install request
pip3 install jsonify
pip3 install cryptography
pip install gql[all]
pip3 install rdflib

Json-server installation:
npm install -g json-server
Navigate to semantic-json-server
npm install

Json-graphql-server installation:
npm install -g json-graphql-server
Navigate to semantic-json-graphql-server
npm install

Rdf4j-server installation
Install XAMPP, or just tomcat based on your preference
https://www.apachefriends.org/ro/index.html
Start XAMPP and tomcat, navigate to http://localhost:8080/ -> manager 
Use credentials (from tomcat-users.xml)
Deplay war file rdf4j-server from the semantic-rdf4j-server/war
Same with the other one rdf4j-workbench.war
From tomcat manager navigate to the newly deployed rdf4j-workbench and create a repository called 'grafexamen'

React-frontend installation
Navigate to semantic-frontend-server
npm install
If you are running on windows in package.json you might need to change start script (use set instead of export for port change)

Starting the servers:
Navigate to each folder with command prompt or terminal
json-server --watch db.json --port 4000
json-graphql-server db.js
For backend:
.\venv\Scripts\activate.bat (windows)
source venv/bin/activate (linux)
python api.py
For frontend:
npm start
