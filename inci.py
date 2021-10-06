import requests as rq
from bs4 import BeautifulSoup as bs
from time import sleep
import json

e_id = ""
inci = "http://incisozluk.com.tr/api/?key=android&v=beta&ne="
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "www.incisozluk.com.tr",
            "Referer": "http://www.incisozluk.com.tr/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}


class Entry_Sil:

    def __init__(self,nick,sifre):
        self.user_data = self.login(nick, sifre)
        if not self.user_data["error"]:
            self.nick = nick.replace(" ","-")
            self.token = self.user_data["token"]
            self.uye_id = self.user_data["user"]["uye_id"]
            self.profil_url = f"{inci}profil&uye_id={self.uye_id}"
            self.profil_jsn = self.entrySayisi()
            self.entry_sayisi = self.profil_jsn["uyebilgileri"]["entrysayisi"]


    def login(self,nick,sifre):
        url = f"{inci}login"
        data = {"kuladi":nick,
                "sifre":sifre}

        r = rq.post(url,headers=headers,data=data)
        user_data = r.json()

        return user_data


    def entrySayisi(self):
        profil = rq.get(self.profil_url,headers=headers)
        profiljsn = profil.json()
        return profiljsn


    def nerdenBasla(self):

        if self.entry_sayisi < 20000:
            return "/son-entry/?list=liste"
        elif len(self.profiljsn['sonsukulanan']) != 0:
            return"/son-suku/"
        return "/son-cuku/"


    def link_al(self,adet):
        silinecek = self.nerdenBasla()
        site_url = f"http://www.incisozluk.com.tr/u/{self.nick}{silinecek}"

        r = rq.get(site_url,headers=headers)
        soup = bs(r.content,"lxml")
        ara = soup.find("ul",attrs={"class":"profil-baslik-list wbox"}).find_all("li")
        
        ara_set = list()
        if adet < 100:
            coun = adet + 1
        else:
            coun = 101

        for ekle in ara[1:coun]:
            ara_set.append(ekle.small.text[1:])

        return list(set(ara_set))


    def sil(self,eid):
        sil_url = f"{inci}entry_sil&entry_id="
        sil_url_tam = f"{sil_url}{eid}&token={self.token}"
        deneme = 0
        while deneme < 4:
            r = rq.get(sil_url_tam,headers=headers)
            deneme += 1
            sleep(1)
            if r.json()["error"] == False:
                break
