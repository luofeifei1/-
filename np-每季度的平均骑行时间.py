# -*- coding: utf-8 -*-
import  pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.patches as patches
#%matplotlib inline
import os

data_path='./data/bike/'
file_names=['2017-q1_trip_history_data.csv','2017-q2_trip_history_data.csv',
           '2017-q3_trip_history_data.csv','2017-q4_trip_history_data.csv']

#查看数据类型，统计空值
  #df.info()
   #df.isnull.sum()'''

# 数据收集，集合所有数据
def collect_data():
    data_arr_list=[]
    for file_name in file_names:
        data_file=os.path.join(data_path,file_name)
        data_arr=np.loadtxt(data_file,delimiter=',',dtype='str',skiprows=1)
        data_arr_list.append(data_arr)
    return data_arr_list

# 数据处理
def process_data(data_arr_list):
    duration_min_list=[]
    for data_arr in data_arr_list:
        #拿所有行的第0列
        duration_str_col=data_arr[:,0]
        # 去掉双引号
        duration_str=np.core.defchararray.replace(duration_str_col,'"','')
        # 类型转换，毫秒转分钟*/
        duration_min=duration_str.astype('float')/1000/60

        duration_min_list.append(duration_min)
    return  duration_min_list

    #数据分析
def analyze_data(duration_min_list):
    duration_mean_list=[]
    # enumerate 循环时，伴随索引号
    for idx,duration in enumerate(duration_min_list) :
        duration_mean=np.mean(duration)
        print('第{}季度的，平均骑行时间：{:.2f}分钟'.format(idx+1,duration_mean))
        duration_mean_list.append(duration_mean)
    return duration_mean_list

#数据展示
def show_results(duration_mean_list):
    plt.figure()
    #横向为列表，纵向为数值
    plt.bar(range(len(duration_mean_list)),duration_mean_list)
    plt.show()

def main():

    data_arr_list=collect_data()
    # 数据处理
    duration_min_list=process_data(data_arr_list)
    # 数据分析
    duration_mean_list=analyze_data(duration_min_list)
    #数据展示
    show_results(duration_mean_list)
if __name__ == '__main__':
    main()



