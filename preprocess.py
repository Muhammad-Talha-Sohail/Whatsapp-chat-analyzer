import pandas as pd
import re


def process(file):
    bytes_data = file.getvalue()
    data = bytes_data.decode("utf-8")
    #with open(file,'r',encoding= 'utf-8') as f:
    #   data= f.read()
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s' 
    x = re.split(pattern, data)[1:]
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
     # Working For user and messages    
    df = pd.DataFrame({'message_date': dates,'user_message': messages})  
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
    df['date']= pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute   
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