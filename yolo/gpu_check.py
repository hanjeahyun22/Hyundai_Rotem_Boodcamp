# gpu_check.py
import os

# TensorFlow import 전에 필요한 환경변수 설정
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"

import tensorflow as tf
import time

print("TensorFlow:", tf.__version__)
print("Built with CUDA:", tf.test.is_built_with_cuda())

# 1. Physical GPU 먼저 확인
gpus = tf.config.list_physical_devices("GPU")
print("Physical GPUs:", gpus)

# 2. memory growth는 logical device 확인 전에 설정해야 함
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("[INFO] GPU memory growth enabled")
    except RuntimeError as e:
        print("[WARN] GPU memory growth setting failed:", e)

# 3. 그 다음 logical GPU 확인
print("Logical GPUs:", tf.config.list_logical_devices("GPU"))

# 4. 실제 GPU 연산 테스트
if gpus:
    print("\n[GPU TEST] Matrix multiplication on GPU")

    with tf.device("/GPU:0"):
        a = tf.random.normal([3000, 3000])
        b = tf.random.normal([3000, 3000])

        start = time.time()
        c = tf.matmul(a, b)
        _ = c.numpy()  # 실제 연산 완료 대기
        end = time.time()

    print("Result shape:", c.shape)
    print("Elapsed:", round(end - start, 4), "sec")
else:
    print("\n[INFO] GPU not detected. Running on CPU.")