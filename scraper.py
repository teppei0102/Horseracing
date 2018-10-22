import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import joblib
import numpy as np
import os
from time import sleep

years = np.arange(1990,2018)
field = "06" ## 06:"Nakayama"   Ref: https://ja.wikipedia.org/wiki/Template:Netkeiba-raceresult
# month = np.array(["01","02","03","04","05","06","07","08","09","10","11","12"])
kai = np.array(["01","02","03","04","05"])
hi = np.array(["01","02","03","04","05","06","07","08","09"])
raceN = np.array(["01","02","03","04","05","06","07","08","09","10","11","12"])

for yr in years:
    for k in kai:
        for l in hi:
            for m in raceN:
                # URL = "http://db.netkeiba.com/race/201806030708/"
                URL = "http://db.netkeiba.com/race/"+(str)(yr)+field+k+l+m+"/"
                race = URL.split("/")[4]

                # getting sources
                resp = requests.get(URL)
                ## to avoid Mojibake
                resp.encoding = resp.apparent_encoding
                soup = bs(resp.text, "lxml")

                table = soup.find("table", attrs={"summary": "result of races"})

                if table == None:
                    print("pass:"+(str)(yr)+field+k+l+m)
                else:
                    rows = table.find_all("tr")

                    label = []
                    for i in rows[0].find_all("th"):
                        label.append(i.get_text())
                    label.insert(0,"games")

                    rows = rows[1:]
                    results = []
                    for j in range(len(rows)):
                        res = []
                        for i in rows[j].find_all("td"):
                            res.append(i.get_text().strip())
                        res.insert(0,race)
                        results.append(res)

                    if os.path.isfile("data.dat") == 0:
                        data = pd.DataFrame(columns=label)
                        for i in results:
                            data = data.append(pd.DataFrame([i], columns=label))
                        joblib.dump(data,"data.dat")
                    else:
                        data = joblib.load("data.dat")
                        if (str)(yr)+field+k+l+m in data.values:
                            print("skip")
                        else:
                            for i in results:
                                data = data.append(pd.DataFrame([i], columns=label))
                            joblib.dump(data,"data.dat")
                            print("get:"+(str)(yr)+field+k+l+m)
                sleep(2)
