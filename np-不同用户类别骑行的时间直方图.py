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
# 指定路径保存
output_path='./data/bike/lianxi/'
# 如果不存在,要新建一个文件夹
if not os.path.exists(output_path):
    os.makedirs(output_path)
# 直方图参数
hist_range=(0,180)
n_bins=12

# 只关心两列，骑行时间和用户类别

def collect_data():
    data_arr_list = []
    for file_name in file_names:
        data_file_name=os.path.join(data_path,file_name)
        data_file=np.loadtxt(data_file_name,delimiter=',',dtype='str',skiprows=1)
        data_arr_list.append(data_file)
    return data_arr_list

def pocess_data(data_arr_list):
    year_new_data_list=[]
    for data_arr in data_arr_list:
        data_str=np.core.defchararray.replace(data_arr,'"','')
        # 用户类型
        member_type_col=data_str[:,-1]
        member_type_col=member_type_col.reshape(-1,1)
        # 骑行时间
        data_min=data_str[:,0]
        data_min=data_min.reshape(-1,1)
        # 骑行时间和用户类型横向合并
        new_data = np.concatenate([member_type_col,data_min],axis=1)
        # 将四个季度循环
        year_new_data_list.append(new_data)

    year_new_data=np.concatenate(year_new_data_list,axis=0)
    #过滤
    member_arr=year_new_data[year_new_data[:,0]=='Member']
    casual_arr= year_new_data[year_new_data[:,0] == 'Casual']
    # 转变单位
    year_member_arr=member_arr[:,1].astype('float')/1000/60
    year_casual_arr=casual_arr[:,1].astype('float') / 1000 / 60
    return  year_member_arr,year_casual_arr

def analyze_data(year_member_arr,year_casual_arr):
    #range 规定超过180分钟的数据被过滤掉
    #会返回两个值，1 每个bin 中的样本个数，2 bin 的分界值
    member_hist,member_hist_edges=np.histogram(year_member_arr,range=(0,180),bins=12)
    casual_hist,casual_hist_edges= np.histogram(year_casual_arr, range=(0, 180), bins=12)
    #返回边界等
    print('会员直方图统计信息：{},{}'.format(member_hist,member_hist_edges))
    print('会员直方图统计信息：{},{}'.format(casual_hist,casual_hist_edges))
def show_result(year_member_arr,year_casual_arr):
    # 指定画布大小
    fig=plt.figure(figsize=(10,5))
    # 创建子画布,划分为一行两列
    ax1=fig.add_subplot(1,2,1)
    #统一y 轴范围
    ax2 = fig.add_subplot(1, 2, 2,sharey=ax1)
    # 会员直方图
    ax1.hist(year_member_arr,range=hist_range,bins=n_bins)
    ax2.hist(year_casual_arr, range=hist_range, bins=n_bins)
    # 设置刻度
    # x轴的刻度，每隔15进行划分
    ax1.set_xticks(range(0,181,15))
    ax1.set_title('member')
    ax1.set_ylabel('count')

    #  非会员统计
    ax2.set_xticks(range(0, 181,15))
    ax2.set_title('casual')
    ax2.set_ylabel('count')

    plt.tight_layout()
    plt.savefig(os.path.join(output_path,'zhifangtu.jpg'))
    plt.show()

def main():
    data_arr_list=collect_data()
    year_member_arr,year_casual_arr=pocess_data(data_arr_list)
    analyze_data(year_member_arr,year_casual_arr)
    show_result(year_member_arr,year_casual_arr)

if __name__ == '__main__':
    main()

