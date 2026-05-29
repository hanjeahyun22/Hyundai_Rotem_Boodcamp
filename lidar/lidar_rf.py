import math
import numpy as np
import gymnasium as gym         # 실습환경 제공(현재상태 제공 -> 행동 선택 -> 환경이 행동을 반영) -> 새로운 상태, 보상, 종료조건 반환
from gymnasium import spaces
import matplotlib.pyplot as plt

# 환경/장애물, 라이다
WORLD_W, WORLD_H,  = 20.0, 15.0
OBSTACLES = [(6.0, 4.0, 0.5), (8.0, 10.0, 1.5), (15.0, 5.0, 1.5)]           # [(x좌표, y좌표, 반지름)]
NUM_RAYS = 20
FOV = np.deg2rad(150)       # 라이다의 시야각
MAX_RANGE = 8.0             # 라이다 레이의 최대 감지 거리
STEP_MARCH = 0.05           # 레이의 전진 단위 거리
START_X = 2.0               # 에이전트(차량) 초기 x 좌표
START_Y = 2.0               # 에이전트(차량) 초기 y 좌표

# 현재 차량이 시뮬레이터 공간 경계 내에 있는지 여부 판단
def inside_worldFunc(x, y):
    return (0.0 <= x <= WORLD_W) and (0.0 <= y <= WORLD_H)

# 라이다 ray 끝 점이 장애물과 충돌했는지 판단   --> 장애물과 차량의 거리가 장애물의 반지름 내부에 들어오면 True 반환
def hit_circleFunc(px, py, cx, cy, r):
    return (px - cx)**2 + (py - cy)**2 <= r**2

# 에이전트(차량)의 (x, y, theta)에서 시야각(FOV)으로 지정한 ray의 개수(NUM_RAYS)만큼 ray를 쐈을 때, 
# 각 ray가 처음 부딪히는 지점까지의 거리, ray 균등 각도 구하기
# 에이전트(차량)의 현재 위치와 방향에서 라이다 ray를 쏘는 함수
def cast_lidar(x, y, theta, num_rays = NUM_RAYS, fov = FOV, max_range=MAX_RANGE, step=STEP_MARCH):
    
    # theta:
    # 현재 차량이 바라보는 방향 각도
    # 예) 0이면 오른쪽, pi/2이면 위쪽 방향
    
    # fov:
    # 라이다가 볼 수 있는 전체 시야각
    # 여기서는 150도 범위를 본다는 의미
    
    # theta - fov / 2:
    # 차량 정면(theta)을 기준으로 왼쪽 끝 각도부터 시작
    start = theta - fov / 2
    
    # num_rays:
    # 라이다 ray 개수
    # 여기서는 20개의 ray를 시야각 안에 균등하게 배치
    
    # angles:
    # 각 ray가 발사될 방향 각도들
    # start부터 시작해서 fov 범위 안에 균등하게 나눔
    angles = start + np.arange(num_rays) * (fov / max(num_rays - 1, 1))
    print("angles : ", angles)

    # 초기 거리 배열 초기화 = 최대거리
    dists = np.full(num_rays, max_range, dtype=np.float32)
    print("dists : ", dists)

    # 라이다 센서에서 발생하는 ray에 대해서 index, ray의 angle 반환
    for i, ang in enumerate(angles):
        dist = 0.0                      # ray의 전진 값 --> STEP_MARCH = 0.05(레이의 전진 단위 거리) 만큼 전진
        hit = False                     # 에이전트(차량)가 환경 영역 밖 또는 장애물 충돌 여부   (기본값으로 아직 부딪히지 않은 상태)

        # ray를 STEP_MARCH 만큼 최대거리(max_range)까지 전진
        while dist < max_range:
            px = x + math.cos(ang) * dist       # ray 끝 점 x 좌표
            py = y + math.sin(ang) * dist       # ray 끝 점 y 좌표

            # 판단1) 차량이 world 공간 내에 있는지 판단     -->>    WORLD의 끝 경계에 부딪히면 시퀀스 종료
            if not inside_worldFunc(px, py):
                hit = True
                break

            # 판단2) 차량이 장애물에 부딪혔는지 판단
            for (cx, cy, r) in OBSTACLES:           # cx : 장애물의 x좌표, cy : 장애물의 y좌표, r : 장애물의 반지름 
                if hit_circleFunc(px, py, cx, cy, r):
                    hit = True
                    break
            
            if hit == True:
                break
        
            dist += step
        
        # 충돌 거리 기록(ray의 충돌이 없으면 ray의 최대 거리 기록, 충돌하면 hit=True, break로 종료된 시점의 dist 기록)
        dists[i] = min(dist, max_range)
    
    return dists, angles

# Gymnasium의 기존 환경을 상속받은 클래스 작성
class SimpleLidarEnv(gym.Env):
    def __init__(self, render_mode="human"):
        super().__init__()
        self.render_mode = render_mode

        # 강화 학습 시, action_space, observation_space 는 반드시 설정
        self. action_space = spaces.Discrete(3)     # Discreate(3) - 가능한 행동 3가지 생성 (0:좌회전, 1:직진, 2:우회전)
        self.observation_space = spaces.Box(low=0.0, high=MAX_RANGE, shape=(NUM_RAYS, ), dtype=np.float32)      # 관측값은 길이 20(NUM_RAYS)짜리 배열 (0.0 <= 관측값 <= MAX_RANGE)

        self.v = 0.25                                               # 전진 속도
        self.steer_delta = np.deg2rad(8)                            # 회전각도 - 8도 설정
        self.goal = np.array([18.0, 12.0], dtype=np.float32)        # 에이턴트(차량)의 최종 목표 좌표 (18, 12)
        self.goal_radius = 0.6                                      # 목표 판정 반경
        self.max_steps = 400                                        # 하나의 에피소드에서 허용되는 최대 행동 횟수(좌회전/직진/우회전)

        self.fig, self.ax = None, None                              # rendering용 객체
        self._state = None                                          # [x, y, theta]
        self._prev_goal_dist = None                                 # 이전 목표 거리
        self._steps = 0                                             # step 카운트 변수
    
    # Gym.Env가 제공하는 내부 메소드 (_get_obs, _get_info, _collision) --> 현재 환경 상태를 강화학습이 이해할 수 있는 numpy 수치 배열로 만들어 반환
    def _get_obs(self):
        x, y, theta = self._state
        obs, _ = cast_lidar(x=x, y=y, theta=theta)          # angle은 받지 않고, 거리만 받음
        return obs.astype(np.float32)
    
    def _get_info(self):
        x, y, _ = self._state
        d = np.linalg.norm(np.array([x, y]) - self.goal)    # 목표까지의 거리
        return {"goal_dist":float(d), "steps":self._steps}

    def _collision(self):
        x, y, _ = self._state
        
        # 만약 WOLRD의 경계 밖이라면, 충돌로 간주
        if not inside_worldFunc(x, y):
            return True
        
        # 장애물에 충돌 판단 (기존 장애물 반지름에 0.25를 더해서, 실제로 충돌하기 전에 충돌했을 경우의 회피 기동 하도록 충동 방지)
        for (cx, cy, r) in OBSTACLES:
            if hit_circleFunc(x, y, cx, cy, r + 0.25):
                return True
        
        return False

    # 초기화
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._state = np.array([START_X, START_Y, np.deg2rad(30.0)], dtype=np.float32)
        self._steps = 0
        self._prev_goal_dist = np.linalg.norm(self._state[:2] - self.goal)                  # 초기 목표 거리
        
        obs = self._get_obs()
        info = self._get_info()

        return obs, info

    def step(self, action):
        self._steps += 1
        x, y, theta = self._state

        # 행동 적용
        if action == 0:
            theta += self.steer_delta           # 좌회전
        elif action == 2:
            theta -= self.steer_delta           # 우회전
        
        x += math.cos(theta) * self.v   # 차량이 바라보는 방향(theta)으로 self.v만큼 이동할 때의 x방향 이동량
        y += math.sin(theta) * self.v   # y방향 이동량
        self._state = np.array([x, y, theta], dtype=np.float32)     # 새 위치, 새 방향으로 설정

        goal_dist = np.linalg.norm(self._state[:2] - self.goal)
        process = self._prev_goal_dist - goal_dist                  # 접근 변화량
        self._prev_goal_dist = goal_dist

        # process가 클수록 보상이 커지지만, 매 step마다 작은 시간 패널티(-0.01)를 줘서 빠르게 목표에 도달하도록 유도 --> 무한루프(게으른 작업) 방지
        reward = 1.0 * process - 0.01   # 에이전트(차량)가 괜히 오래 돌아다니지 말고 빠르게 목표로 가도록 만드는 보상식
        terminated, truncated = False, False

        # 전체 시퀀스 종료 조건
        # 1) 목표 도달
        if goal_dist < self.goal_radius:
            reward += 1.0                       # 보상 최대값 부여
            terminated = True                   # 전체 시퀀스 종료
        
        # 2) 충돌한 경우
        if self._collision():
            reward -= 1.0                       # 패널티 최대값 부여
            terminated = True                   # 전체 시퀀스 종료
        
        # 3) 스텝 초과(에이전트(차량)가 WORLD 밖으로 나간 경우)
        if self._steps >= self.max_steps:
            terminated = True
        
        # 관측 정보 반환
        obs = self._get_obs()                   # 라이다 
        info = self._get_info()

        return obs, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            print("현재 상태 : ", self._state)

        ax = self.ax
        ax.clear()
        ax.set_xlim(0, WORLD_W)
        ax.set_ylim(0, WORLD_H)
        ax.set_aspect("equal", adjustable = "box")                              # 가로 세로 비율은 1:1 --> 왜곡 방지
        ax.set_title("Simple Lidar Env")
        ax.plot([0, WORLD_H, WORLD_W, 0, 0], [0, 0, WORLD_H, WORLD_W, 0], lw=2) # 경계 사각형
        
        # 장애물
        for (cx, cy, r) in OBSTACLES:
            circle = plt.Circle((cx, cy), r, edgecolor="tab:red", facecolor="none", lw=2)
            ax.add_patch(circle)
        
        # 목표점
        goal = plt.Circle(tuple(self.goal), self.goal_radius, edgecolor="tab:blue", facecolor="none", lw=2)         # tuple을 쓰는 이유 : 목표 위치를 matplotlib이 이해하기 쉬운 (x, y) 좌표 형태로 바꾸는 것
        ax.add_patch(goal)

        # 에이전트(차량)
        x, y, theta = self._state
        L = 0.6     # 삼각형 높이
        


if __name__ == "__main__":
    env = SimpleLidarEnv()
    obs, info = env.reset()

    total_reward = 0.0

    for t in range(500):
        
        action = env.action_space.sample()                                  # 환경에서 가능한 행동범위 중 무작위로 하나 선택 (좌회전/직진/우회전)
        
        # obs:새로운 상태, reward:보상, terminated:종료여부, truncated:시간제한종료여부, info:추가정보
        obs, reward, terminated, truncated, info = env.step(action)         # 환경 단계 실행(환경이 다음 <새로운>상태와 보상등의 )

        total_reward += reward
        env.render()

    # 에피소드 종료 조건
    if terminated or truncated:
        print(f"Episode and at step={t}, total reward={total_reward:.3f}, info:{info}")
        obs, info = env.reset()
        total_reward = 0.0

    env.close()