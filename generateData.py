import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def generateData(alpha,rm,im =0.0,N_ta = 2**13-1):
    origin_path = os.getcwd()
    os.chdir("miedebye")
    exeName = "Mie_Calculation.exe"
    txtName = '输入参数文本.txt'

    Ta_min, Ta_max = 0,180
    with open(txtName,'w') as f1:
        f1.write('{}\n{:.3f}\t{:.5f}\n{}\t{:.2f}\t{:.2f}'
                .format(alpha,rm,im,N_ta,Ta_min,Ta_max))


    os.system(exeName)
    dataName = "散射光强角分布alpha={:.3f}m={:.5}.txt".format(alpha,rm)
    # 没想到c写出来的不是utf-8编码的，所以这里encoding='gbk'，后面这个delimiter随便要不要
    data = pd.read_csv(dataName,sep ='\t',engine='python',encoding='gbk',delimiter='\s+')
    # os.remove(dataName)
    os.chdir(origin_path)
    return data
if __name__ == "__main__":
    alpha, rm = eval(input('请输入alpha, rm \n'))
    generateData(alpha,rm)