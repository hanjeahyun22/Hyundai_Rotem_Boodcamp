# pack1/mymod1

tot = 100       # 전역변수

def listhap(*ar):
    print(ar)
    if __name__ == '__main__':
        print('나는 메인 모듈')             # ex15module에서 실행해보면, 실행 X -->> mymod1 모듈은 메인 모듈 X -->> ex15module.py가 메인 모듈 O


def kbs():
    print('대한민국 대표 방송')

def mbc():
    print('문화방송')