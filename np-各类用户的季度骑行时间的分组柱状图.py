# -*- coding: utf-8 -*-
# 不同用户在四个季度的平均骑行时间
import  pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.patches as patches
#%matplotlib inline
import os

# 解决中文显示问题,默认字体转为黑体,仅适用于windows 系统
plt.rcParams['font.sans-serif']=['SimHei']

data_path = './data/bike/'
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']
output_path='./data/bike/lianxi/'
# 如果不存在,要新建一个文件夹
if not os.path.exists(output_path):
    os.makedirs(output_path)

# 数据收集
def collect_data(data_filenames):
    data_list=[]
    for data_filename in data_filenames:
        data_file_path=os.path.join(data_path,data_filename)  #路径拼接
        data_file=np.loadtxt(data_file_path,delimiter=',',dtype='str',skiprows=1)
        data_list.append(data_file)
    return data_list

def pocess_analyze_data(data_list,data_arr_type):
    data_min_avg_list=[]
    for data_arr in data_list:
        data_arr_str=np.core.defchararray.replace(data_arr,'"','')
        # 将布尔值分开
        data_arr_bool=data_arr_str[data_arr_str[:,-1]==data_arr_type]
        # 将第一列，转变为列的形式
        data_ms_str=data_arr_bool[:,0]
        data_ms_str=data_ms_str.reshape(-1,1)
        data_min=data_ms_str.astype('float')/1000/60
        data_min_avg=np.mean(data_min)
        data_min_avg_list.append(data_min_avg)
    return data_min_avg_list

def show_result(data_min_avg_list_member,data_min_avg_list_casual):
    bar_locs=np.arange(4)
    plt.figure(figsize=(10,5))
    plt.bar(bar_locs,data_min_avg_list_member, width=0.35,label='Member', facecolor = 'yellowgreen')
    # 并列柱状图要改变x轴的位置，相同位置会被覆盖
    plt.bar(bar_locs+0.35,data_min_avg_list_casual,width=0.35,label='Casual',facecolor = 'lightskyblue')
    # 想让刻度，显示在中间。把刻度作偏移+柱子宽度的1/2
    plt.xticks(bar_locs+0.175, ['1st', '2nd', '3rd', '4th'], rotation=45)
    plt.ylabel('平均骑行时间(分钟)',fontproperties=get_chinese_font())
    plt.legend(loc='best',pro=get_chinese_font())
    plt.title('Member vs Casual 柱状图')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'zhutu.jpg'))
    plt.show()

def main():
    data_list=collect_data(data_filenames)
    data_min_avg_list_member=pocess_analyze_data(data_list,'Member')
    data_min_avg_list_casual=pocess_analyze_data(data_list,'Casual')
    print(data_min_avg_list_member)
    print(data_min_avg_list_casual)
    show_result(data_min_avg_list_member, data_min_avg_list_casual)

if __name__ == '__main__':
    main()

