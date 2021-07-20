from .models import Diamond
from django.db import transaction
from .logger import add_log

import pandas as pd
import seaborn as sns
import json
import requests


'''
data_loadedr - data layer get the data from dedicated service or from seaborn model
            and save it in sqlite 
'''

# get pandas dataframe, extract the data and upload it into DB (sqlite)
def load_df_to_db(diamonds_df):
    transaction.set_autocommit(False)
    for record in diamonds_df.to_dict('records'):
        one_diamond = Diamond(**record)
        one_diamond.save() 
    transaction.set_autocommit(True)
    transaction.commit()

# gets new data from a dedicated service and upload it to DB
# returns with information about the total recordes count 
def load_new_data():
    r = requests.post("http://sdkdata.eastus.azurecontainer.io/model/getdiamonds")
    diamonds_df = pd.DataFrame(json.loads(r.text))
    cut_null_df = diamonds_df[diamonds_df['cut'].isna()]
    diamonds_df.drop(cut_null_df.index,inplace=True)
    diamonds_df.drop(['index'],axis=1,inplace=True)
    records_added_count = diamonds_df.shape[0]
    load_df_to_db(diamonds_df)
    records_count = Diamond.objects.all().count()
    pages_count = int(records_count/100) + (records_count %100 > 0)
    message = f"{records_added_count} recordes were loaded to DB from service"
    add_log("Info",message)
    return records_count,pages_count

# initialization - load all records from seaborn model and save it in DB
def init_dataset():
    diamonds = Diamond.objects.all()
    if len(diamonds) == 0:
        print("loading diamonds dataset...")
        diamonds_df = sns.load_dataset('diamonds')
        load_df_to_db(diamonds_df)
        records_count = Diamond.objects.all().count()
        message = f"{records_count} recordes were loaded to DB from seaborn"
        add_log("Info",message)