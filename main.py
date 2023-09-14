import utile
import read
from knn import KNN
import time

path = "KDD1.txt"
newpath = "newKDD.txt"

dataset = read.ReadDATA(path)

dataset = read.DivideDataset(dataset,0.66)

read.SaveToFile("train.txt",dataset[0])
read.SaveToFile("test.txt",dataset[1])

instance=[0,'tcp','private','REJ',0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,120,18,0,0,1,1,0.15,0.08,0,255,18,0.07,0.08,0,0,0,0,1,1,'']
print("###### kNN Non Incremental #######")

start = time.time()
Classifier = KNN(instance,dataset[0],3) 
result = Classifier.Classify()

instance[-1] = result
start = time.time()-start
print(start)
print("la class: ",result)

read.ADDToList(dataset[0],instance)
read.ADDToFile(newpath,instance)
