import pandas as pd
import seaborn as sb
from .models import Diamond
from .logger import add_log
import sklearn.ensemble as se
from sklearn.model_selection import train_test_split
import pickle
from django.core.cache import cache
from django.conf import settings
import os

def fit():
    df = pd.DataFrame(list(Diamond.objects.all().values()))
    df.drop(df.query("x==0 or y==0 or z==0 or y>20 or z>15").index,inplace=True)
    df = pd.get_dummies(df)
    print(df.head(1))
    X = df.drop(['price','id'],axis=1)
    print(X.head(1))
    print("the columns are:")
    print(X.columns)
    
    y = df.price
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.33,random_state=42)
    model = se.RandomForestRegressor()
    model.fit(X_train,y_train)
    score = model.score(X_test,y_test)
    pkl_file_path = os.path.join(os.getcwd(),settings.PKL_FILE_NAME)
    cache.set('current_model', model)
    with open(pkl_file_path, 'wb') as pkl_file:
        pickle.dump(model, pkl_file) 
    message = f"fit was done. score={score}"
    add_log("Info",message)
    print("fit ends")
    return score

def load_model():
    pkl_file_path = os.path.join(os.getcwd(),settings.PKL_FILE_NAME)
    print(f"pkl_file_path is {pkl_file_path}")
    if os.path.isfile(pkl_file_path):
        print("pkl_file_path exists")
        with open(pkl_file_path, 'rb') as pkl_file:  
            model = pickle.load(pkl_file)
            cache.set('current_model', model)
    else:
        print("pkl_file_path does not exist")
        fit()

def predict(features):
    print("predictor predict start")
    columns_for_model = ['carat', 'depth', 'table','x', 'y', 'z', 'cut_Fair',
       'cut_Good', 'cut_Ideal', 'cut_Premium', 'cut_Very Good', 'color_D',
       'color_E', 'color_F', 'color_G', 'color_H', 'color_I', 'color_J',
       'clarity_I1', 'clarity_IF', 'clarity_SI1', 'clarity_SI2', 'clarity_VS1',
       'clarity_VS2', 'clarity_VVS1', 'clarity_VVS2']
    # dfa = pd.DataFrame(list(Diamond.objects.all().values()))
    # dfa.drop(dfa.query("x==0 or y==0 or z==0 or y>20 or z>15").index,inplace=True)
    # dfa = pd.get_dummies(dfa)
    # print("columns start ----- ")
    # print(dfa.columns)
    # print("columns end ----- ")


    # df = pd.DataFrame([[features['carat'],features['depth'],
    #                     features['table'],features['x'],features['y'],
    #                     features['z'],features['cut'],features['color'],features['clarity']]])
    df = pd.DataFrame([features])
    df_plus = pd.get_dummies(df, columns=['cut', 'color','clarity']
               ).reindex(columns=columns_for_model).fillna(0).astype('int')                   
    #df_plus = df_plus.drop(['price','id'],axis=1)
    print("columns start ----- ")
    print(df_plus.columns)
    print("columns end ----- ")
    model =  cache.get('current_model', None)
    the_prediction   = model.predict(df_plus)
    print(f"prediction is {the_prediction}")
    print("predictor predict end")
    message = f"predict was done. {features}"
    add_log("Info",message)
    return the_prediction