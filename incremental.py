import time
import utile
import read
from knnIncremantl import KNNI


train = "train.txt"
test = "test.txt"

train = read.ReadDATA(train)
test = read.ReadDATA(test)
train = read.toDataset(train)
test = read.toDataset(test)

print(len(test),len(train))
stack = [0]*len(train)

instance=[0,'tcp','private','REJ',0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,120,18,0,0,1,1,0.15,0.08,0,255,18,0.07,0.08,0,0,0,0,1,1,'']
print("###### Start train #######")

Incremental = KNNI(test,train,stack,3)
Incremental.start()
print("###### end Train #######")
start = time.time()
result = Incremental.ClassifyI(instance)
start = time.time()-start

print("###### without check class in update #######")
print(start)
print("class : ",result[-1])

stack = [0]*len(train)
print("###### Start train #######")

IncrementalWithCondition = KNNI(test,train,stack,3)
IncrementalWithCondition.startWithCondition()
print("###### end Train #######")
start = time.time()
result = Incremental.ClassifyI(instance)
start = time.time()-start
print("###### with check class in update #######")
print(start)
print("class : ",result[-1])
