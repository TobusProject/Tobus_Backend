import pandas as pd
import csv
from datetime import datetime

alldf = pd.read_csv("../../SourceData/Google/data_v5.csv")
alldf["Date"] = pd.to_datetime(alldf["Date"])
alldf = alldf.drop(["BusNumber"],axis=1)
# alldf = alldf.drop(["Date"],axis=1)
alldf = alldf.drop(["Weekday"],axis=1)
alldf = alldf.drop(["FromTime"],axis=1)
alldf = alldf.drop(["ToTime"],axis=1)
alldf = alldf.drop(["DifSec"],axis=1)
alldf = alldf.drop(["FromPoleJP"],axis=1)
alldf = alldf.drop(["ToPoleJP"],axis=1)
alldf = alldf.drop(["passPole"],axis=1)
alldf = alldf.drop(["passPoleJP"],axis=1)
alldf = alldf.drop(["length"],axis=1)
alldf = alldf.drop(["v_i+1"],axis=1)
alldf["SectionNum"] = alldf["ToTimeNum"]
alldf = alldf.drop(["ToTimeNum"],axis=1)

part1 = alldf[(alldf["Date"]>=datetime(2022,11,30))&(alldf["Date"]<=datetime(2022,12,13))]
part2 = alldf[(alldf["Date"]>=datetime(2022,12,18))&(alldf["Date"]<=datetime(2022,12,24))]
part3 = alldf[(alldf["Date"]>=datetime(2022,12,25))&(alldf["Date"]<=datetime(2022,12,31))]

part1 = part1.drop(["Date"],axis=1)
part2 = part2.drop(["Date"],axis=1)
part3 = part3.drop(["Date"],axis=1)

part1.to_csv("../../SourceData/Google/part1.csv",encoding="utf-8_sig",index=False)
part2.to_csv("../../SourceData/Google/part2.csv",encoding="utf-8_sig",index=False)
part3.to_csv("../../SourceData/Google/part3.csv",encoding="utf-8_sig",index=False)

import csv

with open("../../SourceData/Google/part1.csv","r",encoding="utf-8_sig") as f:
    with open("../../SourceData/Google/part1_d.csv","w",encoding="utf-8_sig", newline="") as g:
        rd = csv.reader(f)
        wt = csv.writer(g)
        lst = [row for row in rd]
        for i in range(len(lst)):
            #print(lst[i][14])
            if i==0:
                wt.writerow(lst[i])
                continue
            elif (float(lst[i][2])*3.6>=14):
                continue
            else:
                if lst[i][3] == "False":
                    lst[i][3] = "0"
                else:
                    lst[i][3] = "1"
            wt.writerow(lst[i])
with open("../../SourceData/Google/part2.csv","r",encoding="utf-8_sig") as f:
    with open("../../SourceData/Google/part2_d.csv","w",encoding="utf-8_sig", newline="") as g:
        rd = csv.reader(f)
        wt = csv.writer(g)
        lst = [row for row in rd]
        for i in range(len(lst)):
            if i==0:
                wt.writerow(lst[i])
                continue
            elif (float(lst[i][2])*3.6>=14):
                continue
            else:
                if lst[i][3] == "False":
                    lst[i][3] = "0"
                else:
                    lst[i][3] = "1"
            wt.writerow(lst[i])
with open("../../SourceData/Google/part3.csv","r",encoding="utf-8_sig") as f:
    with open("../../SourceData/Google/part3_d.csv","w",encoding="utf-8_sig", newline="") as g:
        rd = csv.reader(f)
        wt = csv.writer(g)
        lst = [row for row in rd]
        for i in range(len(lst)):
            if i==0:
                wt.writerow(lst[i])
                continue
#             elif (float(lst[i][2])*3.6>=14):
#                 continue
            else:
                if lst[i][3] == "False":
                    lst[i][3] = "0"
                else:
                    lst[i][3] = "1"
            wt.writerow(lst[i])