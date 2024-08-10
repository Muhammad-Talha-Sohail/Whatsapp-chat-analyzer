def user(data):
      user_list = data['user'].unique().tolist()
      user_list.remove('group_notification')
      user_list.sort()
      user_list.insert(0,"Overall")
      return user_list


def user_data(selected_user,df):
       if selected_user!="Overall":
         user_data  =  df[df['user']==selected_user]
         return user_data
       else:
            return df