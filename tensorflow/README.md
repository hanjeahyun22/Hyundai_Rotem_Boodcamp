# CNN Notebook Scripts - VSCode/Ubuntu 실행용

이 폴더는 Colab/Jupyter Notebook(`.ipynb`) 파일을 VSCode에서 실행하기 쉽도록 `.py`로 변환한 버전입니다.

## 권장 실행 환경

```bash
conda activate hyundai_rotem_bootcamp_finalproject
python -m pip install tensorflow tensorflow-datasets matplotlib numpy pandas scikit-learn opencv-python requests ipykernel
```

VSCode에서 `.py` 파일을 열고 우측 상단 인터프리터를 다음 환경으로 선택하세요.

```text
/home/pnuav/anaconda3/envs/hyundai_rotem_bootcamp_finalproject/bin/python
```

## 실행 예시

```bash
cd ~/HyundaiRotem_Bootcamp/python_source/tensorflow
python cnn1.py
```

## 수정 반영 사항

- Notebook 전용 `!명령어`, `%magic`은 주석 처리했습니다.
- `cnn6gender.py`의 Colab Drive 경로 `/content/drive/MyDrive/person_img/`를 `./person_img/`로 변경했습니다.
- `cnn7aug.py`는 `test_aug.jpg` 파일 존재 여부를 확인하도록 수정했습니다.
- `cnn9catdog.py`의 `google.colab.files.download()`는 주석 처리했습니다.
- `cnn9catdog.py`의 체크포인트 폴더 오타 `chackpoints`를 `chkpoints`로 수정했습니다.
- `cnn10catdog_pred.py`는 `catdog_best.keras`가 없으면 `chkpoints/catdog_best.keras`를 찾도록 수정했습니다.
- MX250/CPU 환경을 고려해 무거운 cat/dog 및 MobileNet 계열 일부 batch size를 줄였습니다.

## 파일/데이터가 추가로 필요한 스크립트

- `cnn6gender.py`: `person_img/` 폴더 필요
- `cnn7aug.py`: `test_aug.jpg` 필요
- `cnn10catdog_pred.py`: `catdog_best.keras` 또는 `chkpoints/catdog_best.keras`, 예측 이미지 필요
- `cnn9catdog.py`, `cnn14tl_catdog.py`: `tensorflow_datasets`가 인터넷에서 cats_vs_dogs 데이터를 다운로드합니다.

## 권장 실행 순서

1. `cnn1.py`
2. `cnn2functional.py`
3. `cnn3subclass.py`
4. `cnn4cifar10.py`
5. `cnn5cifar10.py`
6. `cnn8fmnist.py`
7. `cnn11.py`
8. `cnn12mobileNet.py`
9. `cnn13tl_cifar10.py`
10. `cnn14tl_catdog.py`
11. `cnn9catdog.py`
12. `cnn10catdog_pred.py`

