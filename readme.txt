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

