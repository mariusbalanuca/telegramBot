import urllib2
import time
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("marius.balanuca", "Rumpelstiltskina_22")
newprice = 0


def priceCall():
    price = 0
    site = "https://www.tomtop.com/p-pz0146b-eu.html"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site, headers=hdr)
    page = urllib2.urlopen(req)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page, "html.parser")
    soup.prettify("utf-8")
    for link in soup.findAll("span", {"class": "fz_orange pricelab"}):
        price = link.text
    return price

while True:
    if newprice < priceCall():
        newprice = priceCall()
        server.sendmail("marius.balanuca@gmail.com", "marius.balanuca@gmail.com", newprice)
    time.sleep(3600)
