import math
import numpy as np
import gymnasium as gym         # 실습환경 제공(현재상태 제공 -> 행동 선택 -> 환경이 행동을 반영) -> 새로운 상태, 보상, 종료조건 반환
from gymnasium import spaces
import matplotlib.pyplot as plt

# 환경/장애물, 라이다
WOLRD_W, WORLD_H,  = 20.0, 15.0
OBSTACLES = [(6.0, 4.0, 0.5), (8.0, 10.0, 1.5), (15.0, 5.0, 1.5)]           # [(x좌표, y좌표, 반지름)]
