import requests
import json





if __name__ == "__main__":
    with open(r"C:\\Users\\rayan\Documents\\pihole.txt") as file:
        API = file.readlines()[0]
    IP = "192.168.0.28"
    TotalURL='http://{0}/admin/api.php?{1}&auth={2}'
    TotalURLWOa='http://{0}/admin/api.php?{1}'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    headers = {'User-Agent': user_agent}
    

    # try:
    resp = requests.get(url=TotalURL.format(IP,'summary',API), headers=headers)
    print(resp)
    data=resp.json()
    # resultList = list(data.items())
    # resultList.pop(-1)
    # ans='ADS today:'+data['ads_percentage_today']+'%\n'+ 'Status '+data['status']
    print(data)
    # except Exception as error:
    #     print(error)
    print()
