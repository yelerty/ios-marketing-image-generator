# 🚀 빠른 시작 가이드

## 1단계: 설치

```bash
# 저장소 클론
git clone git@github.com:yelerty/ios-marketing-image-generator.git
cd ios-marketing-image-generator

# 의존성 설치
pip install -r requirements.txt
```

## 2단계: 스크린샷 준비

iPhone 14 Pro에서 촬영한 스크린샷을 준비하세요.
- 해상도: 1179 x 2556 픽셀
- 형식: PNG, JPG, JPEG

## 3단계: 사용 방법 선택

### 🖥️ 방법 A: GUI 사용 (가장 쉬움)

```bash
python gui_enhanced.py
```

1. 이미지를 드래그 앤 드롭하거나 버튼으로 선택
2. 배경 스타일 선택 (흰색, 검정, 그라디언트 등)
3. "마케팅 이미지 생성" 버튼 클릭
4. 저장 위치 선택
5. 완료! 🎉

### 🌐 방법 B: 웹 브라우저 사용

```bash
python web_app.py
```

브라우저에서 `http://localhost:5000` 접속 후:
1. 이미지 드래그 앤 드롭
2. 옵션 선택
3. "마케팅 이미지 생성" 클릭
4. 개별 다운로드

### ⚡ 방법 C: 명령줄 (고급 사용자)

```bash
# 단일 파일
python generator.py screenshot.png -o marketing_image.png

# 폴더 전체
python generator.py screenshots/ -o output/ -b gradient_blue

# 고속 배치 처리 (병렬)
python batch_processor.py screenshots/ -o output/ -w 4
```

## 예제 명령어

### 흰색 배경으로 생성
```bash
python generator.py my_screenshot.png -o output.png -b white
```

### 그라디언트 배경 + 프레임 없이
```bash
python generator.py my_screenshot.png -o output.png -b gradient_blue --no-frame
```

### 여러 이미지 일괄 처리 (빠름)
```bash
python batch_processor.py screenshots_folder/ -o output/ -w 8
```

## 결과물

생성된 이미지:
- 크기: 1290 x 2796 픽셀 (App Store 마케팅 이미지 규격)
- 형식: PNG (고품질)
- 파일명: `marketing_원본이름.png`

## 다음 단계

- 다양한 배경 스타일 시도해보기
- 여러 스크린샷으로 일관된 스타일의 마케팅 이미지 세트 만들기
- App Store Connect에 업로드하기

## 도움이 필요하신가요?

- 전체 문서: `README.md` 참조
- 문제 발생 시: GitHub Issues에 문의
- 추가 기능: 각 Python 스크립트에 `--help` 옵션 사용

예:
```bash
python generator.py --help
python batch_processor.py --help
```

---

**팁**: 첫 사용 시에는 GUI (`gui_enhanced.py`)를 추천합니다!
