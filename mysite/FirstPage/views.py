from django.shortcuts import render
from .src import mysql as db
from .src import wordCloud as wc
from . import forms;
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import LSTM, Dense
from keras.preprocessing import sequence
from keras import backend as K
import gc
from .src import dataProgresses as dp

# Create your views here.

def index(request):
    contexts = db.select_coments_dict();
    return render(request,'index_user.html', {'contexts' : contexts})

def control(request):
    contexts = bullying_comment_dict()
    return render(request,'index_control.html', {'contexts' : contexts})

# 악성 댓글 신고, 의심, 악성댓글인 글을 딕셔너리로 생성
def bullying_comment_dict():
    contexts_temp = db.select_report_all()
    bullyings = db.select_bullying_all()
    contexts = []
    data = wc.create_wordCloud() # 워드 클라우드
    idx = 0;

    for i in range(0,len(data),2):
        if idx < 10:
            dic = {'Index':data[i][0] ,'ID':data[i][1], 'COMENTS':data[i+1][0], 'CATEGORY' : 2, 'ETC':data[i+1][1]}
            idx += 1
            contexts.append(dic)
        else:
            break

    for row in contexts_temp :
        dic = {'Index':row[0] ,'ID':row[1],'COMENTS':row[2], 'CATEGORY' : 0 , 'ETC':0}
        contexts.append(dic)
    for row in bullyings :
        dic = {'Index':row[0] ,'ID':row[1],'COMENTS':row[2], 'CATEGORY' : 1, 'ETC':0}
        contexts.append(dic)

    return contexts

# 신고하기
def report(request):
    if request.method == 'POST':
        form = forms.reportForm(request.POST) #넘겨 받는다
        print(form);
        if form.is_valid(): # 데이터가 있는지 확인
            reportid = form.data['reportid']
            isbullying = 0;
            print("신고 인덱스 :" , reportid)
            # db.insert_data_boder(tempId['NAME'],getDate(),getTime(),subject,content,email);
            db.fix_report_coments(reportid, isbullying)

            return render(request, 'report.html')

        else:
            print("report form.is_valid() 에러")
    else:
        print("report request.method 에러")

# 신고된 목록중 악성댓글 선정
def report_o(request):
    if request.method == 'POST':
        form = forms.reportFormO(request.POST) #넘겨 받는다
        print(form);
        if form.is_valid(): # 데이터가 있는지 확인
            reportid = form.data['reportid1']
            isbullying = 2;
            print("신고 인덱스 :" , reportid)

            db.fix_report_coments(reportid, isbullying)

            return render(request, 'report_o.html')


        else:
            print("report_o form.is_valid() 에러")
    else:
        print("report_o request.method 에러")

# 악성댓글로 분류된 댓글 중 악성댓글이 아닌 댓글 선정
def no_bullying(request):
    if request.method == 'POST':
        form = forms.nobullyingForm(request.POST) #넘겨 받는다
        print(form);
        if form.is_valid(): # 데이터가 있는지 확인
            bullying_id = form.data['bullying_id']
            isbullying = -1;
            print("악플 해제 인덱스 :" , bullying_id)
            db.fix_report_coments(bullying_id, isbullying)

            return render(request, 'no_bullying.html')
        else:
            print("no_bullying form.is_valid() 에러")
    else:
        print("no_bullying request.method 에러")


# 댓글 입력
def Write(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST) #넘겨 받는다
        print(form);
        if form.is_valid(): # 데이터가 있는지 확인
            id = form.data['id']
            comment = form.data['comment']
            print("댓글 :" , id, comment)
            isbullying = dp.check_bullying_comment(comment)
            print("view : ", isbullying)
            db.insert_coments(id, comment, isbullying)


            if isbullying == 1:
                return render(request, 'warning.html')
            elif isbullying == 2:
                return render(request, 'defence.html')
            else :
                return render(request, 'write.html')

        else:
            print("Write form.is_valid() 에러")
    else:
        print("Write request.method 에러")


def start_learning(request):
    return render(request, 'learning.html')

# 재 학습
def reMakeModul(request):
    data = dp.read_csv()

    korean_dict = dp.make_dict(data)  # 한글 문자 라벨링
    # print("size : " , korean_dict.__sizeof__())
    # print(korean_dict)
    new_bullying_comments = db.select_bullying_coments()
    new_nice_comments1 = db.select_report_coments()
    new_nice_comments2 = db.select_coments()
    new_nice_comments = list(new_nice_comments1) + list(new_nice_comments2)

    bullying_sentences = db.select_dataSet("bullying")
    nice_sentences = db.select_dataSet("nice")

    sentences_temp1 = dp.make_syllable(bullying_sentences, korean_dict)
    sentences_temp2 = dp.make_syllable(nice_sentences, korean_dict)
    sentences_temp3 = dp.make_syllable(new_bullying_comments, korean_dict)
    sentences_temp4 = dp.make_syllable(new_nice_comments, korean_dict)
    sentences_bullying = sentences_temp1 + sentences_temp3
    sentences_nice = sentences_temp2 + sentences_temp4
    bullying, nice = [], []
    sentences = sentences_bullying + sentences_nice

    for s in sentences_bullying:
        bullying.append(1)
    for s in sentences_nice:
        nice.append(0)

    # 단어에 대한 인덱스 정보가 있는 딕셔너리의 길이
    vocab_size = korean_dict.__sizeof__() # 한글 글자 csv 행의 수

    X_train, y_train = sentences, (bullying + nice)

    # 데이터 길이 일치 시키기
    max_words = 15
    X_train = sequence.pad_sequences(X_train, maxlen=max_words)

    print(X_train)

    embedding_size = 12
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_size, input_length=max_words))  # 임베딩

    model.add(LSTM(100))
    model.add(Dense(1, activation="sigmoid"))
    print(model.summary())

    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    # 학습 모델을 이용해 학습 진행
    num_epochs = 15

    print("\n--- Training ---")
    model.fit(X_train, y_train, epochs=num_epochs)
    model.save("bullying_classification_model.h5")
    db.done_learning_coments(new_nice_comments, new_bullying_comments)
    K.clear_session()
    del model
    gc.collect()
    # contexts = bullying_comment_dict()
    # return render(request, 'index_control.html', {'contexts': contexts})
    return render(request, 'learning_finish.html')
