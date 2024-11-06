import streamlit as st
import sqlite3
import mysql.connector
import pandas as pd
from datetime import datetime,timedelta
import numpy as np
from pyecharts.charts import Pie, Bar, Line, Scatter, Geo
from pyecharts.charts import Map
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
import time
from pyecharts.faker import Faker
from pyecharts.globals import ChartType, SymbolType, CurrentConfig, ThemeType, GeoType

# 隐藏streamlit默认格式信息
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            <![]()yle>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)


def LatLon_Rad2Dec(LatLon):
    Rad_Lon = [float(table[0:3]) for table in LatLon['经度']]
    Rad_Lon_Min = [float(table[4:10])/60 for table in LatLon['经度']]
    LatLon_Dec = list(np.add(Rad_Lon, Rad_Lon_Min))

    Rad_Lat = [float(table[0:3]) for table in LatLon['纬度']]
    Rad_Lat_Min = [float(table[4:10])/60 for table in LatLon['纬度']]
    LatLat_Dec = list(np.add(Rad_Lat, Rad_Lat_Min))

    Dec = pd.DataFrame(list(zip(LatLon_Dec, LatLat_Dec)),columns=['经度','纬度'])

    return Dec

@st.cache_data
def load_data():
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
    users_df = pd.DataFrame(users,columns=['时间', '车速', '经度', '纬度', '里程', '列车号',
                                           '车厢', '波磨1', '波磨2', '多边形1', '多边形2',
                                           '多边形3', '多边形4', '多边形5', '多边形6', '多边形7'
                                           , '多边形8'])
    cursor.close()
    sql_connection.close()
    return users_df

users_df = load_data() #加载数据

end_date = datetime.now()
start_date = end_date - timedelta(weeks=4)

start_date = start_date.date()
end_date = end_date.date()

start_date = pd.to_datetime(start_date)
start_date = st.sidebar.date_input("开始日期:", start_date, format='YYYY/MM/DD')
end_date = st.sidebar.date_input("结束日期:", end_date, format='YYYY/MM/DD')

# 筛列车数据
train_num = st.sidebar.multiselect(
    "选择列车号：", users_df['列车号'].unique(),
    default=users_df['列车号'].unique().tolist()[:5]
)
filter_data = users_df[(users_df['列车号'].isin(train_num))]

start_date1 = start_date.strftime('%Y-%m-%d')
end_date1 = end_date.strftime('%Y-%m-%d')

filter_data['时间'] = pd.to_datetime(filter_data['时间'])
filter_data = filter_data[filter_data['时间'] >= start_date1]
filter_data = filter_data[filter_data['时间'] <= end_date1]

tab1, tab2, tab3, tab4= st.tabs(['地图', '统计', '数据展示', '123'])
with tab1:
    condition = (filter_data['波磨1'] > '0') | (filter_data['波磨2'] > '0')
    filter_data = filter_data[condition]

    LatLon = filter_data[['纬度', '经度']]
    Dec = LatLon_Rad2Dec(LatLon)

    Dec.rename(columns={'纬度': 'lat', '经度': 'lon'}, inplace=True)
    df_map = pd.DataFrame(Dec, columns=['lat', 'lon'])
    df_map = df_map[df_map['lat'] != 0]

    st.map(df_map)
with tab2:
    num_DBX = filter_data['车厢'].value_counts()
    st.bar_chart(num_DBX)
with tab3:
    st.write(filter_data)


