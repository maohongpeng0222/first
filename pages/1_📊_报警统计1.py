import streamlit as st
import sqlite3
import mysql.connector
import pandas as pd
from datetime import datetime,timedelta
import numpy as np
from pyecharts.charts import Pie, Bar, Line, Scatter
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from pyecharts.options import TitleOpts, LegendOpts, ToolboxOpts, VisualMapOpts

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
    users_df = pd.DataFrame(users, columns=['时间', '车速', '经度', '纬度', '里程', '列车号',
                                            '车厢', '波磨1', '波磨2', '多边形1', '多边形2',
                                            '多边形3', '多边形4', '多边形5', '多边形6', '多边形7'
                                            , '多边形8'])
    cursor.close()
    sql_connection.close()
    return users_df

users_df = load_data() #加载数据

end_date = datetime.now()
start_date = end_date - timedelta(weeks=8)

start_date = start_date.date()
end_date = end_date.date()

start_date = pd.to_datetime(start_date)
start_date = st.sidebar.date_input("开始日期:", start_date, format='YYYY/MM/DD')
end_date = st.sidebar.date_input("结束日期:", end_date, format='YYYY/MM/DD')

start_date1 = start_date.strftime('%Y-%m-%d')
end_date1 = end_date.strftime('%Y-%m-%d')

users_df['时间'] = pd.to_datetime(users_df['时间'])
filter_data = users_df[users_df['时间'] >= start_date1]
station_info = filter_data[filter_data['时间'] <= end_date1]

# 筛列车数据
train_num = st.sidebar.multiselect(
    "统计分析：", ['波磨', '多边形'],
    default=['多边形']
)

if train_num == ['波磨']:

    # start_date1 = start_date.strftime('%Y-%m-%d')
    # end_date1 = end_date.strftime('%Y-%m-%d')
    #
    # users_df['时间'] = pd.to_datetime(users_df['时间'])
    # filter_data = users_df[users_df['时间'] >= start_date1]
    # station_info = filter_data[filter_data['时间'] <= end_date1]

    condition = (station_info['波磨1'] > '0') | (station_info['波磨2'] > '0')
    station_info = station_info[condition]

elif train_num == ['多边形']:

    # start_date1 = start_date.strftime('%Y-%m-%d')
    # end_date1 = end_date.strftime('%Y-%m-%d')
    #
    # users_df['时间'] = pd.to_datetime(users_df['时间'])
    # filter_data = users_df[users_df['时间'] >= start_date1]
    # station_info = filter_data[filter_data['时间'] <= end_date1]

    condition = (station_info['多边形1'] > '0') | (station_info['多边形2'] > '0') | (station_info['多边形3'] > '0') | (station_info['多边形4'] > '0') | (station_info['多边形5'] > '0') | (station_info['多边形6'] > '0') | (station_info['多边形7'] > '0') | (station_info['多边形8'] > '0')
    station_info = station_info[condition]

elif (train_num == ['波磨', '多边形']) | (train_num == ['多边形', '波磨']):

    # start_date1 = start_date.strftime('%Y-%m-%d')
    # end_date1 = end_date.strftime('%Y-%m-%d')
    #
    # users_df['时间'] = pd.to_datetime(users_df['时间'])
    # filter_data = users_df[users_df['时间'] >= start_date1]
    # station_info = filter_data[filter_data['时间'] <= end_date1]

    condition = (station_info['波磨1'] > '0') | (station_info['波磨2'] > '0') | (station_info['多边形1'] > '0') | (station_info['多边形2'] > '0') | (station_info['多边形3'] > '0') | (station_info['多边形4'] > '0') | (station_info['多边形5'] > '0') | (station_info['多边形6'] > '0') | (station_info['多边形7'] > '0') | (station_info['多边形8'] > '0')
    station_info = station_info[condition]

else:

    station_info['列车号'] = ''

cate = station_info['列车号'].unique().tolist()
data = station_info['列车号'].value_counts().tolist()

pie = (
    Pie()
       .add('am', [list(z) for z in zip(cate[0:9], data[0:9])],
            radius=["30%", "75%"],
            rosetype="radius"
            )
       .set_global_opts(title_opts=opts.TitleOpts(title="预警统计（饼状图）"))
       .set_global_opts(legend_opts=LegendOpts(padding=0,is_show=True,item_height=10,
                        item_gap=15))
       .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
       )

b = (
    Bar()
        .add_xaxis(station_info['列车号'].unique().tolist()[0:14])
        .add_yaxis(
        series_name=None, y_axis=station_info['列车号'].value_counts().tolist()[0:14])
        .set_global_opts(
        title_opts=opts.TitleOpts(
            title="预警统计（柱状图）"
        ),  # 工具栏，可以切换图表样式--折线图，柱状图....等切换
        toolbox_opts=opts.ToolboxOpts(),
    )
)

st_pyecharts(pie)
st_pyecharts(b)


