#  streamlit run app.py

import streamlit as st
import requests
import pandas as pd
# Backend API URL
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import time

# 应用标题
st.title('交互式数据分析应用')

# 文件上传
uploaded_file = st.file_uploader("选择一个xlsx文件", type="xlsx")
if uploaded_file is not None:

    with st.spinner('Wait for it ... ...'):
        time.sleep(2)

    data = pd.read_excel(uploaded_file)

    # 筛选车号
    train_num = st.sidebar.multiselect('选择列车号',data['列车号'].unique())

    start_date = st.sidebar.date_input("开始日期:", format='YYYY/MM/DD', key='start_date')
    end_date = st.sidebar.date_input("结束日期:", format='YYYY/MM/DD', key='end_date')

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if start_date and end_date:

    # time_range = st.sidebar.slider('时间轴',
    #                                min_value=data['时间'].min(),
    #                                max_value=data['时间'].max(),
    #                                value=(data['时间'].min(),data['时间'].max()),
    #                                format="MM-DD-YY hh:mm"
    #                                )
        filter_data = data[(data['列车号'].isin(train_num))]
        filter_data['时间'] = filter_data['时间'].dt.date

        # start_date = pd.to_datetime('2024-08-30')
        start_date1 = start_date.strftime('%Y-%m-%d')
        end_date1 = end_date.strftime('%Y-%m-%d')

        filter_data['时间'] = pd.to_datetime(filter_data['时间'])
        filter_data = filter_data[filter_data['时间'] >= start_date1]
        station_info = filter_data[filter_data['时间'] <= end_date1]

        # filter_data[filter_data['时间'] >= pd.to_datetime('2024-08-30')]
        # filter_data[pd.to_datetime(filter_data['时间']) <= pd.to_datetime('2024-08-30')]

        df_map = station_info[['纬度','经度']]
        df_map.rename(columns={'纬度':'lat','经度':'lon'},inplace=True)
        df_map = pd.DataFrame(df_map,columns=['lat', 'lon'])

        tab1, tab2 = st.tabs(['地图','统计'])
        with tab1:
            st.map(df_map)
        with tab2:
            num_DBX = data['列车号'].value_counts()

            st.bar_chart(num_DBX.head(20))

# st.title("地图展示")
#
# file_path = 'C:/Users/ASUS/Desktop/车站坐标匹配（细）2024-09-14_15-23-39.xlsx'
# data = pd.read_excel(file_path)  # 读取excel数据  , sheet_name=None
#
# df_map = data[['纬度','经度']]
# df_map.rename(columns={'纬度':'lat','经度':'lon'},inplace=True)
#
#
# df_map = pd.DataFrame(df_map,columns=['lat', 'lon'])
# st.map(df_map)

