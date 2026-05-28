import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. 환경 / 에이전트 설정
# ============================================================

# 시뮬레이션 월드 크기
# LiDAR 센서가 탐지하는 2D 공간의 가로, 세로 크기
WORLD_W, WORLD_H = 20.0, 15.0

# 벽 두께
# 현재 코드에서는 직접 사용하지 않고,
# 월드 밖으로 나가면 벽과 충돌한 것으로 처리한다.
WALL_THICK = 0.5

# 원형 장애물 정보
# 형식: (중심 x좌표, 중심 y좌표, 반지름)
OBSTACLES = [
    (6.0, 4.0, 1.0),            # (6,4) 좌표에 위치한 반지름 1짜리 장애물
    (12.0, 10.0, 1.5),          # (12,10) 좌표에 위치한 반지름 1짜리 장애물
    (15.0, 5.0, 1.0),           # (15,5) 좌표에 위치한 반지름 1짜리 장애물
]

# 에이전트 초기 상태
# x, y: 에이전트 위치
# theta: 에이전트가 바라보는 방향, radian 단위
agent = {
    "x": 3.0,
    "y": 3.0,
    "theta": np.deg2rad(30)   # 30도를 radian으로 변환
}

# LiDAR 파라미터
NUM_RAYS = 32                 # LiDAR 광선 개수
FOV = np.deg2rad(180)         # 시야각 180도
MAX_RANGE = 10.0              # 최대 탐지 거리
STEP = 0.05                   # 광선이 전진하는 간격


# ============================================================
# 2. 충돌 판정 함수
# ============================================================

def inside_world(x, y):
    """
    현재 좌표가 월드 내부에 있는지 확인하는 함수.

    x가 0 이상 WORLD_W 이하이고,
    y가 0 이상 WORLD_H 이하이면 True를 반환한다.
    그 외에는 월드 밖이므로 False를 반환한다.
    """
    return (0.0 <= x <= WORLD_W) and (0.0 <= y <= WORLD_H)


def hit_circle(px, py, cx, cy, r):
    """
    점(px, py)이 원형 장애물 내부에 있는지 확인하는 함수.

    px, py: 검사할 점의 좌표
    cx, cy: 원형 장애물 중심 좌표
    r: 원형 장애물 반지름

    원의 방정식:
    (px - cx)^2 + (py - cy)^2 <= r^2 이면 충돌
    """
    return (px - cx) ** 2 + (py - cy) ** 2 <= r ** 2


# ============================================================
# 3. LiDAR 스캔 함수
# ============================================================

def cast_lidar(
    x,
    y,
    theta,
    num_rays=NUM_RAYS,
    fov=FOV,
    max_range=MAX_RANGE,
    step=STEP
):
    """
    에이전트 위치에서 여러 방향으로 LiDAR ray를 발사하고,
    각 ray가 벽 또는 장애물에 처음 닿는 거리값을 계산한다.

    입력:
        x, y      : 에이전트 위치
        theta     : 에이전트가 바라보는 방향
        num_rays  : LiDAR ray 개수
        fov       : LiDAR 시야각
        max_range : 최대 탐지 거리
        step      : ray 전진 간격

    출력:
        dists  : 각 ray별 충돌 거리 배열
        angles : 각 ray별 절대 각도 배열
    """

    # 첫 번째 ray의 각도
    # 에이전트 방향 theta를 기준으로 시야각의 왼쪽 끝부터 시작
    start = theta - fov / 2

    # LiDAR ray 각도 배열 생성
    # start부터 start + fov까지 num_rays개로 균등 분할
    angles = start + np.arange(num_rays) * (fov / max(num_rays - 1, 1))

    # 모든 ray의 거리값을 max_range로 초기화
    # 충돌하지 않으면 최대거리로 남는다.
    dists = np.full(num_rays, max_range, dtype=float)

    # 각 ray에 대해 충돌 검사
    for i, ang in enumerate(angles):
        dist = 0.0
        hit = False

        # ray가 최대 거리까지 전진하면서 충돌 여부 확인
        while dist < max_range:
            # 현재 ray 방향으로 dist만큼 이동한 점의 좌표
            px = x + np.cos(ang) * dist
            py = y + np.sin(ang) * dist

            # 월드 밖으로 나가면 벽에 충돌한 것으로 처리
            if not inside_world(px, py):
                hit = True
                break

            # 원형 장애물과 충돌했는지 검사
            for cx, cy, r in OBSTACLES:
                if hit_circle(px, py, cx, cy, r):
                    hit = True
                    break

            # 충돌했으면 해당 ray의 탐색 종료
            if hit:
                break

            # 충돌하지 않았으면 step만큼 더 전진
            dist += step

        # 충돌 거리 저장
        # 충돌하지 않았으면 max_range 저장
        dists[i] = min(dist, max_range)

    return dists, angles


# ============================================================
# 4. 시각화 함수
# ============================================================

def plot_world(agent, rays_endpoints=None):
    """
    2D 월드, 장애물, 에이전트, LiDAR ray를 시각화하는 함수.
    """

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    # 월드 범위 설정
    ax.set_xlim(0, WORLD_W)
    ax.set_ylim(0, WORLD_H)

    # x, y 축 비율을 동일하게 설정
    ax.set_aspect("equal", adjustable="box")

    ax.set_title("Simple 2D LiDAR")

    # 월드 경계선 그리기
    ax.plot(
        [0, WORLD_W, WORLD_W, 0, 0],
        [0, 0, WORLD_H, WORLD_H, 0],
        lw=2
    )

    # 원형 장애물 그리기
    for cx, cy, r in OBSTACLES:
        circle = plt.Circle(
            (cx, cy),
            r,
            edgecolor="tab:red",
            facecolor="none",
            lw=2
        )
        ax.add_patch(circle)

    # 에이전트 위치 및 방향
    x = agent["x"]
    y = agent["y"]
    th = agent["theta"]

    # 에이전트 삼각형 크기
    L = 0.6

    # 에이전트를 삼각형으로 표현
    triangle = np.array([
        [x + np.cos(th) * L, y + np.sin(th) * L],
        [x + np.cos(th + 2.5) * L / 1.5, y + np.sin(th + 2.5) * L / 1.5],
        [x + np.cos(th - 2.5) * L / 1.5, y + np.sin(th - 2.5) * L / 1.5],
    ])

    ax.fill(
        triangle[:, 0],
        triangle[:, 1],
        alpha=0.8,
        color="tab:blue",
        label="agent"
    )

    # LiDAR ray 그리기
    if rays_endpoints is not None:
        for x0, y0, x1, y1 in rays_endpoints:
            ax.plot(
                [x0, x1],
                [y0, y1],
                lw=1,
                alpha=0.8
            )

    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


# ============================================================
# 5. 메인 실행부
# ============================================================

if __name__ == "__main__":

    # LiDAR 스캔 실행
    obs, angles = cast_lidar(
        agent["x"],
        agent["y"],
        agent["theta"]
    )

    # 시각화용 ray 끝점 좌표 계산
    endpoints = []

    for dist, angle in zip(obs, angles):
        x0 = agent["x"]
        y0 = agent["y"]

        x1 = x0 + np.cos(angle) * dist
        y1 = y0 + np.sin(angle) * dist

        endpoints.append((x0, y0, x1, y1))

    # LiDAR 거리 관측값 출력
    print("LiDAR observation distances:")
    print(np.round(obs, 2))

    # 월드 및 LiDAR ray 시각화
    plot_world(agent, endpoints)