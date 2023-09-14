import math
import operator

class KNNI :
    def __init__(self,instances,dataset,stack,k) :
        self.instances = instances
        self.dataset = dataset
        self.k = k
        self.stack = stack
    
    def start(self,size=10,MinDistance=0):
        self.train(size)
        self.Classify(size,self.update,MinDistance)

    def startWithCondition(self,size=10,MinDistance=0):
        self.train(size)
        self.Classify(size,self.updateWithCondition,MinDistance)

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
    
    def VoisinKNN(self,instance):
        distance = []
        length = len(instance)-1
        for x in range(len(self.dataset)):
            dist = self.distanceEcludienne(instance,self.dataset[x],length)
            distance.append((self.dataset[x],dist,x))
        distance.sort(key=operator.itemgetter(1))
        voisins=[]
        distances =[]
        for x in range (self.k+1):
            voisins.append(distance[x][0])
            self.stack[distance[x][2]] += 1
            distances.append((distance[x][1]))
        return voisins,min(distances)

    def train (self,size):
        for i in  range(size):
            result = self.VoisinKNN(self.instances[i])
            voisins=result[0].copy()
            VoisinOccurance = {}
            for y  in range (len(voisins)):
                ClasseChoisie = voisins[y][-1]
                if ClasseChoisie in VoisinOccurance:
                    VoisinOccurance[ClasseChoisie]+=1
                else:
                    VoisinOccurance[ClasseChoisie]=1
            VoisinOccSorted = sorted(VoisinOccurance.items(),key=operator.itemgetter(1),reverse=True)            
            self.instances[i][-1] = VoisinOccSorted[0][0]
            
        
    def Classify (self,size,callback,mini):
        for i in  range(size,len(self.instances)):
            result = self.VoisinKNN(self.instances[i])
            voisins=result[0].copy()            
            VoisinOccurance = {}
            for y  in range (len(voisins)):
                ClasseChoisie = voisins[y][-1]
                if ClasseChoisie in VoisinOccurance:
                    VoisinOccurance[ClasseChoisie]+=1
                else:
                    VoisinOccurance[ClasseChoisie]=1
            VoisinOccSorted = sorted(VoisinOccurance.items(),key=operator.itemgetter(1),reverse=True)            
            self.instances[i][-1] = VoisinOccSorted[0][0]
            if(mini<result[1]):            
                callback(self.instances[i])
    
    def ClassifyI (self,instance):
        result = self.VoisinKNN(instance)
        voisins=result[0].copy()
        VoisinOccurance = {}
        for y  in range (len(voisins)):
            ClasseChoisie = voisins[y][-1]
            if ClasseChoisie in VoisinOccurance:
                VoisinOccurance[ClasseChoisie]+=1
            else:
                VoisinOccurance[ClasseChoisie]=1
        VoisinOccSorted = sorted(VoisinOccurance.items(),key=operator.itemgetter(1),reverse=True)            
        instance[-1] = VoisinOccSorted[0][0]       
        return instance
        
    def MinValue (self):
        return self.stack.index(min(self.stack))

    def update (self,instance):
        i = self.MinValue()
        self.dataset[i] = instance

    def MinValues (self,key):
        minimum = max(self.stack)+1
        index=-1
        for i in  range(len(self.stack)):
            if(key == self.dataset and self.stack[i]<minimum):
                index = i
                minimum=self.stack[i]
        return index
        
    def updateWithCondition (self,instance):
        i = self.MinValues(instance[-1])
        self.dataset[i] = instance
