# diamonds_prediction

Overview
--------
Web application That enables to predict diamonds price
it is based on Django framework and uses sqlite as DB.
during initialization, the application takes the diamonds dataset from seaborn module and
loads it to sqlite DB

User can:
1. Load new data from dedicated service (http://sdkdata.eastus.azurecontainer.io/model/getdiamonds)
2. fit the model to be alligned with the up to date data
3. predict price of diamond by supplying its feature
4. give feedback for the prediction 
5. see table with all the up to date dataset

Admin user can:
1. see logs for all actions that were done
2. see all the predictions + their feedback from user


installation and execution instructions:
----------------------------------------
to run on local machine:
------------------------
1.  git clone https://github.com/yokop/diamonds_prediction.git
2.  pip install virtualenv
3.  python -m virtualenv venv
4.  venv\Scripts\activate.bat
5.  cd diamonds_prediction
6.  pip install -r requirements.txt
7.  python manage.py runserver
8.  via browser: http://127.0.0.1:8000/

to run with docker:
-------------------
sudo docker build . -t diamonds_app:v1
sudo docker run -p 8000 -t diamonds_app:v1

docker was uploaded to azure:
http://diamonds.eastus.azurecontainer.io:8000/

