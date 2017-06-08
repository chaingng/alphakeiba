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
            for k in range(j+1, len(list_int)):
                val = {
                    'value': float(list_int[i])/sum * 300 + float(list_int[j])/sum * 300 + float(list_int[k])/sum * 300,
                    'result': 1 if (i==0 and j==1 and k==2) else 0
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

print 'end'

## test ###

file_name = '20170107-kyoto-11'

alphas = []
sum = 0.0

for line in open('test/'+file_name + '.alpha', 'r'):
    if len(line[:-1]):
        alpha = line.split('\t')[2]
        alpha = re.sub(r'\(.*', "", alpha)
        sum += float(alpha)
        alphas.append(float(alpha))

for i in range(len(alphas)):
    alphas[i] = alphas[i]/sum * 1000

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

# 補正連対率を計算
umaren_probs = []

total_umaren_probs = 0.0
for i in range(len(alphas)):
    total_umaren_probs = total_umaren_probs + probs[int(alphas[i])]

for i in range(len(alphas)):
    umaren_prob = probs[int(alphas[i])]/total_umaren_probs * 200 * 0.01
    umaren_probs.append(umaren_prob)

# 馬連ごとの的中率を計算

for i in range(len(alphas)):
    for j in range(i+1, len(alphas)):
        prob = umaren_probs[i] * umaren_probs[j]/(2.0 - umaren_probs[i])
        results.append(
            {
                'one' : i+1,
                'two' : j+1,
                'prob' : prob,
                'ozz' : ozz[i+1][j+1],
                'expected_value' : prob * ozz[i+1][j+1]
            }
        )

for item in sorted(results, key=lambda x: x['prob'], reverse=True):
    if item['prob'] >= 0.0:
        print "{one}-{two} | {expected_value:.3f} (prob={prob:.3f} oz={ozz})".format(expected_value=item['expected_value'],ozz=item['ozz'],prob=item['prob'],one=item['one'], two=item['two'])
