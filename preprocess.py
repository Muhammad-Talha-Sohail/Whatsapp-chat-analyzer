import pandas as pd
import re
from datetime import datetime


def process(file):
    bytes_data = file.getvalue()
    data = bytes_data.decode("utf-8")
    #with open(file,'r',encoding= 'utf-8') as f:
    #   data= f.read()
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APM]{2}\s-\s' 
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
     # Working For user and messages    
    df = pd.DataFrame({'message_date': dates,'user_message': messages})
    date = list(map(lambda x: x.split(',')[0],df.message_date))
    time_ = list(map(lambda x: x.split(',')[1].replace('-',''),df.message_date))
    df['date']= date   
    df['time_12hrs']= time_   
     # Making 24 hours format from 12 hours format
    def change(x):
        x = x.strip().replace('\u202f', ' ').replace('\u200f', '')
        time_obj = datetime.strptime(x, "%I:%M %p")
        time_str_24hr = time_obj.strftime("%H:%M")
        return time_str_24hr
    
    df['time']=df['time_12hrs'].apply(change)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df['message']= (df.message.apply(lambda x: x.lower())) 
    df.drop('user_message',axis='columns',inplace=True) 

       # Working For date and time 
    df['date'].convert_dtypes(convert_string=False)
    df['time'].convert_dtypes(convert_string=False) 


    df['date']=pd.to_datetime(df['message_date'],format='%m/%d/%y, %I:%M %p - ')
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute   
    df['date'] = df['date'].dt.date
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    df.drop('message_date',axis='columns',inplace=True)
    return df