from tensorflow.python.keras.models import load_model
import pandas as pd
import time
import datetime
import csv

allSection = 288
global trafficinfo
trafficinfo = []
def main():
    df = pd.read_csv("data_now.csv")
    #trafficinfo_new = [0]*(allSection+1)
    with open("Threshold.csv","r",encoding="utf-8_sig") as th:
        dbgEMPTY = [] ###############################
        for SecNum in range(allSection):
            if SecNum == 0:
                continue
            threshold = th.readline()
            threshold = threshold.split(",")
            threshold1 = float(threshold[1])
            #print(threshold1)
            filename = "Models/WebService/" + str(SecNum) + ".h5"
            try:
                model = load_model(filename)
            except:
                #trafficinfo_new[SecNum] = trafficinfo[SecNum]
                continue
            df1 = df.query("SectionNum==@SecNum")
            #print(df1.head())
            df1 = df1.dropna()
            
            if len(df1) == 0:
                if trafficinfo[SecNum] == 1:
                    dbgEMPTY.append(SecNum) ########################
                #trafficinfo[SecNum] = trafficinfo[SecNum]
                # print("Empty")
                continue
            # df1 = df1.drop(["isJam"],axis = 1)
            df1 = df1.drop(["SectionNum"],axis = 1)
            df1 = df1.reset_index(drop=True)
            #print(df1)
            service_df = pd.DataFrame()
            if len(df1)==1:
                service_df = df1
            else:
                service_df = df1
                v_mean = df1["v_i"].mean()
                v2_mean = df1["v_i-1"].mean()
                #print("v_mean: ",v_mean)
                service_df.iat[0,0] = v_mean
                service_df.iat[0,1] = v2_mean
                #print(service_df)
                service_df = service_df[0:1]

            #print(service_df.head())
            if (service_df["v_i"].item()*3.6) >= 14:
                trafficinfo[SecNum] = 0
                continue
            #print(service_df.head())
            tmp = service_df.iloc[[0], :]
            pdc = model.predict(tmp, verbose=0)
            #print(pdc)
            if pdc[0][0] >= threshold1:
                trafficinfo[SecNum] = 1
            else:
                trafficinfo[SecNum] = 0
        print(dbgEMPTY) ##########################
        with open("trafficinfo.csv","w",encoding="utf-8_sig",newline="") as f:
            wt = csv.writer(f)
            result = []
            now = datetime.datetime.now()
            d = now.strftime("%Y年%m月%d日 %H時%M分")
            result.append(d)
            for SecNum in range(allSection):
                if trafficinfo[SecNum] == 1:
                    result.append(str(SecNum))
            
            wt.writerow(result)



if __name__ == "__main__":
    trafficinfo = [0]*(allSection+1)
    # main(trafficinfo)
    initial = [0]*(allSection+1)
    n = datetime.datetime.now()
    while (n.hour < 9) | (n.hour>=22):
        trafficinfo = initial
        time.sleep(300)
    while (n.hour >= 9) & (n.hour<22): 
        main()
        time.sleep(300)