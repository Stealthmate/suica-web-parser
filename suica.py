from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from pyquery import PyQuery as pq
from datetime import datetime as dt, timedelta, date

HOME = "https://www.mobilesuica.com/index.aspx"
HISTORY = "https://www.mobilesuica.com/iq/ir/SuicaDisp.aspx?returnId=SFRCMMEPC03"

HEADERS = {
  "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}

def getCookies(driverpath, username='', password=''):
    opts = Options()
    opts.add_argument('--window-size=500,600')
    opts.add_argument('--app={}'.format(HOME))
    if driverpath:
        driver = webdriver.Chrome(chrome_options=opts, executable_path=driverpath)
    else:
        driver = webdriver.Chrome(chrome_options=opts)
        
    elem = driver.find_element_by_name('MailAddress')
    elem.send_keys(username)
    elem = driver.find_element_by_name('Password')
    elem.send_keys(password)
    while(driver.current_url == HOME):
        pass
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

def parseSuicaDate(d):
    now = dt.now()
    lastYear = (now.replace(day=1) - timedelta(days=30 * 6)).year
    thisYear = now.year

    month = int(d.split("/")[0])
    day = int(d.split("/")[1])

    return date(lastYear if month > 5 else thisYear, month, day)

def processHtml(html):

    if "利用履歴表示が可能な時間" in html:
        print("ERROR: Cannot sync between 00:50 ~ 05:00")

    r = pq(html)
    rows = r("td > table > tr > td > table > tr")
    transactions = []
    for r1 in rows[1:]:
        t = pq(r1)("td").text().split(" ")
        sd = parseSuicaDate(t[0])
        t1 = {
            'issuedAt': str(sd),
            'type1': t[1],
            'issuer1': t[2],
            'type2': t[3],
            'issuer2': t[4],
            'balance': int(t[5].replace('¥', '').replace(',', '')),
            'amount': 0 if len(t[6]) == 0 else int(t[6].replace(',', ''))
        }
        transactions.append(t1)
    return transactions

def fetchRawHtml(cookies):
    return requests.post(HISTORY, headers=HEADERS, cookies=cookies).text

def fetchHistory(cookies):
    html = fetchRawHtml(cookies)
    return processHtml(html)

def parseHistory(username, password, driverpath):
    c = getCookies(driverpath, username, password)
    c = { x['name']: x['value'] for x in c }
    return fetchHistory(c)
