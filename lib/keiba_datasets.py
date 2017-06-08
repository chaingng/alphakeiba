# coding: UTF-8

import glob
import os
import re
import random

class KeibaDatasets:
    def __init__(self):
        self.currentdir = os.getcwd()
        self.files = os.listdir(self.currentdir+'/data')
    def sanrenpuku(self, rand=False):
        return_list = []
        list = []
        #各ファイルごとにデータ整形
        for file_name in self.files:
            list_int = []
            sum = 0

            #１ファイルごとの指数の合計を計算
            #生の指数を配列に保存
            for line in open('data/'+file_name, 'r'):
                if len(line[:-1]):
                    alpha = line.split('\t')[3]
                    sum += int(alpha)
                    list_int.append(int(alpha))
            #指数の合計で1.0に正規化
            #[3つの馬の指数合計、指数最小値、指数最大値、1(正解)or0(不正解)]のファイルを作成
            for i in range(len(list_int)):
                for j in range(i+1, len(list_int)):
                    for k in range(j+1, len(list_int)):
                        a = float(list_int[i])/sum
                        b = float(list_int[j])/sum
                        c = float(list_int[k])/sum
                        val = [(a+b+c)/3.0, min(a,b,c), max(a,b,c), 1 if (i==0 and j==1 and k==2) else 0]
                        list.append(val)
                        if i==0 and j==1 and k==2:
                            return_list.append(val)
            false_val = random.randint(1,len(list)-1)
            return_list.append(list[false_val])
        return return_list if rand else list


if __name__ == '__main__':
    keiba = KeibaDatasets()
    list = keiba.sanrenpuku(True)

    for line in list:
        print line
        break
    print list[:3]
    print len(list)
