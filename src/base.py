import pandas as pd
import requests
import urllib.request, json
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth

class Base:
    
    def __init__(self):
        self.api_url = "https://developer.nps.gov/api/v1/parks?limit=500"
        self.get_data()
    
    def return_url(self):
        return self.api_url
    
    def get_data(self):
        endpoint = "https://developer.nps.gov/api/v1/parks?limit=500"
        HEADERS = {"X-Api-Key":"tASLjg1NQgfuVlLUOD6CdFa93VhSUfc52WuUthf9"}
        req = urllib.request.Request(endpoint,headers=HEADERS)
        response = urllib.request.urlopen(req)
        data = response.read()

        json_data = json.loads(data.decode('utf-8'))
        parks = json_data['data']
        self.df = pd.DataFrame.from_dict(parks)
        
        
if __name__ == '__main__':
    c = Base()
    c.df.to_csv('national_park_information.csv', index=False)


    def clean_data(self):
        columns = ['fees','id','latLong','entrancePasses','directionsInfo','directionsUrl','addresses','weatherInfo','name','contacts']
        self.df.drop(columns=columns,axis=1,inplace=True)
        self.df=self.df.apply(pd.to_numeric,errors='ignore')
        column_fix(self.df,'activities')
        column_fix(self.df,'topics')
        name_change = [{'fullName':'full_name'},{'parkCode':'park_code'},{'entranceFees':'entrance_fees'},{'operatingHours':'operating_hours'}]
        for name in name_change:
            self.df.rename(columns=name,inplace=True)
        cost=[]
        entrance=[]
        for i in self.df['entrance_fees']:
            if len(i)==0:
                cost.append(0)
                entrance.append('Entrance - Free')
            else:
                if len(i)>0:
                    cost.append([i[c]['cost'] for c in range(len(i))])
                if len(i)>0:
                    entrance.append([i[c]['title'] for c in range(len(i))])
        self.df['cost']=cost
        self.df['entrance']=entrance
        self.df.drop(columns='entrance_fees', axis=1, inplace=True)
        operating=[]
        holidays=[]
        for i in self.df['operating_hours']:
            if len(i)>0:
                operating.append(i[0]['standardHours'])
            if len(i)==0:
                operating.append(np.nan)
        for i in self.df['operating_hours']:
            if len(i)>0 and len(i[0]['exceptions'])>0:
                holidays.append(list(set([i[0]['exceptions'][x]['name'] for x in range(len(i[0]['exceptions']))])))
            else:
                holidays.append(np.nan)
        print(len(operating))
        print(len(holidays))
        self.df['standard_hours']=operating
        self.df['holiday']=holidays
        self.df.drop(columns='operating_hours', axis=1, inplace=True)
    
    @staticmethod
    def column_fix(df,column,name='name'):
        for i in range(len(df[column])):
            a_list = []
            for e in range(len(df[column][i])):
                a_list.append(df[column][i][e][name])
            df[column][i] = a_list