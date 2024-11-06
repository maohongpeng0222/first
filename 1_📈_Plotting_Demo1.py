import streamlit as st
import sqlite3
import mysql.connector
import pandas as pd
from datetime import datetime,timedelta

def LatLon_Rad2Dec(LatLon):
    Rad_Lat = LatLon['纬度'][0:3]
    Rad_Lon = LatLon['经度'][0:3]
    LatLon[4:10]

    users_df['经度'][121][0:3]
    users_df['经度'][121][4:10]

sql_connection = mysql.connector.connect(
    host='172.168.100.80',
    user='root',
    password='123456'
    # database='bsy-private-data'
)

# 创建cursor对象
cursor = sql_connection.cursor()

# 查询
query = ("SELECT t2.times,t2.speeds,t2.longitude,t2.latitude,t2.mileage,t2.group_no,t2.carriage_no,t2.cggbm_status1,t2.cggbm_status2,t2.zxcldbx_status1,t2.zxcldbx_status2,t2.zxcldbx_status3,t2.zxcldbx_status4,t2.zxcldbx_status5,t2.zxcldbx_status6,t2.zxcldbx_status7,t2.zxcldbx_status8 "
         "FROM `bsy-private-data`.sys_bvds_eth_error t2")
cursor.execute(query)

# 获取查询结果
users = cursor.fetchall()
# users_df = pd.DataFrame(users,columns=['时间', '车速', '经度', '纬度', '里程', '列车号',
#                                        '车厢', '波磨1', '波磨2', '多边形1', '多边形2',
#                                        '多边形3', '多边形4', '多边形5', '多边形6', '多边形7'
#                                        , '多边形8'])
# df_map_users_df = users_df[['纬度', '经度']]
# for index,row in df_map_users_df.iterrows:
#     row

end_date = datetime.now()
start_date = end_date - timedelta(weeks=8)

start_date = start_date.date()
end_date = end_date.date()

start_date = pd.to_datetime(start_date)
start_date = st.sidebar.date_input("开始日期:", start_date, format='YYYY/MM/DD')
end_date = st.sidebar.date_input("结束日期:", end_date, format='YYYY/MM/DD')

# 筛列车数据
# even_numbers = list(filter(lambda x: x == x.unique(), users[0][5]))
ages = [table[5] for table in users]
ages = pd.Series(ages)
ages = ages.unique()

train_num = st.sidebar.multiselect(
    "选择列车号：",ages
)
filter_data = users[(users['列车号'].isin(train_num))]


start_date1 = start_date.strftime('%Y-%m-%d')
end_date1 = end_date.strftime('%Y-%m-%d')

filter_data['时间'] = pd.to_datetime(filter_data['时间'])
filter_data = filter_data[filter_data['时间'] >= start_date1]
station_info = filter_data[filter_data['时间'] <= end_date1]

df_map = station_info[['纬度', '经度']]
df_map_users_df = users_df[['纬度', '经度']]

for row in df_map_users_df['纬度']:
    row


df_map.rename(columns={'纬度': 'lat', '经度': 'lon'}, inplace=True)
df_map = pd.DataFrame(df_map, columns=['lat', 'lon'])

# tab1, tab2 ,tab3= st.tabs(['地图', '统计', '数据展示'])
tab2 ,tab3= st.tabs(['统计', '数据展示'])
# with tab1:
#     st.map(df_map)
with tab2:
    num_DBX = filter_data['列车号'].value_counts()
    st.bar_chart(num_DBX.head(20))
with tab3:
    st.write(filter_data)

# 展示数据

# for user in users_df:
#     time = user[0]
#     speeds = user[1]
#     lon = user[2]
#     lat = user[3]
#     group_no = user[5]
#     carriage_no = user[6]
#     bm_1 = user[7]
#     bm_2 = user[8]
#     dbx_1 = user[9]
#     dbx_2 = user[10]
#     dbx_3 = user[11]
#     dbx_4 = user[12]
#     dbx_5 = user[13]
#     dbx_6 = user[14]
#     dbx_7 = user[15]
#     dbx_8 = user[16]
#
#     st.write(user)



# 关闭cursor连接


cursor.close()
sql_connection.close()
