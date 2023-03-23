# ODPT APIから都バス運行データを取得
import json
import requests
import time
import csv
import atexit
import datetime
import os

# プログラム停止時にSlackに通知を送るための関数。引数は送信するメッセージ。
# def sendNotificationToSlack(message):
#     webhook_url = "https://hooks.slack.com/services/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"
#     requests.post(webhook_url, data=json.dumps(
#         {
#             'text': message,
#             "link_names": 1
#         }
#     ))

# バスの運行データを取得し、CSVに書き込む
# url: ODPT APIにアクセスするためのURL
# outputFile: 出力CSVファイルのパス
def requestBusData(url, outputFile):
    # リクエストをtry
    try: 
        request = requests.get(url)
        request.raise_for_status()
    except requests.exceptions.RequestException as e: # HTTPエラー発生時
        print(e)
        # sendNotificationToSlack('@channel HTTP error: ' + str(request.status_code) + '(ASUS PC)')
        return

    jsonData = request.json()
    ##################################################
    c = True
    if(os.path.isfile(outputFile)):
        c = False
    print(c)
    file = open(outputFile, 'a',encoding="utf-8_sig",newline="") # append(追記)モード
    w = csv.writer(file)
    if c:
        wt = "date","timestamp","note","busroutePattern","startPole","terminalPole","busNumber","fromTime","fromPole","toPole"
        w.writerow(wt)
    ####################################################
    try:
        size = len(jsonData) # sizeは、現在走行中のバスの数と一致
        date = jsonData[0]['dc:date']
        date_data = date[:10]
        timestamp = date[11:19]
        print(date_data + ' ' + timestamp + ', ' + str(size) + ' buses running')
        for j in range(size):
            note = jsonData[j]['odpt:note']
            busroutePattern = jsonData[j]['odpt:busroutePattern'][26:]
            startingBusstopPole = jsonData[j]['odpt:startingBusstopPole'][22:]
            terminalBusstopPole = jsonData[j]['odpt:terminalBusstopPole'][22:]
            busNumber = jsonData[j]['odpt:busNumber']
            fromBusstopPoleTime = jsonData[j]['odpt:fromBusstopPoleTime'][11:19]
            fromBusstopPole = jsonData[j]['odpt:fromBusstopPole'][22:]
            toBusstopPole = jsonData[j]['odpt:toBusstopPole'][22:]
            w.writerow([date_data,timestamp,note,busroutePattern,startingBusstopPole,terminalBusstopPole,busNumber,fromBusstopPoleTime,fromBusstopPole,toBusstopPole])
    except IndexError:
        print("No JSON data")
    finally:
        file.close()


def main():
    # リクエストURLを作成
    base_url = "https://api.odpt.org/api/v4/odpt:Bus"
    MY_CONSUMER_KEY = "Your consumer key"
    
    # エラーハンドリングの関数を登録
    # atexit.register(sendNotificationToSlack, "@channel 都バスデータの取得が停止しました(渋滞検知Webサービス)") # Slack Incoming Webhook
    
    n = datetime.datetime.now() # 現在時刻の取得
    
    
    while True:
        while (n.hour < 9) | (n.hour>=22): # データ取得休止時間
            # 22時以降、使う予定のない、古いCSVのデータを削除
            d_today = datetime.date.today()  # CSVファイルの名前は日付としている。
            oldCSV = str(d_today) + ".csv" 
            if(os.path.isfile(oldCSV)):
                print("delete old CSV: " + oldCSV)
                os.remove(oldCSV)

            print("Now sleeping...")
            print(n)
            time.sleep(60)
            n = datetime.datetime.now()

        while (n.hour >= 9) & (n.hour<22): # データ取得時間 (30秒ごとにAPIにデータをリクエスト)
            d_today = datetime.date.today()  # CSVファイルの名前は日付としている。
            # URLの作成
            url = base_url + "?odpt:operator=odpt.Operator:Toei&acl:consumerKey=" + MY_CONSUMER_KEY
            requestBusData(url, str(d_today) + ".csv")
            time.sleep(30)

if __name__ == "__main__":
    main()
