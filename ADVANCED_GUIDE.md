# 🎨 고급 기능 가이드

## 🆕 새로운 Pro 기능

업로드하신 eBay와 명상 앱 예시처럼 전문적인 마케팅 이미지를 만들 수 있습니다!

### ✨ 주요 기능
- 📝 **텍스트 오버레이**: 제목, 부제목 추가
- 📱 **멀티 레이아웃**: 3개 스크린샷 동시 배치 (eBay 스타일)
- 🎨 **전문 폰트**: SF Pro, Helvetica, Roboto 등
- 🌈 **커스텀 색상**: 그라디언트, 텍스트 색상 자유롭게
- 🔄 **3D 효과**: 원근감 있는 배치

## 🚀 빠른 시작

### 방법 1: Pro GUI (추천!)

\`\`\`bash
python gui_pro.py
\`\`\`

화면에서:
1. 이미지 선택
2. 레이아웃 선택 (단일 or 3개)
3. 제목/부제목 입력
4. 폰트/색상 선택
5. 생성!

### 방법 2: CLI (고급 사용자)

\`\`\`bash
# eBay 스타일
python generator_advanced.py screen1.png screen2.png screen3.png \\
  -o ebay_style.png --layout triple \\
  --title "Treat yourself" \\
  --subtitle "You've got our Money Back Guarantee."

# 명상 앱 스타일
python generator_advanced.py meditation.png -o output.png \\
  --title "Love and Accept Yourself" \\
  --subtitle "Meditation helps millions" \\
  --gradient-colors "60,60,180" "100,80,200"
\`\`\`

## 📱 레이아웃 옵션

### Single Layout (단일)
- 1개 스크린샷
- 크게 보여주기
- 특정 기능 강조

\`\`\`bash
python generator_advanced.py screenshot.png -o output.png \\
  --layout single --title "Save time"
\`\`\`

### Triple Layout (3개)
- 3개 스크린샷 동시에
- 원근감 효과 (좌우 이미지 약간 회전)
- 앱의 다양한 기능 표시

\`\`\`bash
python generator_advanced.py img1.png img2.png img3.png \\
  -o output.png --layout triple
\`\`\`

## 🎨 텍스트 스타일링

### 폰트 선택
\`\`\`bash
--font sf_pro        # Apple San Francisco (iOS)
--font helvetica     # Helvetica Neue (클래식)
--font roboto        # Google Roboto (Android)
--font montserrat    # Montserrat (우아함)
--font opensans      # Open Sans (가독성)
\`\`\`

### 텍스트 크기
\`\`\`bash
--title-size 60      # 작게
--title-size 90      # 기본 (권장)
--title-size 120     # 크게
\`\`\`

### 텍스트 위치
\`\`\`bash
--text-position top      # 상단 (기본)
--text-position bottom   # 하단
--text-position center   # 중앙
\`\`\`

### 텍스트 색상
\`\`\`bash
--title-color "60,120,255"    # 파란색
--title-color "255,255,255"   # 흰색
--title-color "255,215,0"     # 골드
\`\`\`

## 🌈 배경 커스터마이징

### 그라디언트 (추천!)
\`\`\`bash
# 파란색-보라색
--gradient-colors "74,144,226" "155,89,182"

# 녹색 계열
--gradient-colors "50,180,74" "50,215,75"

# 주황색 계열
--gradient-colors "255,149,0" "255,179,64"
\`\`\`

### 단색 배경
\`\`\`bash
--background solid --gradient-colors "255,255,255" "255,255,255"
\`\`\`

## 💡 실전 예제

### 예제 1: eBay 스타일
\`\`\`bash
python generator_advanced.py s1.png s2.png s3.png \\
  -o ebay.png --layout triple \\
  --title "Treat yourself" \\
  --subtitle "You've got our Money Back Guarantee." \\
  --gradient-colors "230,230,245" "255,255,255" \\
  --font helvetica --title-size 100
\`\`\`

### 예제 2: 쇼핑 앱 (Free shipping)
\`\`\`bash
python generator_advanced.py shopping.png -o output.png \\
  --title "Free shipping*" \\
  --subtitle "1-4 day shipping on millions of items" \\
  --font roboto --text-position top
\`\`\`

### 예제 3: 명상/웰니스 앱
\`\`\`bash
python generator_advanced.py meditation.png -o output.png \\
  --title "Love and Accept Yourself" \\
  --subtitle "Meditation helps millions to relax" \\
  --gradient-colors "60,60,180" "100,80,200" \\
  --font sf_pro --title-color "255,255,255"
\`\`\`

## 🎯 Pro Tips

### 텍스트 작성
✅ 좋은 예:
- "Save time" (짧고 명확)
- "Free shipping*" (혜택 강조)
- "Treat yourself" (감성적)

❌ 피할 것:
- 너무 긴 문장 (3줄 이상)
- 복잡한 설명
- 너무 작은 글씨

### 색상 선택
- **밝은 배경** → 어두운 텍스트 (대비 ⬆️)
- **어두운 배경** → 밝은 텍스트
- **브랜드 색상** 활용하세요!

### 레이아웃 선택
- **1개 기능** 집중 → Single
- **여러 기능** 표시 → Triple
- **스토리텔링** → Triple (순서대로)

## 📊 대량 처리

같은 텍스트로 여러 이미지 처리:

\`\`\`bash
for img in screenshots/*.png; do
    python generator_advanced.py "$img" \\
        -o "output/$(basename $img)" \\
        --title "Your App" \\
        --subtitle "Download now" \\
        --font sf_pro
done
\`\`\`

## 🎓 추가 자료

### 전체 옵션 보기
\`\`\`bash
python generator_advanced.py --help
\`\`\`

### 색상 코드 찾기
- [Color Picker](https://www.google.com/search?q=color+picker)
- RGB 형식: R,G,B (예: 255,0,0 = 빨간색)

### 폰트 다운로드
시스템에 없는 폰트는:
1. Google Fonts에서 다운로드
2. 시스템 폰트 폴더에 설치
3. 프로그램 재시작

## ❓ FAQ

**Q: 텍스트가 잘려요**
A: `--title-size`를 줄이거나 텍스트를 짧게 하세요

**Q: 폰트가 안 바뀌어요**
A: 시스템에 해당 폰트 설치 필요. 없으면 기본 폰트 사용

**Q: 이미지가 흐려요**
A: 원본 스크린샷 해상도 확인 (iPhone 14 Pro: 1179x2556)

**Q: 3개 레이아웃인데 이미지가 1개만 있어요**
A: 자동으로 복사해서 3개로 만듭니다 (또는 더 업로드하세요)

## 🚀 다음 단계

1. **gui_pro.py**로 시각적으로 실험하기
2. 성공한 설정을 CLI로 자동화
3. App Store에 업로드!

즐거운 마케팅 이미지 제작 되세요! 🎉
