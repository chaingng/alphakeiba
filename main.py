# coding: UTF-8

import glob
import os
import re

print os.getcwd()

currentdir = os.getcwd()
files = os.listdir(currentdir+'/data')

list = []

for file_name in files:
    list_int = []
    sum = 0

    for line in open('data/'+file_name, 'r'):
        if len(line[:-1]):
            alpha = line.split('\t')[3]
            sum += int(alpha)
            list_int.append(int(alpha))
    for i in range(len(list_int)):
        for j in range(i+1, len(list_int)):
            val1 = float(list_int[i])/sum * 100
            val2 = float(list_int[j])/sum * 100
            val = {
                'value': val1*val2,
                'result': 1 if (i==0 and j==1) else 0
            }
            list.append(val)


thresholds = []
probs_true = []
probs_total = []
probs = []

for i in [1*x for x in range(300)] :
    thresholds.append(i)
    probs_true.append(0.0)
    probs_total.append(0.0)
    probs.append(0.0)

for line in list:
    for i in range(len(thresholds)):
        if line['value'] >= thresholds[i]:
            if line['result']== 1:
                probs_true[i] = probs_true[i] +1
            probs_total[i] = probs_total[i] + 1

for i in range(len(thresholds)):
    if probs_total[i] != 0.0:
        probs[i] = probs_true[i]/probs_total[i] * 100
        print thresholds[i], '|' ,probs[i]



## test ###

file_name = '20161223-hanshin-12'

alphas = []
sum = 0.0

for line in open('test/'+file_name + '.alpha', 'r'):
    if len(line[:-1]):
        alpha = line.split('\t')[2]
        alpha = re.sub(r'\(.*', "", alpha)
        sum += float(alpha)
        alphas.append(float(alpha))

for i in range(len(alphas)):
    alphas[i] = alphas[i]/sum * 100

# print alphas

ozz = [[0 for i in range(20)] for j in range(20)]

for line in open('test/'+file_name + '.oz', 'r'):
    if len(line[:-1]):
        oz = line.split('\t')[2]
        one_num = line.split('\t')[3]
        two_num = line.split('\t')[5]
        ozz[int(one_num)][int(two_num)] = float(oz)

# print ozz

results = []

sum_probs = 0.0

for i in range(len(alphas)):
    for j in range(i+1, len(alphas)):
        val = alphas[i] * alphas[j]
        sum_probs = sum_probs + probs[int(val)]
        results.append(
            {
                'one' : i+1,
                'two' : j+1,
                'alpha' : val,
                'prob' : probs[int(val)],
                'ozz' : ozz[i+1][j+1],
                'expected_value' : probs[int(val)] * ozz[i+1][j+1] * 0.01
            }
        )

print sum_probs

for item in sorted(results, key=lambda x: x['prob'], reverse=True):
    if item['prob'] >= 1.0:
        print "{one}-{two} | {expected_value:.3f} (prob={prob:.3f} oz={ozz})".format(expected_value=item['expected_value'],ozz=item['ozz'],prob=item['prob'],one=item['one'], two=item['two'])
