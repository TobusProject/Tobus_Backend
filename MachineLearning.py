import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.metrics import TruePositives, TrueNegatives, FalsePositives, FalseNegatives, Precision, Recall, AUC
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
import tensorflow.keras.backend as K
from imblearn.over_sampling import SMOTE
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
import csv
import keras
from collections import defaultdict
#import h5py

with open("../SourceData/Google/Cluster/kmeans_8.csv","r",encoding = "utf-8_sig") as cls:
    rdc  = csv.reader(cls)
    cls = [row for row in rdc]
    clst = defaultdict(int)
    cnum = 0
    for i in range(len(cls)):
        if cnum < int(cls[i][1]):
            cnum = int(cls[i][1])
#             print(cnum)
        clst[int(cls[i][0])] = int(cls[i][1])
    
    
    with open("../Result/ALL/ROC_cluster_kmeans_8.csv","w",encoding="utf-8_sig",newline="") as g:
        wt = csv.writer(g)
        with open("../SourceData/Google/Threshold_cluster_kmeans_8.csv","w",encoding = "utf-8_sig", newline="") as f:


            mlst = []
            print(cnum)
            for i in range(cnum+1):
                model = Sequential()
                model.add(Dense(9, input_dim=4))
                model.add(Activation("sigmoid"))
            #     model.add(Dense(9))
            #     model.add(Activation("sigmoid"))
                model.add(Dense(1))
                model.add(Activation("sigmoid"))
                model.compile(loss="binary_crossentropy",  
                      optimizer="adam",     
                      metrics=['accuracy',AUC()])
                mlst.append(model)
            print(mlst)
            traindf = pd.read_csv("../SourceData/Google/part1_f.csv")
            traindf = traindf.dropna()
            dflst = []
            df_blank = traindf.iloc[0:0]
            df_blank = df_blank.drop(['SectionNum'], axis=1)
            df_blank = df_blank.drop(['FromPole'], axis=1)
            df_blank = df_blank.drop(['ToPole'], axis=1)
            for i in range(cnum+1):
                dflst.append(df_blank)
            for SecNum in range(288):
                if SecNum == 0:
                    continue
                traindf1 = traindf.query('SectionNum==@SecNum')
                traindf1 = traindf1.drop(['SectionNum'], axis=1)
                traindf1 = traindf1.drop(['FromPole'], axis=1)
                traindf1 = traindf1.drop(['ToPole'], axis=1)

                tmp = pd.concat([dflst[int(clst[SecNum])],traindf1])
                dflst[int(clst[SecNum])] = tmp
            print(dflst[1].head())
            for i in range(cnum+1):
                print(i)
                traindf1 = dflst[i]
                traindf1 = traindf1.astype(float)
                traindf1['isJam'] = traindf1['isJam'].astype(int)
                train_y1 = traindf1['isJam']
                #train_y1 =  np_utils.to_categorical(train_y1)
                train_x1 = traindf1.drop(['isJam'],axis=1)
                sm = SMOTE()
                try:
                    train_x1, train_y1 = sm.fit_resample(train_x1, train_y1)
                except:
                    print("Failed to SMOTE in First step")

                history = mlst[i].fit(train_x1, train_y1, epochs=2000,batch_size = 200,verbose=1)

            for i in range(cnum+1):
                if i == 0:
                    continue

                mlst[i].pop()
                mlst[i].pop()


                for layer in mlst[i].layers[:3]:
                    layer.trainable = False
                #model.summary()

            traindfA = pd.read_csv("../SourceData/Google/part2_f.csv")
            testdf = pd.read_csv("../SourceData/Google/part12_f.csv")
            testdf_ = pd.read_csv("../SourceData/Google/part3_f.csv")
            AllTP = 0
            AllTN = 0
            AllFP = 0
            AllFN = 0
            for SecNum in range(288):
                traindfA1 = traindfA.query('SectionNum==@SecNum')
                traindfA1 = traindfA1.drop(['SectionNum'], axis=1)
                traindfA1 = traindfA1.drop(['FromPole'], axis=1)
                traindfA1 = traindfA1.drop(['ToPole'], axis=1)
            #     traindfA1 = traindfA1.drop(['FromTimeNum'], axis=1)
                traindfA1 = traindfA1.astype(float)
                traindfA1["isJam"] = traindfA1["isJam"].astype(int)
                print(traindfA1.info())
                train_y = traindfA1['isJam']
                #train_y =  np_utils.to_categorical(train_y)
                print(train_y)
                train_x = traindfA1.drop(['isJam'],axis=1)
                smt = SMOTE(k_neighbors=2)
                try:

                    train_x3, train_y3 = smt.fit_resample(train_x, train_y)
                except:
                    print("Failed to SMOTE")
                    continue

                modelA = Sequential()
                modelA.add(mlst[int(clst[SecNum])])
                modelA.add(Dense(9))
                modelA.add(Activation("sigmoid"))
                modelA.add(Dense(1))
                modelA.add(Activation("sigmoid"))
                modelA.compile(loss="binary_crossentropy",  
                          optimizer="adam",     
                          metrics=['accuracy',AUC()])
                testdf1 = testdf.query('SectionNum==@SecNum')
                testdf1 = testdf1.drop(['SectionNum'], axis=1)
                strFr = testdf1.FromPole
                strTo = testdf1.ToPole
                testdf1 = testdf1.drop(['FromPole'], axis=1)
                testdf1 = testdf1.drop(['ToPole'], axis=1)
                try:
                    history1 = modelA.fit(train_x3, train_y3, epochs=500, batch_size=50,verbose=0)
                except:
                    continue

                modelA.save("Models/all_cluster/kmeans_8/"+str(SecNum)+".h5",save_format="h5")

            #     testdf1 = testdf1.drop(['FromTimeNum'], axis=1)
                testdf1 = testdf1.astype(float)
                testdf1["isJam"] = testdf1["isJam"].astype(int)


                y_test = testdf1['isJam']
                x_test = testdf1.drop(['isJam'],axis=1)

#                 score = modelA.evaluate(x_test,y_test,verbose=1)
#                 print(score)
                TP = 0
                TN = 0
                FP = 0
                FN = 0

                result = []
                for i in range(len(x_test.index)):
                    tmp = x_test.iloc[[i], :]
                    pdc = modelA.predict(tmp, verbose=0)
                    result.append(pdc[0][0])
                idx = 0
                maxScore = 0
                maxth = 0.5
                print(result)
                try:
                    fpr, tpr, thresholds = roc_curve(y_test,result)
                    #aucs = roc_auc_score(y_test,result)
                    plt.plot(fpr, tpr, marker='o')
                    plt.xlabel('FPR: False positive rate')
                    plt.ylabel('TPR: True positive rate')
                    plt.grid()
                    plt.savefig('../Result/ALL/ROC_cluster/kmeans_8/sklearn_roc_curve'+str(SecNum)+'.png')
                    dist = 2
                    for i in range(len(thresholds)):
                        a = np.array([0,1])
                        b = np.array([fpr[i],tpr[i]])
                        d = np.linalg.norm(b-a)
                        if d < dist:
                            dist = d
                            maxth = thresholds[i]
                except:
                    print("Can't cal auc")
                f.write(str(maxth)+"\n")
                print(maxth)

                pred_y = []
                result = []
                testdf1 = testdf_.query('SectionNum==@SecNum')
                testdf1 = testdf1.drop(['SectionNum'], axis=1)
                strFr = testdf1.FromPole
                strTo = testdf1.ToPole
                testdf1 = testdf1.drop(['FromPole'], axis=1)
                testdf1 = testdf1.drop(['ToPole'], axis=1)
            #     testdf1 = testdf1.drop(['FromTimeNum'], axis=1)
                testdf1 = testdf1.astype(float)
                testdf1["isJam"] = testdf1["isJam"].astype(int)

                y_test = testdf1['isJam']
                x_test = testdf1.drop(['isJam'],axis=1)
                for i in range(len(x_test.index)):
                    tmp = x_test.iloc[[i], :]
                    pdc = modelA.predict(tmp, verbose=0)
                    result.append(pdc[0][0])

                for j in range(len(result)):
                    #print(result[j])
                    if result[j] < maxth:
                        pred_y.append(0)
                    else:
                        pred_y.append(1)

                for row in y_test:
            #        print(row)
                    if pred_y[idx]==row:
                        if pred_y[idx]==1:
                            TP+=1
                        else:
                            TN += 1
                    else:
                        if pred_y[idx]==1:
                            FP += 1
                        else:
                            FN += 1
                    idx += 1

                aucc = -1
                try:
                    aucc = roc_auc_score(y_test,pred_y)
                except:
                    print("Cannot calculate AUC score")

                print(strFr+", "+strTo)
                print("TP: ", end="")
                print(TP)
                print("TN: ", end="")
                print(TN)
                print("FP: ", end="")
                print(FP)
                print("FN: ", end="")
                print(FN)
                print("Accuracy: ", end="")
                Accuracy = 0
                if TP+TN+FP+FN != 0:
                    Accuracy = float((TP+TN)/(TP+TN+FP+FN))
                print(Accuracy)
                print("Precision: ", end="")
                Precision = -1
                if TP+FP!=0:
                    Precision = float((TP)/(TP+FP))
                print(Precision)
                print("Recall: ", end="")
                Recall = -1
                if TP+FN!=0:
                    Recall = float((TP)/(TP+FN))
                print(Recall)
                F1 = -1
                if Precision+Recall!=0:
                    F1 = 2*(Precision*Recall)/(Precision+Recall)
                print("F1 score: ", end="")
                print(F1)
                AllTP += TP
                AllTN += TN
                AllFP += FP
                AllFN += FN     

                wrt = strFr,strTo,Accuracy,Precision,Recall,F1,maxth,aucc,TP,TN,FP,FN,int(clst[SecNum])
                wt.writerow(wrt)
                plt.clf()
                keras.backend.clear_session()
            wrt = AllTP,AllTN,AllFP,AllFN
            wt.writerow(wrt)