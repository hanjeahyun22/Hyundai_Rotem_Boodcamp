# with 구문 사용 - 내부적으로 close
try:
    # 파일 저장
    with open('ftext3.txt', mode='w', encoding='utf-8') as fobj1:               # 파일작업 시, close() 대신에, with 구문으로 대체
        fobj1.write('파이썬에서 문서 저장\n')
        fobj1.write('with 구분은\n')
        fobj1.write('명시적으로 close() 할 필요 없다.\n')
    print('저장 완료')

    # 파일 저장
    with open('ftext3.txt', mode='r', encoding='utf-8') as fobj2:
        print(fobj2.read())

except Exception as e:
    print('err : ', e)


# --------------------------------------------------------------------------------------------------------------------------------
# pickling : 원하는 일반(복합) 객체만 저장

print('\n\n피클링(일반 객체 및 복합 객체 파일 처리)')
import pickle

try:
    dictData = {'tom':'111-1111', '길동':'222-2222'}
    listData = ['마우스', '키보드']
    tupleData = (dictData, listData)

    with open('hello.dat', mode='wb') as fobj3:
        pickle.dump(tupleData, fobj3)                                           # pickle.dump(저장 대상, 파일 객체)
        pickle.dump(listData, fobj3)                                            # list type 객체만 저장
    print('특정 객체를 파일로 저장')

    print('피클 객체 읽기')
    with open('hello.dat', mode='rb') as fobj4:
        a, b = pickle.load(fobj4)                                               # pickle.load(파일 객체명)
        print('a : ', a)                                                        # a : {'tom': '111-1111', '길동': '222-2222'}
        print('b : ', b)                                                        # b :  ['마우스', '키보드']
        c = pickle.load(fobj4)                                              
        print('c : ', c)                                                        # c :  ['마우스', '키보드']
    
except Exception as e:
    print('err : ', e)