import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from preprocess import process
from Statistics import Stats
from user_data import user,user_data


st.title("Chat Analysis")
st.sidebar.title('Whats App chat Analyzer')
# st.sidebar.file_uploader()

uploaded_file=st.sidebar.file_uploader('Choose file',type=['txt'])
user_detail=None

if (uploaded_file):
    data = process(uploaded_file)
    st.dataframe(data)
    members = user(data)
    selected_user = st.sidebar.selectbox("Show analysis wrt",members)
    if  st.sidebar.button("Show Analysis"):
      st.title(selected_user+" Chat Analyze")
      fetch_user_data = user_data(selected_user,data)
      st.dataframe( fetch_user_data)
      
   #  Class instance
      user_detail  = Stats(selected_user,fetch_user_data)
      
      col1,col2,col3 = st.columns(3) 
      with col1:
         st.header('Total Messages')
         st.title(fetch_user_data.shape[0])
      with col2:
         st.header('Media shared')
         media_num  = user_detail.fetch_media()
         st.title(media_num)   

      with col3:
         st.header('Links shared')
         
         links_num =  user_detail.fetch_links()
         st.title(links_num)


    if (selected_user == 'Overall') :
      # print(type(user_detail))
      if (user_detail):
         col1,col2 = st.columns(2)
         with col1:
            st.title("Chart")
            percentage,df2= user_detail.overall_desc()
            bar_data = df2.sort_values(by='chats',ascending=False)
            st.bar_chart(bar_data,x='users',y='chats',horizontal=True,width=700,height=500)
            # flights_wide = busy_users.pivot(index="users", columns="chats", values="chats")
            # sns.barplot(flights_wide)
          
         with col2:
            st.title("Data")
            st.dataframe(percentage,height=500,width=400)     
    try:  

           # most common words
      most_word= user_detail.most_common_word()
      st.header('Most common words')
      st.dataframe(most_word,width=500,)

         # EMOJI EXTRACTOR
      col1,col2 = st.columns(2)   
      emoji_list = user_detail.emoji_extractor()
      with col1:
          st.header('Emojis ')
          st.dataframe(emoji_list)
      with col2:
           st.header('Most shared emojis ')
           palette_color = sns.color_palette('bright')
           y = np.array(emoji_list['Total'].head())
           fig,ax = plt.subplots()
           ax.pie(y,labels=emoji_list['emoji'].head(),autopct=f"%0.2f",startangle=45,colors=palette_color)
           plt.legend(title='Emojis')
           st.pyplot(fig)
         
         # Weekly and Monthly Activity Analysis
      col1,col2 = st.columns(2)   
      with col1:
          daily_chats = user_detail.weekly_activity()
          st.header('Daily chats data')
          fig,ax = plt.subplots()
          ax.barh(daily_chats['day_name'],np.array(daily_chats['count']),color='yellow')
          st.pyplot(fig)
      with col2:
          monthly_chats = user_detail.monthly_activity()
          st.header('Monthly chats data')
          fig,ax = plt.subplots()
          ax.barh(monthly_chats['month'],np.array(monthly_chats['count']),color='lightblue')
          st.pyplot(fig)

          # Monthly Timeline

      timeline = user_detail.timeline_analysis()
      st.header('Monthly Time analysis')
      fig,ax = plt.subplots()
      ax.plot(timeline['Date'], timeline['message'],color='#ACE1AF',marker='x',mec='red',mfc='#F6FB7A')
      plt.xticks(rotation='vertical')
      st.pyplot(fig)

          # Daily Timeline
      d_timeline = user_detail.daily_timeline_analysis()
      st.header('Daily Time analysis')
      fig,ax = plt.subplots()
      ax.plot(d_timeline['only_date'], d_timeline['message'],color='#D95F59')
      plt.xticks(rotation='vertical')
      st.pyplot(fig)

     # Word Cloud 
      word_cloud,title = user_detail.wordCloud_generator()
      st.subheader(f"Word cloud")
      fig,ax = plt.subplots()
      ax.imshow(word_cloud)
      st.pyplot(fig)

       
      # heatmap 
      st.header('Activity map')
      table = user_detail.activity_map() 
      fig,ax = plt.subplots()
      ax = sns.heatmap(table)
      st.pyplot(fig)

     
    except :
       print('error')
