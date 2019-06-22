# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 23:37:10 2019

@author: 86187
"""
import  pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.patches as patches
#%matplotlib inline
import os

data_path = './data/bike/'
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']


#数据收集+数据处理
def collect_and_process_data():
    data_cols = []
    for data_filename in data_filenames:
        data_file=os.path.join(data_path,data_filename)
        data_arr=np.loadtxt(data_file,delimiter=',',dtype='str',skiprows=1)
        #先去掉所有的双引号
        clean_data =np.core.defchararray.replace(data_arr, '"','')
        data_cols.append(clean_data)
    return data_cols
#先划分为了4个季度

#数据分析----数据过滤---通过用户类型分类

def get_mean_duraion_by_type(data_cols,member_type):
    mean_duration_list=[]
    for data_arr in data_cols:
        # 每一行（所有行）的最后一列，布尔
        bool_arr=data_arr[:,-1]==member_type
        #相对应行位置进行过滤,取相应的行
        #bool_arr 是布尔值，只取了True 的行
        filtered_arr=data_arr[bool_arr]
        #先将过滤值的第一列转换数据类型,再转换为分钟
        mean_duration=np.mean(filtered_arr[:,0].astype('float')/1000/60)
        mean_duration_list.append(mean_duration)
    return mean_duration_list


#数据展示
def save_and_results(member_mean_duration_list,casual_mean_duration_list):
    # 1 信息输出
    for idx in range(len(member_mean_duration_list)):
        # 得到每个季度会员的平均骑行时间和非会员的平均骑行时间
        member_mean_duration=member_mean_duration_list[idx]
        casual_mean_duration=casual_mean_duration_list[idx]
        print('第{}季度，会员骑行时间为{:.2f}分钟，非会员骑行时间{:.2f}分钟'.format(
            idx,member_mean_duration,casual_mean_duration))

    # 2 分析结果保存
    #构造多维数组，最后输出为2行4列
    #mean_duration_arr=np.array([member_mean_duration_list,casual_mean_duration_list])

   # 将两行4列转置为4行2列，用转置函数
    mean_duration_arr=np.array([member_mean_duration_list,casual_mean_duration_list]).transpose()

    #保存在目录中,header 可以写第一行数据
    #comments 默认表头是#
    #fmt 设置保存的csv中的数字形式
    np.savetxt('./data/bike/mean_duration.csv',mean_duration_arr,delimiter=',',
               header='member,casual',fmt='%.4f',comments='')

    # 3 可视化结果保存
    plt.figure()
    #plot 为线图,分别绘制会员和非会员的图形,marer='o'点
    plt.plot(member_mean_duration_list,color='r',linestyle='-',marker='o',label='member')
    plt.plot(casual_mean_duration_list,color='g',linestyle='--',marker='*',label='casual')
    plt.title('member vs casual')
    # 调整横坐标,坐标只在0-3区间,rotation刻度进行旋转
    plt.xticks(range(0,4),['1st','2nd','3rd','4th'],rotation=45)
    plt.xlabel('Quarter')
    plt.ylabel('mean duration(min)')
    plt.legend(loc='best')
    #调整布局，以紧凑的形式进行布局
    plt.tight_layout()
    # 在show之前，就进行保存
    plt.savefig('./data/bike/mean_duration.jpg')

    plt.show()


def main():
    #数据获取和数据处理
    data_cols=collect_and_process_data()
    #数据分析
    #会员数据的分析
    member_mean_duration_list=get_mean_duraion_by_type(data_cols,'Member')
    #非会员数据的分析
    casual_mean_duration_list = get_mean_duraion_by_type(data_cols,'Casual')
    #数据展示
    save_and_results(member_mean_duration_list,casual_mean_duration_list)


if __name__ == '__main__':
    main()
