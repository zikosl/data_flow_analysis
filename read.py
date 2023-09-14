import pandas as p
import random

def ReadDATA(filename):
    d= p.read_csv(filename, sep=',')
    return d

def ADDToList(train, instance):
    train.append(instance)
    return train

def ADDToFile(filename , instance):
    
    with open(filename,'a') as f:    
        for i in range(0,len(instance)-1):
            f.write(str(instance[i])+",")
        f.write(str(instance[len(instance)-1]))    
        f.write("\n")
        f.close()

def SaveToFile(filename , dataset):
    with open(filename,'w') as f:
        for instance in dataset:
            for i in range(0,len(instance)-1):
                f.write(str(instance[i])+",")
            f.write(str(instance[len(instance)-1]))    
            f.write("\n")
        f.close()

def toDataset(data):
    lignes=data.values
    dataset = lignes.tolist()
    return dataset

def DivideDataset(data , split):
    lignes=data.values
    dataset = lignes.tolist()
    trainingDataset=[]
    testSet=[]
    for x in range (1,len(dataset)):
        a = random.random()
        if a < split:
            trainingDataset.append(dataset[x])
        else:
            val = dataset[x]
            val[-1] = ''
            testSet.append(val)
                        
    return trainingDataset,testSet