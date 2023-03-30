# 発車時刻をバス停区間になるよう並び替え
# ex: 前のバス停の出発時刻,前のバス停名,次のバス停の出発時刻,次のバス停名
# 区間に15分以上かかる場合は削除(その区間を走っていない可能性が高い)
# 区間に1分未満しかかからない場合は削除
import time
import csv
# import datetime
from datetime import date,datetime,timedelta
# import pandas as pd
import csv
from collections import defaultdict
import math
import numpy as np

def main():
    from datetime import date,datetime,timedelta
    import pandas as pd
    import csv
    # 不要な情報と重複を削除

    nameCSV =  "all.csv" #都バス全データをマージしたもの
    rawalldf = pd.read_csv(nameCSV)
    rawalldf["date"] = pd.to_datetime(rawalldf["date"])
    selectdf = rawalldf[(rawalldf["date"]>=datetime(2022,12,18))&(rawalldf["date"]<=datetime(2022,12,31))]
    selectdf = selectdf.drop(["timestamp"],axis=1)
    selectdf = selectdf.drop_duplicates()

    # ソート

    selectdf = selectdf.sort_values(["busNumber","date","fromTime"])
    print(selectdf.head(3))
    print(selectdf.tail(3))


    selectdf.to_csv("allSortedtmp.csv",encoding="utf-8_sig",index=False)

    with open("allSortedtmp.csv","r",encoding="utf-8_sig")as selectedt:
        with open("allSorted.csv","w",encoding="utf-8_sig",newline="")as selected:
            rd = csv.reader(selectedt)
            wt = csv.writer(selected)
            lst = [row for row in rd]
            for i in range(len(lst)):
                wrt = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i][8]
                if i==0:
                    wt.writerow(wrt)
                    continue
                if lst[i-1][1]==lst[i][1]:
                    continue
                    
                wt.writerow(wrt)
    with open("allSorted.csv","r",encoding="utf-8_sig")as selected:
        with open("ordered.csv","w",encoding="utf-8_sig",newline="")as ordered:
            rd = csv.reader(selected)
            lst = [row for row in rd]
            wt = csv.writer(ordered)
            #header = "ID","BusNumber","Date","Weekday","busroutePattern","startPole","terminalPole","Busnumber","FromTime","FromPole","ToTime","ToPole"
            header = "BusNumber","Date","Weekday","FromTime","ToTime","DifSec","FromPole","ToPole","FromPoleJP","ToPoleJP"
            wt.writerow(header)
            
            for i in range(len(lst)-1):
                if i == 0: continue
                if (lst[i+1][5]!=lst[i][5])|(lst[i][0]!=lst[i+1][0]): continue
                if (lst[i][8]!=lst[i+1][7]):
                    continue
                
                fromTime = lst[i][6].split(":")
                toTime = lst[i+1][6].split(":")
                #print(int(fromTime[1]))
                #print(int(toTime[1]))
                diffTime = (int(toTime[0])-int(fromTime[0]))*3600
                
                diffTime += (int(toTime[1])-int(fromTime[1]))*60
                # print(diffTime)
                diffTime += int(toTime[2])-int(fromTime[2])
                
                
    #             if diffTime>=900: continue
    #             if diffTime<30: continue
                #print(fromTime)
                if (fromTime[0]=='06') | (fromTime[0]=='07') | (fromTime[0]=='08'):
                    continue
                fromjp = lst[i][1].split(" ")
                tojp = lst[i+1][1].split(" ")
                
                
                date = datetime.strptime(lst[i][0],"%Y-%m-%d")
                day = date.strftime("%A")
                
                #row = lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i+1][6],lst[i][8]
                row = lst[i][5],lst[i][0],day,lst[i][6],lst[i+1][6],diffTime,lst[i][7],lst[i][8],fromjp[2],tojp[2]
                wt.writerow(row)

    print(1)
    with open("ordered.csv","r",encoding="utf-8_sig")as ordered:
        with open("2secordered.csv","w",encoding="utf-8_sig",newline="")as tsec:
            with open("BusSectionList_all_1.csv","r",encoding="utf-8_sig") as busstop:
                rd = csv.reader(ordered)
                brd = csv.reader(busstop)
                bslst = [row for row in brd]
                lst = [row for row in rd]
                wt = csv.writer(tsec)
                header = "BusNumber","Date","Weekday","FromTime","ToTime","DifSec","FromPole","ToPole","FromPoleJP","ToPoleJP","passPole","passPoleJP"
                wt.writerow(header)
                for i in range(len(lst)-1):
                    if i==0:
                        continue
                    check = False
                    check2 = False
                    for j in range(len(bslst)):
                        if(lst[i][8]==bslst[j][0]) & (lst[i+1][9]==bslst[j][3]):
                            #print(lst[i][8]+" "+bslst[j][0]+" "+lst[i+1][9]+" "+bslst[j][3])
                            check = True
                            break
                        if(lst[i][8]==bslst[j][0]) & (lst[i][9]==bslst[j][3]):
                            check2 = True
                    if (check) & (lst[i][0]==lst[i+1][0]) & (lst[i][1]==lst[i+1][1]):
                        wrt = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i+1][4],int(lst[i][5])+int(lst[i+1][5]),lst[i][6],lst[i+1][7],lst[i][8],lst[i+1][9],lst[i][7],lst[i][9]
                        wt.writerow(wrt)
                    elif (check2):
                        wrt = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i][8],lst[i][9],"",""
                        wt.writerow(wrt)
    import csv
    from datetime import datetime
    from collections import defaultdict

    with open("2secordered.csv","r",encoding="utf-8_sig")as tsec:
        with open("Result_Google_all.csv","r",encoding="utf-8_sig") as result:
            with open("2secWITHtruth.csv","w",encoding="utf-8_sig",newline="") as wrtf:
                rdsec = csv.reader(tsec)
                rdrst = csv.reader(result)
                wt = csv.writer(wrtf)
                header = "BusNumber","Date","Weekday","FromTime","ToTime","DifSec","FromPole","ToPole","FromPoleJP","ToPoleJP","passPole","passPoleJP","length","velocity","isJam"
                wt.writerow(header)
                lst = [row for row in rdsec]
                truth = [row for row in rdrst]
                mp1 = defaultdict(float)
                mp2 = defaultdict(str)
                for j in range(len(truth)):
                    if j==0:
                        continue
                    tm = datetime.strptime(truth[j][0], "%Y/%m/%d")
                    trtime = truth[j][1].split(":")
                    secc = int(trtime[0])*60+int(trtime[1])
                    #print(secc)
                    secc //= 5
                    #print(secc)
                    secc *= 5
                    key = tm,secc,truth[j][2],truth[j][3]
                    mp1[key] = truth[j][5]
                    mp2[key] = truth[j][8]
                for i in range(len(lst)):
                    if i==0:
                        continue
                    bstime = datetime.strptime(lst[i][1], "%Y-%m-%d")
                    btime = lst[i][4].split(":")
                    secb = int(btime[0])*60+int(btime[1])
                    secb //= 5
                    secb *= 5
                    key = bstime,secb,lst[i][8],lst[i][9]
                    dist = mp1[key]
                    isJam = mp2[key]
                    if int(lst[i][5]) != 0:
                        wrtc = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i][8],lst[i][9],lst[i][10],lst[i][11],dist,float(dist)/float(lst[i][5]),isJam
                        wt.writerow(wrtc)
    import pandas as pd

    df = pd.read_csv("2secWITHtruth.csv")
    df = df.dropna()
    df.to_csv("data.csv",encoding="utf-8_sig",index=False)
    sdf = pd.read_csv("data.csv")
    sdf = sdf.sort_values(["Date","FromPoleJP","ToPoleJP","FromTime"])

    sdf.to_csv("data_v1.csv",encoding="utf-8_sig",index=False)

    import csv
    with open("data_v1.csv","r",encoding="utf-8_sig") as v1:
        with open("data_v2.csv","w",encoding="utf-8_sig",newline="") as v2:
            rd = csv.reader(v1)
            wt = csv.writer(v2)
            header = "BusNumber","Date","Weekday","FromTime","ToTime","DifSec","FromPole","ToPole","FromPoleJP","ToPoleJP","passPole","passPoleJP","length","v_i","isJam","v_i-1"
            wt.writerow(header)
            lst = [row for row in rd]
            for i in range(len(lst)):
                if i==0:
                    continue
                if (i==1)|((lst[i][8]!=lst[i-1][8])|(lst[i][9]!=lst[i-1][9])):
                    wrt = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i][8],lst[i][9],lst[i][10],lst[i][11],lst[i][12],lst[i][13],lst[i][14],lst[i][13]
                    wt.writerow(wrt)
                else:
                    wrt = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i][8],lst[i][9],lst[i][10],lst[i][11],lst[i][12],lst[i][13],lst[i][14],lst[i-1][13]
                    wt.writerow(wrt)

    import csv
    with open("data_v2.csv","r",encoding="utf-8_sig") as v2:
        with open("data_v3.csv","w",encoding="utf-8_sig",newline="") as v3:
            rd = csv.reader(v2)
            wt = csv.writer(v3)
            header = "BusNumber","Date","Weekday","FromTime","ToTime","DifSec","FromPole","ToPole","FromPoleJP","ToPoleJP","passPole","passPoleJP","length","v_i","isJam","v_i-1","v_i+1"
            wt.writerow(header)
            lst = [row for row in rd]
            for i in range(len(lst)):
                if i==0:
                    continue
                if (i==len(lst)-1):
                    wrt = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i][8],lst[i][9],lst[i][10],lst[i][11],lst[i][12],lst[i][13],lst[i][14],lst[i][15],lst[i][13]
                    wt.writerow(wrt)                
                elif ((lst[i][8]!=lst[i+1][8])|(lst[i][9]!=lst[i+1][9])):
                    wrt = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i][8],lst[i][9],lst[i][10],lst[i][11],lst[i][12],lst[i][13],lst[i][14],lst[i][15],lst[i][13]
                    wt.writerow(wrt)
                else:
                    wrt = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i][8],lst[i][9],lst[i][10],lst[i][11],lst[i][12],lst[i][13],lst[i][14],lst[i][15],lst[i+1][13]
                    wt.writerow(wrt)

    import csv
    with open("data_v3.csv","r",encoding="utf-8_sig") as v3:
        with open("data_v4.csv","w",encoding="utf-8_sig",newline="") as v4:
            rd = csv.reader(v3)
            wt = csv.writer(v4)
            header = "BusNumber","Date","Weekday","FromTime","ToTime","DifSec","FromPole","ToPole","FromPoleJP","ToPoleJP","passPole","passPoleJP","length","v_i","isJam","v_i-1","v_i+1","FromTimeNum","SectionNum","v_mean"
            wt.writerow(header)
            lst = [row for row in rd]
            for i in range(len(lst)):
                if i==0:
                    continue
                fromtime = lst[i][3].split(":")
                totime = lst[i][4].split(":")
                ftimenum = int(fromtime[0])*3600+int(fromtime[1])*60+int(fromtime[2])
                ftimenum //= 1200
    #             ttimenum = int(totime[0])*3600+int(totime[1])*60+int(totime[2])
    #             ttimenum //=1200
                wrt = lst[i][0],lst[i][1],lst[i][2],lst[i][3],lst[i][4],lst[i][5],lst[i][6],lst[i][7],lst[i][8],lst[i][9],lst[i][10],lst[i][11],lst[i][12],lst[i][13],lst[i][14],lst[i][15],lst[i][16],ftimenum
                wt.writerow(wrt)
    import csv
    with open("data_v4.csv","r",encoding="utf-8_sig")as v4:
        with open("BusSectionList_all_2.csv","r",encoding="utf-8_sig") as lst:
            with open("data_v5.csv","w",encoding="utf-8_sig",newline="") as v5:
                rd = csv.reader(v4)
                bls = csv.reader(lst)
                wt = csv.writer(v5)
                lst = [row for row in rd]
                blst = [row for row in bls]
                for i in range(len(lst)):
                    if i==0:
                        wt.writerow(lst[i])
                        continue
                    for j in range(len(blst)):
                        #print(blst[0],lst[8],blst[3],lst[9])
                        if (blst[j][0]==lst[i][8]) & (blst[j][3] == lst[i][9]):
                            lst[i].append(blst[j][12])
                            lst[i].append(blst[j][13])
                            wt.writerow(lst[i])
                            break
    

if __name__ == "__main__":
    main()