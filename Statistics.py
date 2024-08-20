from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import emoji




with open('stop_hinglish.txt','r') as f:
      stopwords = f.read()
      f.close()    



class Stats:
    def __init__(self,selected_user,df):
           self.extractor = URLExtract()
           self.user = selected_user
           self.df  = df
      
    def fetch_links(self):
            urls = self.extractor.find_urls(self.df.message.to_string())
            return len(urls)
    
    def fetch_media(self):
          media  = self.df[self.df.message =='<media omitted>\n'].shape[0]
          return media
    
    def overall_desc(self):
        df2 = self.df[self.df['user'] != 'group_notification']
        busy = df2.groupby(['user']).agg({"message":'count'})  # [('Talha',50),("harry",676)]  
        X = [i for i in busy['message'].keys()]
        Y = [i for  i in busy['message'].values]
        df2 = pd.DataFrame({
              'users':X,
              'chats':Y
        })
        
        percentage = round((busy/df2.shape[0]),3).reset_index().rename( columns={'user':'Participant',"message":'Contribution'})
        percentage['Contribution'] = percentage.Contribution.apply(lambda x: str(x)+' %')
        
        return percentage,df2
    

    def wordCloud_generator(self):                         
           df2 = self.df[(self.df['user'] != 'group_notification') ]
           df2 =df2[df2['message']!='<media omitted>\n'] 
           lst = []
           for i in df2.message:
                lst.extend(i.split())             
           words = [i for i in lst if i not in stopwords]    
           wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                 min_font_size = 10).generate(str(words))
           return wordcloud,self.user
    
    
    def most_common_word(self):
          df2 = self.df[(self.df['user'] != 'group_notification') ]
          df2 =df2[df2['message']!='<media omitted>\n'] 
          lst ,temp= [] ,{}
          for i in df2.message:
            lst.extend(i.split())
          words = [i for i in lst if i not in stopwords]    
          for i in words:
            if i not in temp.keys():
                  tot = words.count(i)
                  temp[i]=tot
          most=pd.DataFrame(
          {
          'words':temp.keys(),
          'no_of_occurance':temp.values()
          }
          )
          most_word=most.sort_values(by='no_of_occurance',ascending =False)[:30].reset_index(drop=True)
          return most_word
     
     
    def  timeline_analysis(self):
  
         timeline = self.df.groupby(['year','month']).agg({"message":"count"}).reset_index()
         temp=[]
         for i in range(timeline.shape[0]):
           temp.append(f"{timeline['year'][i]}-{timeline['month'][i]}")

         timeline['Date']=temp
         return timeline    
     
    def daily_timeline_analysis(self):
           daily_timeline = self.df.groupby(['only_date']).agg({"message":'count'}).reset_index()    
           return daily_timeline
    def emoji_extractor(self):
          df2 = self.df[(self.df['user'] != 'group_notification') ]
          df2 =df2[df2['message']!='<media omitted>\n'] 
          lst = []
          for i in df2.message:
             lst.extend(i.split())
          emoji_list = []
          for message in lst:
            if(emoji.is_emoji(message)):
                  emoji_list.append(message)
        
          emojis_data =pd.DataFrame({
             "emoji":emoji_list
               }).value_counts().reset_index().rename(columns={"count":"Total"})
          return emojis_data
    def weekly_activity(self):
           day = self.df.day_name.value_counts().reset_index()
           return day
    def monthly_activity(self):
          month = self.df.month.value_counts().reset_index()
          return  month
    def activity_map(self):
        table = pd.pivot_table(self.df,index='day_name',columns='period',values='message', aggfunc='count').fillna(0)     
        return table   


