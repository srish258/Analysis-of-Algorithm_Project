import sys
import psutil 
import os 
import time
def GS(str_base,str_genratedIndices):
    str_update = str_base

    for i in str_genratedIndices:
        i = int(i)
        if i+1 >= len(str_update):
            str_update = str_update[:i+1] + str_update
        else:
            str_update = str_update[:i+1] + str_update + str_update[i+1:]

    return str_update

def GIS(input_file):
    with open(input_file,"r") as f:
        input_lines = f.readlines()
        input_lines = [x.replace("\n","") for x in input_lines]
        #total size of input n
        n = len(input_lines)

        str1_base = input_lines[0]
        str1_genratedIndices = []
        i = 1
        while i<n:
            position_j = input_lines[i]
            if position_j.isdigit():
                str1_genratedIndices.append(position_j)
            else:
                break
            i+=1
        
        str1 = GS(str1_base,str1_genratedIndices)
        
        str2_base = input_lines[i]
        str2_genratedIndices = []
        i += 1
        while i<n:
            position_k = input_lines[i]
            if position_k.isdigit():
                str2_genratedIndices.append(position_k)
            else:
                break
            i+=1
        str2 = GS(str2_base,str2_genratedIndices)
        return str1,str2


'''
from nw.py,
implementing nw algo
'''

def SequenceAlignment_NWalgo(str1,str2, gapPenalty, MPmatrix):
    # implementing stage 1
    n= len(str1)
    m=len(str2) 
    dp = []
    for i in range(n+1):
        dp.append([0]*(m+1))
    for j in range(n+1):
        dp[j][0] = gapPenalty*j
    for k in range(m+1):
        dp[0][k] = gapPenalty*k
    for j in range(1,n+1):
        for k in range(1, m+1):
            dp[j][k] = min(dp[j-1][k-1] + MPmatrix[str1[j-1]][str2[k-1]], dp[j][k-1] + gapPenalty, dp[j-1][k] + gapPenalty)
    
    #implement stage 2
    align_str1= ""
    align_str2 = ""
    j = n
    k = m

    while j and k:
        value = dp[j][k]
        valueDiag = dp[j-1][k-1]
        valueUp = dp[j-1][k]
        valueLeft = dp[j][k-1]
        if value == valueDiag + MPmatrix[str1[j-1]][str2[k-1]]:
            align_str1 = str1[j-1] + align_str1
            align_str2 = str2[k-1] + align_str2
            j -= 1
            k -= 1
        elif value == valueUp + gapPenalty:
            align_str1 = str1[j-1] + align_str1
            align_str2 = '_' + align_str2
            j -= 1
        elif value == valueLeft + gapPenalty:
            align_str1 = '_' + align_str1
            align_str2 = str2[k-1] + align_str2
            k -= 1
    # for remaining ---
    while j:
        align_str1 = str1[j-1] + align_str1
        align_str2 = '_' + align_str2
        j -= 1
    while k:
        align_str1 = '_' + align_str1
        align_str2 = str2[k-1] + align_str2
        k -= 1
    return ["".join(align_str1[id:id+51]) + " " + "".join(align_str1[-50:]), "".join(align_str2[id:id+51]) + " " + "".join(align_str2[-50:]), dp[n][m]]
    





gapPenalty = 30
# mismatch penalty
MPmatrix = { 
    "A" : {"A" : 0,   "C" : 110, "G" : 48,  "T" : 94},
    "C" : {"A" : 110, "C" : 0,   "G" : 118, "T" : 48},
    "G" : {"A" : 48,  "C" : 118, "G" : 0,   "T" : 110},
    "T" : {"A" : 94,  "C" : 48,  "G" : 110,  "T": 0}
}
begin=time.time()
input_file = sys.argv[1]
X_str1,Y_str2=GIS(input_file)    
X_str1_result,Y_str2_result,cost = SequenceAlignment_NWalgo(X_str1, Y_str2,gapPenalty, MPmatrix)
end=time.time()
process = psutil.Process(os.getpid())
memory=process.memory_info().rss/1024
# print(memory,cost)
f = open("output2.txt", "a")
f.write(X_str1_result+"\n")
f.write(Y_str2_result+"\n")
f.write(str(cost)+"\n")
f.write(str(end-begin)+"\n")
f.write(str(memory)+"\n")
f.close()
f = open("mem2.txt", "a")
f.write(str(memory)+"\n")
f.close()
f = open("time2.txt", "a")
f.write(str(end-begin)+"\n")
f.close()


