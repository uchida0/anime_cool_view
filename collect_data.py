import os
import datetime
import json
import pandas as pd
from bs4 import BeautifulSoup
import requests

def makeDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def makefile(path, text):
    with open(path, mode="w") as f:
        f.write(text)


def collect_data(link, cool):
    #title_list:list
    #seisaku_list:list


    html = requests.get(link)

    soup = BeautifulSoup(html.text, "html.parser")

    #<div class="animeSeasonBox">
    #<p class="seasonAnimeTtl"><a href="">animetitle</a></p>
    #<dl class="seasonAnimeDetail"><dt>制作会社</dt><dd>シンエイ動画、TIA</dd>
    
    #<div class="seasonBoxImg"><a href=""><img src=""></a>

    #div class="animeSeasonBox"が1単位

    #animeSeasonBoxes = soup.findAll("div", {"class": "animeSeasonBox"})
    #print(len(animeSeasonBoxes))

    
    #アニメタイトルを取得
    animeTitle = soup.findAll("p", {"class": "seasonAnimeTtl"})
    title_list = []

    print("アニメタイトルリスト取得開始!!")

    for at in animeTitle:
        #print(at.string)
        #アニメタイトルのデータを格納
        title_list.append(at.string)
    
    print("アニメタイトルリスト取得完了.")

    #詳細情報（制作会社など）を取得
    animeDetail = soup.findAll("dl", {"class": "seasonAnimeDetail"})
    
    seisaku_list = []

    print("制作会社リスト取得開始...")

    for ad in animeDetail:
        #print(len(ad))
        if len(ad) > 1:
            #print()
            seisaku_text = ad.find("dt", text="制作会社")
            if seisaku_text:
                seisaku_text = seisaku_text.string
            #print(seisaku_text)

            #制作会社の情報があれば取得する
            if seisaku_text == "制作会社":
                seisaku = ad.find("dt", text="制作会社").next_element.next_element.next_element
                seisaku = seisaku.string
                #print(seisaku)
            else:
                seisaku = "データなし"
            
            #制作会社のデータを格納
            seisaku_list.append(seisaku)
        
        else:
            #print()
            seisaku = "データなし"

            #制作会社のデータを格納
            seisaku_list.append(seisaku)
    
    print("制作会社リスト取得完了!!")

    #画像を保存
    makeDir("data/" + cool)
    makeDir("result/" + cool)

    anime_Img = soup.findAll("div", {"class": "seasonBoxImg"})
    img_list = []

    print("アニメ画像取得開始...")
    
    for ai in anime_Img:
        img_link = ai.img.get("src")
        #print(img_link)
        img_list.append(img_link)
    
    img_count = 0
    for target in img_list:
        res = requests.get(target)
        #title_list[img_count]だとタイトルにスラッシュが入っているファイル名が生成できないから番号で管理
        with open("data/" + cool + "/" + str(img_count+1) + ".jpg", "wb") as f:
            f.write(res.content)
        img_count += 1
    

    print("アニメ画像取得完了!!")
    #title_listとseisaku_listの情報を一時テキストとして保存

    print("リスト作成中...")

    with open("data/" + cool + "/" + "anime_list.txt", "w", encoding="utf-8") as f:
        for i in range(len(title_list)):
            f.write("==="+str(i+1)+"===\n")
            f.write(title_list[i]+"\n")
            f.write(seisaku_list[i]+"\n")
    
    print("All completed!!")


if __name__=="__main__":
    spring_2021 = "https://anime.eiga.com/program/"
    winter_2021 = "https://anime.eiga.com/program/season/2021-winter/"
    autumn_2020 = "https://anime.eiga.com/program/season/2020-autumn/"
    summer_2020 = "https://anime.eiga.com/program/season/2020-summer/"
    spring_2020 = "https://anime.eiga.com/program/season/2020-spring/"
    winter_2020 = "https://anime.eiga.com/program/season/2020-winter/"
    autumn_2019 = "https://anime.eiga.com/program/season/2019-autumn/"
    summer_2019 = "https://anime.eiga.com/program/season/2019-summer/"
    spring_2019 = "https://anime.eiga.com/program/season/2019-spring/"
    winter_2019 = "https://anime.eiga.com/program/season/2019-winter/"

    
    autumn_2013 = "https://anime.eiga.com/program/season/2013-autumn/"
    summer_2013 = "https://anime.eiga.com/program/season/2013-summer/"
    spring_2013 = "https://anime.eiga.com/program/season/2013-spring/"
    winter_2013 = "https://anime.eiga.com/program/season/2013-winter/"




    
    #link = spring_2021
    #cool = "spring_2021"

    #link = winter_2021
    #cool = "winter_2021"

    #link = autumn_2013
    #cool = "autumn_2013"

    #link = summer_2013
    #cool = "summer_2013"

    #link = spring_2013
    #cool = "spring_2013"

    link = winter_2013
    cool = "winter_2013"

    collect_data(link, cool)