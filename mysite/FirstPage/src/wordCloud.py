from konlpy.tag import Twitter
from collections import Counter
from .mysql import select_bullyindTable
from PIL import Image
import numpy as np
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import ImageColorGenerator


def get_tags(comment, ntags=300):
    spliter = Twitter()
    return_list = []  # 명사 빈도수 저장할 변수

    # nouns 함수를 통해서 text에서 명사만 분리/추출
    nouns = spliter.nouns(comment)

    count = Counter(nouns)
    # Counter객체를 생성하고 참조변수 nouns할당

    for n, c in count.most_common(ntags):
        temp = (n, c)
        return_list.append(temp)
    # most_common 메소드는 정수를 입력받아 객체 안의 명사중 빈도수
    # 큰 명사부터 순서대로 입력받은 정수 갯수만큼 저장되어있는 객체 반환
    # 명사와 사용된 갯수를 return_list에 저장합니다.
    return return_list

def make_wordCloud_png(data):
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    image_path = os.getcwd() + "/gun3.jpg"
    # print(image_path)
    gun_jpg = np.array(Image.open(image_path))
    image_gun = ImageColorGenerator(gun_jpg)

    tmp_data = dict(data)

    cloud = WordCloud(font_path="c:/Windows/Fonts/malgun.ttf",
                      relative_scaling=0.2, mask=gun_jpg,
                      background_color='white', random_state=42,
                      min_font_size=1, max_font_size=60).generate_from_frequencies(tmp_data)
    plt.figure(figsize=(12,12))
    plt.imshow(cloud.recolor(color_func=image_gun), interpolation="bilinear")
    plt.axis("off")
    fig = plt.gcf()

    fig.savefig('E:/code/Django/mysite/FirstPage/static/images/이미지.png')



def create_wordCloud():
    texts = select_bullyindTable()
    comment = ""
    for text in texts:
        text = text[0].replace("ㅋ","")
        text = text.replace("ㅎ","")
        comment = comment + " " +text

    data = get_tags(comment)  # get_tags 함수 실행
    make_wordCloud_png(data)
    return data