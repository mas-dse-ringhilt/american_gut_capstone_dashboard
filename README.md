### Capstone Dashboard
Interactively explore American Gut Project Samples and Embedding Results for Body Site Classifcation

Create a virtualenv:  
`python3 -m venv virtualenv`

 Activate the python3 virtualenv with the following:  
`source virtualenv/bin/activate`

Install the required packages:  
`pip install -r requirements.txt`

You will also need to clone and pip install dash-sunburst, a new experimental visualization dash feature used in the dashboard.

First clone dash-sunburst git repo run the following from the top level 'cap_dash' directory:    
`git clone https://github.com/plotly/dash-sunburst.git`

Now pip install dash-sunburst (make sure you are in your virtualenv):  
`pip install -e ./dash-sunburst/`

Go to 'dash' directory:  
`cd dash`

To launch the web app UI run the following:   
`python dash_app.py`

Then open up your web browser and go to 'http://localhost:8050/'
