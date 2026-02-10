# openCV(Computer Vision)
# pip install opencv-python 필요

import cv2
print(cv2.__version__)

img1 = cv2.imread('ani.jpeg')
print(type(img1))
cv2.imshow('image test', img1)
cv2.waitKey()
cv2.destroyAllWindows()
# print('end')


# 다른 이름으로 저장
cv2.imwrite('ani2.jpg', img1)
cv2.imwrite('ani3.jpg', img1, [cv2.IMWRITE_JPEG_QUALITY, 10])


# 이미지 크기 조정
img2 = cv2.resize(img1, (300, 100), interpolation=cv2.INTER_AREA)
cv2.imwrite('ani3.jpg', img2)


# 이미지 밝기 조정
# 이미지 상하좌우 회전
# 이미지 특정 영역 자르기
# ...