from PIL import Image, ImageDraw, ImageFont
import pymysql


#1枚ずつ作成し、合成するようにする
#160*160：画像
#0-160,160-200

def make_ga_pic(cool, id, title, seisaku):

    #coolで季節によって色を変える
    #default outline_color
    out_color = (255, 255, 255)
    
    if "spring" in cool:
        #spring(pink)
        out_color = (255, 102, 204)
    elif "summer" in cool:
        #summer(yellow)
        out_color = (247, 234, 65)
    elif "autumn" in cool:
        #autumn(orange)
        out_color = (246, 102, 0)
    elif "winter" in cool:
        #winter(aqua)
        out_color = (144, 192, 240)

    #ベース
    im = Image.new("RGB", (160, 320), (90, 90, 90))
    draw = ImageDraw.Draw(im)

    draw.rectangle((0, 0, 160, 320), fill=(90, 90, 90), outline=(50, 50, 50))


    #titleスペース
    #fill=(50,50,50) gray
    draw.rectangle((0, 160, 160, 200), fill=(50,50,50), outline=(50,50,50))
    
    #seisakuスペース
    #draw.rectangle((0, 200, 160, 320), fill=(50, 50, 50), outline=(50, 50, 50))


    #テキスト
    ttfontname = "C:\\Windows\\Fonts\\meiryob.ttc"
    fontsize = 20
    #text = "アニメタイトル長いやつだよねこれ"
    title_text = title
    seisaku_text = seisaku.replace("、", "\n・")
    seisaku_text = "・"+seisaku_text
    #既定のサイズで入らなければ、2行にするので、文を半分のところで切る
    #既定サイズ：20

    title_font = ImageFont.truetype(ttfontname,18)
    tw, th = draw.textsize(title_text, font=title_font)
    #print(tw)
    tn = 0

    if tw >= 160:
        title_font = ImageFont.truetype(ttfontname, 14)
        tw, th = draw.textsize(title_text, title_font)
        while tw >= 160:
            tn = tn-1
            #t = title_text.rsplit(title_text[tn], 1)[0]
            t_length = len(title_text) + tn
            t = title_text.rsplit(title_text[t_length:], 1)[0]
            tw, th = draw.textsize(t, title_font)
            #print(t)

    if tn != 0:
        title_length = len(title_text)
        tl = title_length + tn 
        title_text = title_text[:tl] + "\n" + title_text[tl:]
        #print(title_text)
        title_font = ImageFont.truetype(ttfontname, 14)


    tw, th = draw.textsize(title_text, title_font)
    if tw >= 160:
        title_font = ImageFont.truetype(ttfontname, 10)
        tw, th = draw.textsize(title_text, title_font)
    draw.multiline_text( ( (160-tw)/2, 160+(40-th)/2 ), title_text, font=title_font, fill=(255, 255, 255) )
    #draw.multiline_text((0,160), title_text, font=title_font, fill=(255, 255, 255))

    #pillow_char_offset(draw, 0, 160, 160, 200, title_text, 30, ttfontname)
    #pillow_char_offset(draw, 0, 200, 160, 320, seisaku_text, 30, ttfontname)

    seisaku_info_font = ImageFont.truetype(ttfontname, 12)
    seisaku_font = ImageFont.truetype(ttfontname, 14)

    draw.text((0, 200), "制作会社", font=seisaku_info_font,fill=(255, 255, 255))

    s_new_list = []

    for s in seisaku_text.split("\n"):
        sw, sh = draw.textsize(s, seisaku_font)
        sn = 0
        if sw > 160:
            while sw > 160:
                sn = sn-1
                st = s.rsplit(s[sn], 1)[0]
                sw, sh = draw.textsize(st, title_font)
        
        if sn != 0:
            sl = len(s) + sn
            #s_new = s[:sl] + "\n" + s[sl:]
            #print(s)
            s_new_list.append(s[:sl])
            s_new_list.append(s[sl:])
        else:
            s_new_list.append(s)
            
    if s_new_list:
        seisaku_text = "\n".join(s_new_list)

    draw.multiline_text((0, 220), seisaku_text, font=seisaku_font, fill=(255, 255, 255))

    
    #textRGB = (0, 0, 0)

    #font = ImageFont.truetype(font=ttfontname, size=fontsize)
    #textWidth, textHeight = draw.textsize(text, font=font)
    #draw.text((80, 180), text, fill=textRGB, font=font, anchor="mm")
    

    result_dir = "result/"
    result_img_dir = result_dir + cool + "/" + str(id) + ".jpg"
    
    im.save(result_img_dir)


    #anime_img
    info_im = Image.open(result_img_dir)
    back_im = info_im.copy()

    #img_dir = "data/spring_2021/31.jpg"
    data_dir = "data/"
    img_dir = data_dir + cool + "/" + str(id) + ".jpg"
    anime_img = Image.open(img_dir)

    result_dir = "result/"
    result_img_dir = result_dir + cool + "/" + str(id) + ".jpg"

    back_im.paste(anime_img, (0, 0))
    back_im.save(result_img_dir)


def pillow_char_offset(draw, x_pos, y_pos, x_end_pos, y_end_pos, char, init_font_size, font_file_name):
    length = x_end_pos - x_pos
    height = y_end_pos - y_pos
    
    out_text_size = (length+1, height+1)
    font_size_offset = 0
    font = None

    while length < out_text_size[0] or height < out_text_size[1]:
        font = ImageFont.truetype(font_file_name, init_font_size - font_size_offset)
        #print(init_font_size - font_size_offset)
        out_text_size = draw.textsize(char, font=font)
        font_size_offset += 1
    
    draw.text((x_pos, y_pos), char, fill=(255, 255, 255), font=font)


#DBからデータを取ってきてdictで返す
def select_anime_datas(cool):
    print("DBからデータ取得中...")

    #anime_dict = [{"id": 1, "title": anime_title, "seisaku": seisaku_kaisha}]
    connection = pymysql.connect(
        host="localhost",
        user="sora",
        password="monster",
        db="good_anime_bu",
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        select_query = (
            "SELECT * FROM " + cool
        )
        cursor.execute(select_query)
    
    #connection.commit()
    #print(cursor.fetchall())
    anime_dict = cursor.fetchall()
    #print(anime_dict)
    connection.close()

    print("DBからデータ取得完了!!")

    return anime_dict


#dictを受け取ってmake_ga_picを回す
def make_pics(anime_dict, cool):

    anime_num = len(anime_dict)
    anime_num = str(anime_num)

    #dictを回して、画像生成を繰り返す
    for anime in anime_dict:
        id = anime["id"]
        title = anime["title"]
        seisaku = anime["seisaku"]

        print(str(id) + "/" + anime_num)
        
        make_ga_pic(cool=cool, id=id, title=title, seisaku=seisaku)


def all_anime_pic(cool, num):
    data = "result/" + cool + "/"
    #(160,320) * n
    #header:(160*n, 160)

    if "spring" in cool:
        #spring(pink) (251,218,222) (255,102,204), (255, 105, 180),(241,114,163)
        color = (241, 114, 163)
    elif "summer" in cool:
        #summer(yellow)
        color = (247, 234, 65)
    elif "autumn" in cool:
        #autumn(orange)
        color = (246, 102, 0)
    elif "winter" in cool:
        #winter(aqua)
        color = (144, 192, 240)

    n = 6
    #(90,90,90)
    im = Image.new("RGB", (160*n, 320*((num//n) +1)+160), color)
    draw = ImageDraw.Draw(im)
    ttfontname = "C:\\Windows\\Fonts\\meiryob.ttc"
    cool_font = ImageFont.truetype(ttfontname, 100)
    draw.text((0, 0), cool, font=cool_font, fill=(255, 255, 255))
    #draw.text((0, 200), "制作会社", font=seisaku_info_font,fill=(255, 255, 255))
    im.save(data + cool + ".jpg")

    all_img = Image.open(data + cool + ".jpg")
    back_im = all_img.copy()

    for i in range(1, num+1):
        img_dir = data + str(i)+".jpg"
        w_count = (i%n) -1
        if i%n == 0:
            w_count += n

        h_count = i//n
        if i%n == 0:
            h_count -= 1

        anime_img = Image.open(img_dir)

        back_im.paste(anime_img, (160*w_count, 320*h_count + 160))
    
    back_im.save(data + cool + ".jpg")
    

if __name__ == "__main__":
    #cool = "spring_2021"
    #cool = "winter_2021"
    #cool = "autumn_2013"
    #cool = "summer_2013"
    #cool = "spring_2013"
    cool = "winter_2013"
    #make_ga_pic(num)
    anime_dict = select_anime_datas(cool)
    all_num = len(anime_dict)
    make_pics(anime_dict, cool)

    all_anime_pic(cool, all_num)