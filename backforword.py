# -*- coding:utf-8 -*-
# Filename: backforword.py
# Author：rubeeny
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
# 打印路径概率表
def print_dptable(V):
    #V是一个数组，数组的元素为字典，数组长度为观察序列的长度
    #字典存放的是每个时刻，到达每一个状态的概率和
    print("     ",end='')
    for i in range(len(V)):
        print("%7d" % i,end='')
    print('\n')
    for y in V[0].keys():
        print("%.5s: " % y,end='')
        for t in range(len(V)):
            print("%.7s " % ("%f" % V[t][y]),end='')
        print('\n')

#发射概率
emission_probability = {
    'Rainy': {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
    'Sunny': {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
}
def backword():
    bresult=[dict() for i in range(len(observations))]
    for y in states:
        bresult[len(observations)-1][y]=1.0

    for t in range(len(observations)-2,-1,-1):
        for i in states:#t时刻的状态i
            bresult[t][i]=0.0
            for j in states:#t+1时刻的每一个状态j
                # 注意 emission_probability[j][observations[t+1]] observations[t+1]是 t+1
                bresult[t][i]+=transition_probability[i][j]*emission_probability[j][observations[t+1]]*bresult[t+1][j]

    print_dptable(bresult)
    pp=0.0
    for y in states:
        pp=pp+bresult[0][y]*start_probability[y]*emission_probability[y][observations[0]]
    # pp=bresult[0][states[0]]*start_probability[states[0]]*emission_probability[states[0]][observations[0]]\
    #    +bresult[0][states[1]]*start_probability[states[1]]*emission_probability[states[1]][observations[0]]
    print("观察序列[",end='')
    for o in observations:
        print(o+',',end='')
    print("]概率：%f"%pp)
def forword():
    fresult = [dict() for i in range(len(observations))]
    for y in states:
        fresult[0][y]=start_probability[y]*emission_probability[y][observations[0]]

    for t in range(1,len(observations)):
        for i in states:#t时刻的状态i
            fresult[t][i]=0
            for j in states:#t-1时刻的每一个状态j
                fresult[t][i]+=fresult[t-1][j]*transition_probability[j][i]*emission_probability[i][observations[t]]

    print_dptable(fresult)
    pp=0.0
    for y in states:
        pp =pp+fresult[len(observations)-1][y]

    print("观察序列[",end='')
    for o in observations:
        print(o+',',end='')
    print("]概率：%f"%pp)

if __name__ == '__main__':
     backword()
     #观察序列概率：0.033612
     forword()
    #观察序列概率：0.033612



