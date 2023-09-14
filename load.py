import pandas as pd
import read
import time 
from knn import KNN

train = 'NSL-KDD/KDDTrain+.txt'
test = 'NSL-KDD/KDDTest+.txt'

tf = read.ReadDATA(train)
tf = read.toDataset(tf)

tsf = read.ReadDATA(test)
tsf = read.toDataset(tsf)

newtf = [f[:-1] for f in tf]
newtsf = [f[:-1] for f in tsf]

true=0
false=0
start = time.time()
for instance in newtsf:
    Classifier = KNN(instance,newtf,3) 
    result = Classifier.Classify()
    if(result==instance[-1]):
        true+=1
    else:
        false+=1
start = time.time()-start
print(start)
print(true,false)