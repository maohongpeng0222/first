#  streamlit run Hello.py

import streamlit as st

st.set_page_config(
    page_title="你好",
    page_icon="👋",
)

st.write("# Hello! 欢迎使用! 👋")

st.sidebar.success("在上方选择一个演示。")

st.markdown(
    """
    该平台是一个专为数据科学和机器学习项目而构建的应用。
    **👈 从侧边栏选择一个演示**，看看能做什么吧！

    ### 查看一些更复杂的示例
    - 使用神经网络来 [分析 Udacity 自动驾驶汽车图像数据集](https://github.com/streamlit/demo-self-driving)
    - 探索一个 [纽约市乘车数据集](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

