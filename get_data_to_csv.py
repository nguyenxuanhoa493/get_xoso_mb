import datetime
from email import header
import pendulum
import requests
from bs4 import BeautifulSoup
import re
import csv
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def gen_url(time_date):
    return pendulum.from_timestamp(time_date, tz='Asia/Bangkok').format('DD-MM-YYYY')
    
def get_data_a_day(date):
    print('Xử lý ngày: '+date)
    url='https://ketqua1.net/xo-so-mien-bac.php?ngay='+date
    response = requests.request("GET", url, headers=HEADERS,)
    soup = BeautifulSoup(response.text)
    try:
        result_tab_mb = soup.find_all(id='result_tab_mb')[0].findAll('tr')[2:]
        count=0
        list_lo=[]
        for i in result_tab_mb:
            giai = re.findall('[0-9]+', i.get_text())[0]
            if count < 4:
                list_lo+=cut_str(giai,5)
            elif count==4 or count ==5:
                list_lo+=cut_str(giai,4)
            elif count==6:
                list_lo+=cut_str(giai,3)
            else:
                list_lo+=cut_str(giai,2 )
            count+=1

        list_lo_uni=[]
        for x in list_lo:
            if x not in list_lo_uni:
                list_lo_uni.append(x)       
        with open('data.csv','a') as file:
            writer = csv.writer(file)
            is_best=True
            date =date[-4:]+date[2:6]+date[:2]
            for lo in list_lo_uni:
                val =[date,lo,str(list_lo.count(lo)),'1'] if is_best else [date,lo,str(list_lo.count(lo)),'0']
                print(val)
                writer.writerow(val)
                is_best=False
    except:
        pass

def cut_str(text,space):
    ls=[]
    s=0
    for i in range(0,len(text),space):
        s+=space
        ls.append(text[i:s][-2:])
    return ls

START_DATE='05-01-2002'
start_time=int(datetime.datetime.strptime(START_DATE, '%d-%m-%Y').strftime("%s"))

END_DATE = '10-01-2002'
end_time=int(datetime.datetime.strptime(END_DATE, '%d-%m-%Y').strftime("%s"))
with open('data.csv','w') as file:
    writer = csv.writer(file)
    hearder_csv=["Date","Number","Count","is_best"]
    writer.writerow(hearder_csv)
while start_time <= end_time:
    get_data_a_day(gen_url(start_time))
    start_time+=86400

