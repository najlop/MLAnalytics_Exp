#! /bin/bash
# set -e

# Start SSH server
sudo service ssh start

# # create log directory
# if [ ! -d "/lightcurveruntime/logs" ]; then
#     mkdir /lightcurveruntime/logs
# fi

# start the services
# nohup micromamba run -n arielgpt flask --app competition_host run --port 5001 >> /lightcurveruntime/logs/flask.log 2>&1 
# nohup micromamba run -n arielgpt streamlit run main.py >> /lightcurveruntime/logs/streamlit.log 2>&1 &
micromamba run -n arielgpt streamlit run app.py