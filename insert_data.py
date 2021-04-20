import pymysql

#MySQLにデータを入れて画像生成に用いる


def init_cool_table(cool):
    connection = pymysql.connect(
        host="localhost",
        user="sora",
        password="monster",
        db="good_anime_bu"
    )

    #DBname ="good_anime_bu"

    with connection.cursor() as cursor:
        init_query = (
            "CREATE TABLE IF NOT EXISTS " + cool +
            " (id int, title text, seisaku text);"
        ) 
        cursor.execute(init_query)
    
    connection.commit()
    connection.close()



def insert_anime_list(cool, anime_list):
    
    #MySQL接続
    connection = pymysql.connect(
        host="localhost",
        user="sora",
        password="monster",
        db="good_anime_bu"
    )


    with connection.cursor() as cursor:
        #pymysqlのプレースホルダは%sで良く、数値か文字列か適切に展開してくれるらしい
        insert_query = (
            "INSERT INTO " + cool + " (id, title, seisaku) VALUES (%s,%s,%s);"
        )

        cursor.executemany(insert_query, anime_list)

    
    connection.commit()
    connection.close()


#data/　にあるanime_list.txtからリストを作成
def make_anime_list(cool):
    data = "data/" + cool + "/anime_list.txt"
    #title_list = []
    #seisaku_list = []
    anime_list = []
    anime_number = 1
    an_text = "==="+str(anime_number)+"===\n"
    
    with open(data, "r", encoding="utf-8") as f:
        for line in f:
            #print(line)
            if line == an_text:
                title = f.__next__()
                seisaku = f.__next__()
                title = title.rstrip("\n")
                seisaku = seisaku.rstrip("\n")
                #print(title)
                #print(seisaku)


                #title_list.append(title)
                #seisaku_list.append(seisaku)
                anime_list.append([anime_number, title, seisaku])

                anime_number += 1
                an_text = "==="+str(anime_number)+"===\n"

    #return title_list, seisaku_list
    return anime_list


if __name__ == "__main__":
    #cool = "spring_2021"
    #cool = "winter_2021"
    #cool = "autumn_2013"
    #cool = "summer_2013"
    #cool = "spring_2013"
    cool = "winter_2013"
    #title_list, seisaku_list = make_anime_list(cool)
    anime_list = make_anime_list(cool)
    init_cool_table(cool)
    #print(anime_list)
    insert_anime_list(cool, anime_list)