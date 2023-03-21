#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/4/3 20:34
# @Author : cc
# @File : Least square method.py
# @Software: PyCharm

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy import array

""" 使用最小二乘法，拟合出一元线性回归模型：z = wx + b。
一元的意思是样本x通过一个属性描述，原本可能是矢量x_i = (x_i1, x_i2...,x_id)被例如颜色，大小...
属性描述，现在只有一个x_i1描述，则直接把矢量x_i看成标量，w也是标量

计算出使得损失最小的w和b，
画出拟合直线和原始的散点图
点距离拟合直线越远，代表误差越大
"""
st.header('数据模拟')

# 画出样例的真实分布，输入样本x和真实标记y
def plot_origin(points: array) -> None:
    """
    :param points: array类型的二维数组
    :return:
    """
    arr_x = points[:, 0]  # return list: 所有元素（子数组）中的第一个元素：x
    arr_y = points[:, 1]  # return list: 所有元素（子数组）中的第二个元素：y

    # 画出散点图：照理说学的时间越长，考试分数越高
    pc=plt.scatter(arr_x, arr_y)
       plt.show()
    st.write(pc)

# 2. 策略：求均方误差（损失函数）
def compute_cost(w: float, b: float, points: array) -> float:
    """ 计算均方误差（损失函数）：预测输出和真实标记之间的差距: y - (wx + b)
                z = wx + b 为我们要拟合的线性模型
    :param w: 线性模型参数
    :param b: 线性模型参数
    :param points: array类型的二维数组：所有样例
    :return:  输出E(w，b) 均方误差值
    """
    total_cost = 0
    m = len(points)  # 样本个数m

    # 计算均方误差
    for i in range(m):
        x_i = points[i, 0]  # 第i个样例的第一个元素：x
        y_i = points[i, 1]  # 第i个样例的第二个元素：y
        total_cost += (y_i - w * x_i - b) ** 2
    return total_cost / m  # 均方误差


"""3. 算法：拟合：学得z = wx+b 近似于真实标记y
使用基于均方误差最小化的 最小二乘参数估计
求能使得均方误差最小的w和b：损失函数分别对w，b求偏导=0
以下代码都基于公式推导出来的w，b的表示方法
"""


# 求列表内元素平均值
def avg(lst):
    l = len(lst)
    return sum(lst[i] for i in range(l)) / l


def fit(points: array) -> tuple:
    x_avg = avg(points[:, 0])  # 样本均值
    m = len(points)
    # 求w
    numerator, denominator = 0, -m * x_avg ** 2  # w公式的分子，分母
    for i in range(m):
        x_i, y_i = points[i, 0], points[i, 1]
        numerator += y_i * (x_i - x_avg)
        denominator += x_i ** 2
    w = numerator / denominator

    # 求b
    sum_y = 0
    for i in range(m):
        x_i, y_i = points[i, 0], points[i, 1]
        sum_y += y_i
    b = (sum_y - w * x_avg * m) / m
    return w, b


# 画出拟合函数：一元线性回归模型
def plot_fit(arr_x: array, arr_y: array) -> None:
    plt.scatter(arr_x, arr_y)  # 画散 点 图
    # array类型可以直接对每个元素乘上一个常数，不用for循环慢慢一个个乘
    predict_y = w * arr_x + b  # 拟合的线性模型：预测标记y
    plt.plot(x, predict_y, c='r')  # 画 经过x，y的曲线/直线
    plt.show()


if __name__ == '__main__':
    points = np.genfromtxt('data.csv', delimiter=',')  # array
    x = points[:, 0]  # return array: 所有元素（子数组）中的第一个元素：x
    y = points[:, 1]  # return array: 所有元素（子数组）中的第二个元素：y

    w, b = fit(points)
    print('w, b分别为', w, b)

    print('损失为：', compute_cost(w, b, points))

    cc=plot_fit(x, y)
st.write(cc)
