"""
첨도, 왜도(편차)가 큰 데이터 -->> 로그 변환 필요 -->> 분포 개선, 범위 차이 축소 -->> 모델을 안정적으로 수행 가능
--->>> 정규성을 높일 수 있음 <<<---
y = log(x) 에서, x에 0을 넣으면 error가 발생 -->> x + offset 으로 error 방지
"""

import math
class LogTrans:
    def __init__(self, offset:float=1.0):
        self.offset = offset

    def transform(self, x_list:list[float]):                # 로그 변환
        return [math.log(x + self.offset) for x in x_list]

    def inverse_trans(self, x_list:list[float]):            # 역 변환
        return [math.exp(x_log) - self.offset for x_log in x_list]

def main():
    data = [10.0, 100.0, 1000.0, 10000.0]                   # 예로 편차가 큰 자료
    
    # 로그 변환용 객체
    log_trans = LogTrans(offset=1.0)

    # 로그 변환 및 역변환
    data_log_scaled = log_trans.transform(data)
    reversed_data = log_trans.inverse_trans(data_log_scaled)
    reversed_data_round = [round(val,1) for val in reversed_data]

    print('원본 자료 : ', data)                             # [10.0, 100.0, 1000.0, 10000.0]
    print('로그 변환 자료 : ', data_log_scaled)             # [2.3978952727983707, 4.61512051684126, 6.90875477931522, 9.210440366976517]   -->>    10~10000 원본 데이터 편차보다, 2~9 로 완화.
    print('역변환 : ', reversed_data_round)
    
if __name__ == '__main__':
    main()