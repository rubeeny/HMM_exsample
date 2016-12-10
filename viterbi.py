# -*- coding:utf-8 -*-
# Filename: viterbi.py
# Author：longzhangchao
# Date: 2016-012-10 8:51AM
#状态序列
states = ('Rainy', 'Sunny')
#观察序列
observations = ('walk', 'shop', 'clean')
#初始概率
start_probability = {'Rainy': 0.6, 'Sunny': 0.4}
#状态转移概率
transition_probability = {
    'Rainy': {'Rainy': 0.7, 'Sunny': 0.3},
    'Sunny': {'Rainy': 0.4, 'Sunny': 0.6},
}
#发射概率
emission_probability = {
    'Rainy': {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
    'Sunny': {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
}

# 打印路径概率表
def print_dptable(V):
    #V是一个数组，数组的元素为字典，数组长度为观察序列的长度
    #字典存放的是每个时刻，到达每一个状态的最大概率
    print("     ",end='')
    for i in range(len(V)):
        print("%7d" % i,end='')
    print('\n')
    for y in V[0].keys():
        print("%.5s: " % y,end='')
        for t in range(len(V)):
            print("%.7s " % ("%f" % V[t][y]),end='')
        print('\n')

#维特比算法
def viterbi(obs, states, start_p, trans_p, emit_p):
    """
    :param obs:观测序列
    :param states:隐状态
    :param start_p:初始概率（隐状态）
    :param trans_p:转移概率（隐状态）
    :param emit_p: 发射概率 （隐状态表现为显状态的概率）
    :return:
    """
    # 路径概率表 V[时间][隐状态] = 概率
    #V[t][y]表示在t时刻，到达状态y的最大概率
    # V是一个数组，数组的元素为字典，数组长度为观察序列的长度
    #字典存放的是每个时刻，到达每一个状态的最大概率
    V = [{}]
    # 一个中间变量，代表当前状态是哪个隐状态
    #存放的是当V[t][y]取最大概率时的前一状态
    #path是一个字典，字典的key表示当前的状态，值表示到达当前状态概率最大的路径
    path = {}

    # 初始化初始状态 (t == 0)
    for y in states:
        #V[0][y]表示t==0时刻，到达状态y的最大概率
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        #当t为0时 到达当前的状态概率最大的路径就是当前的状态本身
        #y表示当前状态，[y]表示到达当前状态概率最大的前一状态
        path[y] = [y]

    # 对 t > 0 跑一遍维特比算法
    for t in range(1, len(obs)):#对于每个时刻t
        V.append({})
        newpath = {}

        for y in states:#对于当前状态y
            # 概率 隐状态 =    前状态是y0的概率 * y0转移到y的概率 * y表现为当前状态的概率
            #寻找到达当前状态的最大概率，并记录前一状态到state中
            (prob, state) = max([(V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states])
            # 记录最大概率
            V[t][y] = prob
            # 记录路径
            #state记录的是前一状态，y记录的是当前状态 P[state]表示到达前一状态概率最大的路径，[y]表示当前路径
            #这行代码的含义是到达当前状态最大概率的路径 等于 到达前一状态概率最大的路径加上当前状态
            #这也是一个递归的过程
            newpath[y] = path[state] + [y]

        # 不需要保留旧路径
        path = newpath

    print_dptable(V)
    #求最后一个时刻，概率最大的状态和对应的概率
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    #最大概率和最可能的路径
    return (prob, path[state])

def example():
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)

print (example())