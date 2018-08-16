from wordcloud import WordCloud,color_from_image
import pymysql
import os
import jieba


#生成txt文件，写入同good_id的商品的所有评论，一个good_id对应一个txt
def create_txt():

    #创建一个文件夹wordcould存放词频图
    if not os.path.isdir('wordcloudfile'):
        os.mkdir('wordcloudfile')

    #数据库连接
    db = pymysql.Connect(host='localhost',port=3306,user='root',password='ROOKIE',db='tb_comment',charset='utf8mb4')
    cursor = db.cursor()

    #查询所有商品的id
    sql = "select good_id from goods;"
    cursor.execute(sql)
    goods_id = cursor.fetchall()

    #遍历id并写入生成txt文件
    for good_id in goods_id:
        id = good_id[0]
        sql = 'select content from comments where good_id=%d'%id    #查询该商品的所有评论
        cursor.execute(sql)
        with open('./wordcloudfile/%d.txt' % id, 'w+', encoding='utf-8') as f:  #编码使用utf-8，否则会报编码错误
            for content in cursor.fetchall():
                f.write(content[0]+'\n')

#生成云图，一个txt对应一张云图
def create_pic():
    txt_list =[x for x in  os.listdir('./wordcloudfile') if '.txt' in x]    #遍历
    for txt in txt_list:
        with open('./wordcloudfile/%s'%txt,'r',encoding='utf-8') as f:
            text = f.read()
        word_count = ','.join(jieba.cut(text))          #jieba的精准模式
        font = 'SIMYOU.ttf'
        wc = WordCloud(background_color='white',font_path=font,scale=1.5).generate(word_count)
        wc.to_file('./wordcloudfile/%s'%txt.replace('.txt','.jpg'))         #

#create_txt()
#create_pic()




