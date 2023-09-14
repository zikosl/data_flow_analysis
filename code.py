import pandas as p
import random
import math
import time
import operator
#from  pycm import * 

class KNN:
    #################################
    def ReadDataSet(self , filename):
        d= p.read_csv(filename, sep=',')
        return d

    ####################################################
    def distanceEcludienne(self,line1 , line2 , length):
        distance=0         
        for x in range(length):
            if ((type(line1[x]) == str) | (type(line2[x]) == str)):
                if (line1[x]==line2[x]):
                    distance=0
                else:
                    distance=1
            else:
                distance += pow((line1[x]-line2[x]),2)
                          
        return math.sqrt(distance)

    ###################################################
    def VoisinKNN(self,instanceTest , trainingSet , k):
        distance = []
        # dans le length de test on mis -1 psk le test ne contient pas de classe(label)
        length = len(instanceTest)-1
        for x in range(len(trainingSet)):
            dist = KNN.distanceEcludienne(self,instanceTest,trainingSet[x],length)
            distance.append((trainingSet[x],dist,x))
        distance.sort(key=operator.itemgetter(1))
            
        voisins=[]
        IndiceDist=[]
        for x in range (k+1):
            voisins.append(distance[x][0])
            #Indice fiha Element , la distance , et l'indice de l'element
            IndiceDist.append((distance[x][2],distance[x][1]))
        print("Indice,Distance = ")
        print(IndiceDist)    
        return voisins

    #####################################################################
    def DivideDataset(self ,d , split , trainingDataset=[] , testSet=[]):
        count=0
        voisins=[]
        #X dans les ligne et Y dans les colonne
        lignes=d.values
        dataset = lignes.tolist()
        print("la longeur du dataset",len(dataset))
        for x in range (1,len(dataset)):
            a = random.random()
            if a < split:
               trainingDataset.append(dataset[x])
            else:
               testSet.append(dataset[x])
                            
        return trainingDataset,testSet

    ##################################################
    def ClassifyI (self,trainingDataset , instance,K):
        voisins=KNN.VoisinKNN(self,instance , trainingDataset , K).copy()
        VoisinOccurance = {}
        for y  in range (len(voisins)):
            #voisins[x][-1] le x correspond a la ligne et le -1 on travaille par modulo il correspond a la derniere case(c'est la classe)
            ClasseChoisie = voisins[y][-1]
            if ClasseChoisie in VoisinOccurance:
                VoisinOccurance[ClasseChoisie]+=1
            else:
                VoisinOccurance[ClasseChoisie]=1

        VoisinOccSorted = sorted(VoisinOccurance.items(),key=operator.itemgetter(1),reverse=True)
        print('la classe est:')
        print(VoisinOccSorted[0][0])
        for x in range(len(instance)):
            if(x == (len(instance)-1)):
                instance[x]=VoisinOccSorted[0][0]
                print("instance: " ,instance[x])
                       
        return VoisinOccSorted[0][0]

    ######################################
    def ADDToList( self, train, instance):
        train.append(instance)
        print(len(instance))
        return train

    #########################################
    def ADDToFile(self ,filename , instance):
        
        with open(filename,'a') as f:    
        #f = open (filename, "w")
            for i in range(0,len(instance)-1):
                f.write(str(instance[i])+",")
            f.write(str(instance[len(instance)-1]))    
            f.write("\n")
            f.close()
        
###############################################
start_time = time.time()            
#cree un objet
Obj1=   KNN()

#Appelle d'une method de la classe
d = KNN.ReadDataSet(Obj1,r'KDD1.txt')
dataset = KNN.DivideDataset(Obj1,d , 0.66 , [] , [])    
train=dataset[0]

print("***********Classification à base d'une Instance*******************")
#instance=[195,196,114,114,114,0,'TEST','INSTANCE','TCP',214,1462,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,8,8,0.0,0.0,0,0,1.0,0.0,0.0,255,255,1.0,0.0,0.0,0.0,0.0,0.0,0.01,0.01,'']
instance=[0,'tcp','private','REJ',0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,120,18,0,0,1,1,0.15,0.08,0,255,18,0.07,0.08,0,0,0,0,1,1,''
]
TestDataset = KNN.ClassifyI( Obj1, dataset[0] , instance, 3 )

print("Resultat de la fonction classify à base d'une instance=")
print(TestDataset)

data = KNN.ADDToList(Obj1, train ,instance)
KNN.ADDToFile(Obj1,r'newDataKDD.txt', instance)


