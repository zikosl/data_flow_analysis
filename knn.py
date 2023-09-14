import math
import operator

class KNN :
    def __init__(self,instance,dataset,k) :
        self.instance = instance
        self.dataset = dataset
        self.k = k
        
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
    
    def VoisinKNN(self):
        distance = []
        length = len(self.instance)-1
        for x in range(len(self.dataset)):
            dist = self.distanceEcludienne(self.instance,self.dataset[x],length)
            distance.append((self.dataset[x],dist,x))
        distance.sort(key=operator.itemgetter(1))
        voisins=[]
        IndiceDist=[]
        for x in range (self.k+1):
            voisins.append(distance[x][0])
            IndiceDist.append((distance[x][2],distance[x][1]))
        return voisins

    def Classify (self):
        voisins=self.VoisinKNN().copy()
        VoisinOccurance = {}
        for y  in range (len(voisins)):
            ClasseChoisie = voisins[y][-1]
            if ClasseChoisie in VoisinOccurance:
                VoisinOccurance[ClasseChoisie]+=1
            else:
                VoisinOccurance[ClasseChoisie]=1
        VoisinOccSorted = sorted(VoisinOccurance.items(),key=operator.itemgetter(1),reverse=True)             
        return VoisinOccSorted[0][0]