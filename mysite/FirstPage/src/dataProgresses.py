import re
import csv
from keras.models import load_model
from keras import backend as K
from keras.preprocessing import sequence
import gc

# 한글 데이터 로드
def read_csv():
    f = open('koreanLabling.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    data = []
    for line in rdr:
        data.append(line)
        # print(line)

    f.close()

    return data

# 한글 데이터 딕셔너리로 변환
def make_dict(data):
    new_dict = dict()
    word, index = [],[]
    for d in data:
        word.append(d[0])
        index.append(d[1])

    new_dict = dict(zip(word, index))

    # print(new_dict)

    return new_dict


#텍스트 정제(전처리)
def cleanText(readData):
    #텍스트에 포함되어 있는 특수 문자 제거
    # text = re.sub('[-=+;,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》ㅋㅎ0123456789zxcvbnmasdfghjkklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP]', '', readData)
    text = re.sub( '[^ㄱ-ㅣ가-힣]+','', readData) # 한글 빼고 다지우기

    return text

# 음절 단위로 끊기
def make_syllable(sentences, korean_dict):
    sentence = []
    for sent in sentences:
        sent = str(sent)
        sent = sent.replace("\n", "")
        sent = sent.replace(" ", "")
        sent = sent.replace("ㅋ", "")
        sent = cleanText(sent)
        sent2 = []
        for s in sent:
            # print(type(s), s, korean_dict.get(s))
            sent2.append(int(korean_dict.get(s)))
        sentence.append(sent2)

    return sentence


# 악성 댓글인지 판단
def check_bullying_comment(comment):
    global model
    isbullying = -1 # -1: 악성댓글아님, 0 : 신고중, 1 : 악성댓글의심, 2 : 악성댓글
    data = read_csv()
    korean_dict = make_dict(data) # 한글 문자 라벨링
    X_test = []
    temp = []
    comment = cleanText(comment)
    comment = make_syllable(comment, korean_dict)
    print(comment)
    for c in comment:
        if len(c) < 1:
             continue
        temp.append(c[0])

    X_test.append(temp)
    print(X_test)

    max_words = 15
    X_test = sequence.pad_sequences(X_test, maxlen=max_words)

    model = load_model("bullying_classification_model.h5")
    print("Loaded model")

    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    y_pred = model.predict(X_test)
    print("예측 : ", y_pred)
    if y_pred < 0.5 :
        isbullying = -1;
    elif y_pred < 0.90 and y_pred >= 0.5 :
        isbullying = 1;
    elif y_pred >= 0.90 :
        isbullying = 2;

    K.clear_session()
    del model
    gc.collect()

    return isbullying



