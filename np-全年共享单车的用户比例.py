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

def collect_data():
    data_arr_list=[]
    for file_name in file_names:
        data_file_name=os.path.join(data_path,file_name)
        data_file=np.loadtxt(data_file_name,delimiter=',',dtype='str',skiprows=1)
        data_arr_list.append(data_file)
    return data_arr_list

# 求的是全年的数据，---numpy的数组合并
def process_data(data_arr_list):
    member_type_list=[]
    for data_arr in data_arr_list:
        # 去掉最后一列的双引号
        member_type_col=np.core.defchararray.replace(data_arr[:,-1],'"','')
        # 一列默认为一个维度，默认为横向的，要调整为纵向的向量
        #-1 是numpy 自动计算有多少行
        member_type_col=member_type_col.reshape(-1,1)
        member_type_list.append(member_type_col)
    #将4个合并到一起
    year_member_type=np.concatenate(member_type_list)
    return year_member_type


# 比较全年共享单车的用户比例
def analyze_data(year_member_type):
    #[year_member_type == 'Member']显示布尔值，起过滤用
    # shape[0]查看行数
    n_member =year_member_type[year_member_type=='Member'].shape[0]
    n_casual = year_member_type[year_member_type == 'Casual'].shape[0]
    n_user=[n_member,n_casual]
    return n_user

def show_result(n_user):
    plt.figure()
    plt.pie(n_user,startangle=90,autopct='%1.2f%%',labels=['Member','Casual'],
            shadow=True,explode=(0.05,0.05))
    plt.title('Member vs Casual')
    plt.tight_layout()
    #设置正圆形
    plt.axis('equal')
    plt.legend()
    #指定路径保存
    plt.savefig(os.path.join(output_path,'bintu.jpg'))
    plt.show()

def main():
    data_arr_list=collect_data()
    year_member_type=process_data(data_arr_list)

    n_user=analyze_data(year_member_type)

    show_result(n_user)

if __name__ == '__main__':
    main()