# Create Zendesk Tickets from Github Notifications
A zendesk ticket will be created for new comment on a github repo where you are only a watcher.

# Software Requirements
python3<br>
git

# Instructions for installation
1. Download the framework as a zip file or type
```git clone https://github.com/mukeshtiwari1987/ghub_watcher```
2. Go inside the directory by typing ```cd ghub_watcher```
3. Create a python virtual environment by typing ```python3 -m venv venv```
4. Activate python virtual environment by typing ```source venv/bin/activate```    
5. To install python libraries used in the program, type ```pip3 install -r requirements.txt``` 

# Set Credentials in Environment Variables
1. Get the API Token for Github and Zendesk
2. Type following to set the environment variables
```
export GITHUB_TOKEN='your_github_token'
export ZENDESK_URL='https://your_zendesk_domain.zendesk.com/api/v2/tickets.json'
export ZENDESK_EMAIL='your_email_address'
export ZENDESK_TOKEN='your_zendesk_token'
```
# Instructions for execution 
1. To execute the program, type ```python3 gtoz.py```
2. Logs are captured in <i>debug.log</i> file.