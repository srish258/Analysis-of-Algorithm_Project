import time
import os, psutil
import sys
import copy
import gc
import tracemalloc

tracemalloc.start()

#begin = time.time()
mat=[]
def generateString(base_string, indices):
    result_string = base_string
    for i in indices:
        i = int(i)
        if i+1 < len(result_string):
            result_string = result_string[:i+1] + result_string + result_string[i+1:]
        else:
            result_string = result_string[:i+1] + result_string 
        #print(result_string)
    return result_string
      
# input generator : read from input.txt

def generateInputStrings(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
        lines = [x.replace("\n","") for x in lines]

        n = len(lines)
        X_base_string = lines[0]
        X_gen_indices = []
        i=1
        while i<n :
            index =  lines[i]
            if index.isdigit():
                X_gen_indices.append(index)
            else:
                break
            i+=1
        # print(X_base_string,X_gen_indices)
        X = generateString(X_base_string,X_gen_indices)

        Y_base_string = lines[i]
        Y_gen_indices = []
        i+=1
        while i<n:
            Y_gen_indices.append(lines[i])
            i+=1
        # print(Y_base_string,Y_gen_indices)
        Y = generateString(Y_base_string,Y_gen_indices)
        return X,Y
    
dp = []
alignmentA = ""
alignmentB = ""

nw_result=[0,0,0]

def nw(A, B):
    # The Needleman-Wunsch algorithm
    
    # Stage 1: Create a zero matrix and fills it via algorithm
    n, m = len(A), len(B)
    # mat = []
    dp = []
    # mat.clear()
    for i in range(n+1):
        dp.append([0]*(m+1))
    for j in range(m+1):
        dp[0][j] = gapPenalty*j
    for i in range(n+1):
        dp[i][0] = gapPenalty*i
    for i in range(1, n+1):
        for j in range(1, m+1):
            dp[i][j] = min(dp[i-1][j-1] + simMatrix[A[i-1]][B[j-1]], dp[i][j-1] + gapPenalty, dp[i-1][j] + gapPenalty)

    # Stage 2: Computes the final alignment, by backtracking through matrix
    alignmentA = ""
    alignmentB = ""
    i, j = n, m
    while i and j:
        score, scoreDiag, scoreUp, scoreLeft = dp[i][j], dp[i-1][j-1], dp[i-1][j], dp[i][j-1]
        if score == scoreDiag + simMatrix[A[i-1]][B[j-1]]:
            alignmentA = A[i-1] + alignmentA
            alignmentB = B[j-1] + alignmentB
            i -= 1
            j -= 1
        elif score == scoreUp + gapPenalty:
            alignmentA = A[i-1] + alignmentA
            alignmentB = '-' + alignmentB
            i -= 1
        elif score == scoreLeft + gapPenalty:
            alignmentA = '-' + alignmentA
            alignmentB = B[j-1] + alignmentB
            j -= 1
    while i:
        alignmentA = A[i-1] + alignmentA
        alignmentB = '-' + alignmentB
        i -= 1
    while j:
        alignmentA = '-' + alignmentA
        alignmentB = B[j-1] + alignmentB
        j -= 1
    # Now return result in format: [1st alignment, 2nd alignment, similarity]
    # nw_result[0]=alignmentA
    # nw_result[1]=alignmentB
    # nw_result[2]= dp[n][m]
    return [alignmentA, alignmentB, dp[n][m]]


def forwards1(x, y):
    n, m = len(x), len(y)
    # mat = []
    global mat
    # mat = [[0] * (m+1) for i in range(2)]
    # print("forwards1",mat)
    # print(m+1)
    for i in range(2):
        for j in range(m+1):
            mat[i][j]=0
    for j in range(m+1):
        mat[0][j] = gapPenalty*j
    for i in range(1, n+1):
        mat[1][0] = i * gapPenalty
        for j in range(1, m+1):
            mat[1][j] = min(mat[0][j-1] + simMatrix[x[i-1]][y[j-1]],
                            mat[0][j] + gapPenalty,
                            mat[1][j-1] + gapPenalty)
        # mat[0]= copy.deepcopy(mat[1])
        for j in range(len(mat[0])):
            mat[0][j]=mat[1][j]
    # global c
    # print("size = ",sys.getsizeof(mat),"c =",c)
    # c+=1
    return mat[1][:m+2]


def backwards1(x, y):

    n, m = len(x), len(y)
    global mat
    # mat = [[0] * (m+1) for i in range(2)]
    # print("forwards1",mat)
    # print(m+1)
    for i in range(2):
        for j in range(m+1):
            mat[i][j]=0
            
    for j in range(m+1):
        mat[0][j] = gapPenalty*j
    for i in range(1, n+1):
        mat[1][0] = i * gapPenalty
        for j in range(1, m+1):
            # mat[1][j] = min(mat[0][j-1] + simMatrix[x[i-1]][y[j-1]],
            #                 mat[0][j] + gapPenalty,
            #                 mat[1][j-1] + gapPenalty)
            
            mat[1][j] = min(mat[0][j-1] + simMatrix[x[n-i]][y[m-j]],
                            mat[0][j] + gapPenalty,
                            mat[1][j-1] + gapPenalty)
        # mat[0]= copy.deepcopy(mat[1])
        for j in range(len(mat[0])):
            mat[0][j]=mat[1][j]
    # print("size = ",sys.getsizeof(mat))
    return mat[1][:m+2]

def hirschberg(x, y):
    # This is the main Hirschberg routine.
    n, m = len(x), len(y)
    if n<2 or m<2:
        # In this case we just use the N-W algorithm.
        
        return nw(x,y)
    else:
        # Make partitions, call subroutines.
        F, B = forwards1(x[:n//2], y), backwards1(x[n//2:], y)
        partition = [F[j] + B[m-j] for j in range(m+1)]
        cut = partition.index(min(partition))
        # Clear all memory now, so that we don't store data during recursive calls.
        F, B, partition = [], [], []
        # Now make recursive calls.
        callLeft = hirschberg(x[:n//2], y[:cut])
        callRight = hirschberg(x[n//2:], y[cut:])
        # Now return result in format: [1st alignment, 2nd alignment, similarity]
        
        return [callLeft[r] + callRight[r] for r in range(3)]

gapPenalty = 30
# mismatch penalty
simMatrix = { 
    "A" : {"A" : 0,   "C" : 110, "G" : 48,  "T" : 94},
    "C" : {"A" : 110, "C" : 0,   "G" : 118, "T" : 48},
    "G" : {"A" : 48,  "C" : 118, "G" : 0,   "T" : 110},
    "T" : {"A" : 94,  "C" : 48,  "G" : 110,  "T": 0}
}
 
input_file = sys.argv[1]

def find_answer(input_file):
    begin = time.time()
    X,Y=generateInputStrings(input_file)    
    global mat
    mat = [[0] * (max(len(X),len(Y))+1) for i in range(2)]
    # print(mat)
    xAns,yAns,cost = hirschberg(X, Y)
    del mat  
    
    #print("Alignment of A: ", xAns)
    #print("Alignment of B: ", yAns)
    #print("Similarity score: ", cost)
    snapshot=tracemalloc.take_snapshot()
    top_stats=snapshot.statistics('traceback')
    stat = top_stats[0]
    print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
    for line in stat.traceback.format():
        print(line)
    end = time.time()
    # gc.collect(generation=2)
    process = psutil.Process(os.getpid())
    memory=process.memory_info().rss/1024
    
    #print(memory)
    #print("time:",end-begin)

    f = open("output_eff.txt", "a")
    #f.write(sys.argv[1][-5]+"\n")
    f.write(str(len(X))+" "+str(len(Y))+" "+str(len(X)+len(Y))+"\n")
    f.write("".join(xAns[:50])+" "+"".join(xAns[-50:])+"\n")
    f.write("".join(yAns[:50])+" "+"".join(yAns[-50:])+"\n")
    f.write(str(float(cost))+"\n")
    f.write(str(end-begin)+"\n")
    f.write(str(memory)+"\n")
    f.write("\n")
    f.close()
    f = open("time2.txt", "a")
    f.write(str(end-begin)+"\n")
    f.close()
    f = open("mem2.txt", "a")
    f.write(str(memory)+"\n")
    f.close()
    
    return len(X)+len(Y),end-begin,memory,cost

print(find_answer(input_file))