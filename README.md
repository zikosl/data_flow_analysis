#KNN
class pour tout knn non incremental

#KNNI (knnincremental.py)
class pour tout knn verion Incremental

pour le principe :

j'ai utilise fichier KDD1.txt et decoper en 2 fichier:
test.txt dataset sans class
train.txt dataset avec sans class

dans la class KNNI :
il ya 4 parametre trainset ,testset (pour la retrain et changer les frequence), stack pour les frequence
et l K

les 2 fonction start ->
le principe de mise a jour et que la mise jour fait pour l'instance de frequence minimum sans tenir compte la class
les 2 fonction startwithcondition ->
le principe de mise a jour et que la mise jour fait pour l'instance de frequence minimum avec tenir compte la class


les 2 fonction 
train avec le prametre size que signifier les instance que modifier les frequence
classify avec le prametre size que signifier les instance que modifier le dataset (length dataset-size)

