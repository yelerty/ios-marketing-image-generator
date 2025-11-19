# iOS Marketing Image Generator 🎨📱

iPhone 14 Pro 스크린샷을 **eBay, 명상 앱 같은** 전문적인 App Store 마케팅 이미지(1290x2796)로 자동 변환하는 강력한 도구입니다.

## 🆕 Pro 기능 (NEW!)

- 📝 **텍스트 오버레이**: "Save time", "Free shipping" 같은 마케팅 문구 추가
- 📱 **멀티 레이아웃**: 3개 스크린샷을 eBay 스타일로 배치 (원근감 효과 포함)
- 🎨 **전문 폰트**: SF Pro, Helvetica, Roboto, Montserrat, Open Sans
- 🌈 **완전한 커스터마이징**: 그라디언트, 텍스트 색상, 크기 자유롭게 조정
- 👁️ **실시간 미리보기**: Pro GUI에서 결과 즉시 확인

## ✨ 기본 기능

- 📱 **완벽한 크기 조정**: iPhone 14 Pro 스크린샷을 1290x2796 픽셀 마케팅 이미지로 자동 변환
- 🎨 **다양한 배경 스타일**: 흰색, 검정, 그라디언트, App Store 회색, 커스텀 색상
- ✨ **자동 효과**: 그림자/프레임 효과 자동 추가
- 🚀 **일괄 처리**: 여러 이미지 동시 처리 (병렬 처리 지원)
- 🎯 **비율 유지**: 원본 비율을 유지하며 최적 크기로 자동 조정
- 🖱️ **드래그 앤 드롭**: 편리한 GUI 인터페이스
- 🌐 **웹 인터페이스**: 브라우저에서 바로 사용 가능
- ⚡ **고속 처리**: 멀티스레딩으로 빠른 처리 속도

## 🆕 NEW! 고급 기능 (Advanced)

- **📱 다중 디바이스 레이아웃**: 1개, 2개, 3개 스크린샷 동시 표시
- **📝 텍스트 오버레이**: 제목, 부제목, 설명 텍스트 추가
- **🎨 전문 폰트**: SF Pro, Helvetica, Roboto 등 자동 감지
- **✨ 3D 효과**: 기울임, 그림자, 둥근 모서리
- **⚡ 빠른 템플릿**: eBay, 명상 앱 스타일 등 프리셋

## 설치

```bash
# 저장소 클론
git clone git@github.com:yelerty/ios-marketing-image-generator.git
cd ios-marketing-image-generator

# 의존성 설치
pip install -r requirements.txt
```

## 사용법

### 🆕 방법 A: 고급 생성기 (Advanced) - 추천!

#### 단일 디바이스 + 텍스트
```bash
python generator_advanced.py screenshot.png -o output.png \
  --title "Treat yourself" \
  --subtitle "You've got our Money Back Guarantee" \
  --background white
```

#### 2개 디바이스 레이아웃
```bash
python generator_advanced.py screen1.png screen2.png -o output.png \
  --layout double \
  --title "Save time" \
  --subtitle "Zip through checkout" \
  --background gradient_blue
```

#### 3개 디바이스 + 풀 텍스트
```bash
python generator_advanced.py s1.png s2.png s3.png -o output.png \
  --layout triple \
  --title "Love and Accept Yourself" \
  --subtitle "Meditation helps millions" \
  --description "of people to relax, stay calm and balanced" \
  --background gradient_purple
```

#### Pro GUI (고급 GUI)
```bash
python gui_pro.py
```

**기능:**
- 📱 1-3개 스크린샷 선택
- 📝 제목, 부제목, 설명 입력
- 🎨 텍스트 색상 커스터마이징
- ⚡ eBay, 명상 앱 스타일 프리셋
- 👁️ 실시간 미리보기

### 방법 B: 기본 생성기 (Basic)

#### 명령줄 인터페이스 (CLI)

단일 이미지 변환

```bash
# 기본 사용 (흰색 배경)
python generator.py screenshot.png -o marketing_image.png

# 그라디언트 배경 사용
python generator.py screenshot.png -o output.png -b gradient_blue

# 프레임 없이 생성
python generator.py screenshot.png -o output.png --no-frame
```

여러 이미지 일괄 처리

```bash
# screenshots 폴더의 모든 이미지를 output 폴더로 변환
python generator.py screenshots/ -o output/

# 검정 배경으로 일괄 변환
python generator.py screenshots/ -o output/ -b black
```

### 방법 2: 기본 GUI

```bash
# 간단한 GUI 실행
python gui.py
```

### 방법 3: 고급 GUI (드래그 앤 드롭 지원)

```bash
# 향상된 GUI 실행 (드래그 앤 드롭, 미리보기 기능)
python gui_enhanced.py
```

**기능:**
- 🖱️ 드래그 앤 드롭으로 파일 추가
- 👁️ 실시간 미리보기
- 🎨 커스텀 배경 색상 선택
- 📊 진행 상황 표시

### 방법 4: 웹 인터페이스

```bash
# 웹 서버 시작
python web_app.py
```

그 다음 브라우저에서 `http://localhost:5000` 접속

**기능:**
- 🌐 브라우저에서 바로 사용
- 📤 드래그 앤 드롭 업로드
- 💾 개별 다운로드
- 📱 모바일 지원

### 방법 5: 고속 배치 처리

```bash
# 병렬 처리로 빠른 변환 (4개 워커)
python batch_processor.py screenshots/ -o output/ -w 4

# 그라디언트 배경으로 8개 워커 사용
python batch_processor.py screenshots/ -o output/ -b gradient_blue -w 8
```

**특징:**
- ⚡ 멀티스레딩으로 고속 처리
- 📊 진행률 표시 (tqdm)
- 📈 성공/실패 통계

## 명령어 옵션

- `input`: 입력 스크린샷 파일 또는 디렉토리 (필수)
- `-o, --output`: 출력 파일 또는 디렉토리 (기본값: output)
- `-b, --background`: 배경 스타일
  - `white`: 흰색 배경 (기본값)
  - `black`: 검정색 배경
  - `gradient_blue`: 파란색 그라디언트
  - `app_store_gray`: App Store 스타일 회색
- `--no-frame`: 그림자/프레임 효과 제거

## 📋 예제

### CLI로 빠르게 시작하기

```bash
# 1. 샘플 이미지 준비
mkdir -p samples/screenshots samples/output

# 2. iPhone 14 Pro에서 촬영한 스크린샷을 samples/screenshots/에 복사

# 3. 마케팅 이미지 생성
python generator.py samples/screenshots/ -o samples/output/ -b gradient_blue
```

### GUI로 간편하게 사용하기

```bash
# 고급 GUI 실행
python gui_enhanced.py

# 1. 이미지를 드래그 앤 드롭하거나 버튼으로 선택
# 2. 배경 스타일과 효과 선택
# 3. '마케팅 이미지 생성' 버튼 클릭
# 4. 저장 위치 선택
```

### 웹 인터페이스 사용하기

```bash
# 웹 서버 시작
python web_app.py

# 브라우저에서 http://localhost:5000 접속
# 드래그 앤 드롭으로 이미지 업로드 후 생성!
```

### 대량 이미지 고속 처리

```bash
# 100개의 이미지를 8개 워커로 병렬 처리
python batch_processor.py large_folder/ -o output/ -w 8 -b white

# 진행률이 실시간으로 표시됩니다:
# 이미지 처리 중: 100%|██████████| 100/100 [00:45<00:00, 2.21개/s]
```

## 지원 형식

- 입력: PNG, JPG, JPEG
- 출력: PNG (고품질, 1290x2796)

## iPhone 14 Pro 스펙

- 스크린샷 해상도: 1179 x 2556 픽셀
- 마케팅 이미지 타겟: 1290 x 2796 픽셀

## 📂 프로젝트 구조

```
ios-marketing-image-generator/
├── generator.py              # 기본 이미지 생성 엔진
├── generator_advanced.py     # 🆕 고급 생성기 (다중 레이아웃, 텍스트)
├── gui.py                    # 기본 GUI
├── gui_enhanced.py           # 고급 GUI (드래그앤드롭, 미리보기)
├── gui_pro.py               # 🆕 프로 GUI (텍스트 오버레이)
├── web_app.py               # Flask 웹 인터페이스
├── batch_processor.py       # 고속 배치 처리
├── create_samples.py        # 샘플 이미지 생성
├── requirements.txt         # 의존성 패키지
├── README.md               # 이 문서
├── QUICKSTART.md           # 빠른 시작 가이드
├── ADVANCED_GUIDE.md       # 🆕 고급 기능 가이드
└── samples/
    ├── screenshots/        # 입력 스크린샷
    └── output/             # 생성된 마케팅 이미지
```

## 💡 사용 팁

### 최상의 결과를 위한 권장사항

1. **입력 이미지**: iPhone 14 Pro 스크린샷 (1179 x 2556) 사용 권장
2. **배경 선택**:
   - 앱이 밝은 테마면 → `white` 또는 `app_store_gray`
   - 앱이 어두운 테마면 → `black` 또는 `gradient_blue`
3. **프레임 효과**: 대부분의 경우 켜두는 것을 권장 (더 전문적인 느낌)
4. **대량 처리**: 10개 이상의 이미지는 `batch_processor.py` 사용 권장

### 성능 최적화

```bash
# CPU 코어 수에 맞게 워커 수 조정
# 예: 8코어 CPU인 경우
python batch_processor.py screenshots/ -o output/ -w 8

# 메모리가 부족한 경우 워커 수 줄이기
python batch_processor.py screenshots/ -o output/ -w 2
```

## 🎨 배경 스타일 가이드

- **white**: 깔끔하고 모던한 느낌, 대부분의 앱에 적합
- **black**: 프리미엄 느낌, 게임이나 엔터테인먼트 앱에 적합
- **gradient_blue**: 역동적이고 현대적, IT/테크 앱에 적합
- **app_store_gray**: App Store 스타일, 공식적인 느낌
- **custom** (GUI만 해당): 브랜드 색상에 맞춤

## 🛠️ 문제 해결

### 드래그 앤 드롭이 작동하지 않는 경우

```bash
pip install tkinterdnd2
```

### 웹 서버가 시작되지 않는 경우

```bash
pip install Flask
```

### 이미지 처리가 느린 경우

```bash
# batch_processor 사용 시 워커 수 증가
python batch_processor.py input/ -o output/ -w 8
```
