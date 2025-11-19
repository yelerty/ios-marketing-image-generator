#!/usr/bin/env python3
"""
Advanced iOS Marketing Image Generator
프로 레벨의 앱 스토어 마케팅 이미지 생성 with 텍스트 오버레이
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import sys

class AdvancedMarketingGenerator:
    # 타겟 해상도
    TARGET_WIDTH = 1290
    TARGET_HEIGHT = 2796
    
    # 레이아웃 타입
    LAYOUT_SINGLE = 'single'           # 1개 스크린샷
    LAYOUT_DOUBLE = 'double'           # 2개 스크린샷
    LAYOUT_TRIPLE = 'triple'           # 3개 스크린샷 (eBay 스타일)
    LAYOUT_PERSPECTIVE = 'perspective' # 원근감 있는 배치
    
    # 텍스트 위치
    TEXT_TOP = 'top'
    TEXT_BOTTOM = 'bottom'
    TEXT_CENTER = 'center'
    
    def __init__(self):
        self.fonts_cache = {}
        self.setup_fonts()
    
    def setup_fonts(self):
        """시스템 폰트 경로 설정"""
        self.font_paths = {
            'sf_pro': [
                '/System/Library/Fonts/SF-Pro-Display-Bold.otf',
                '/System/Library/Fonts/SF-Pro.ttf',
                'SF-Pro-Display-Bold.otf',
            ],
            'helvetica': [
                '/System/Library/Fonts/Helvetica.ttc',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
                'Helvetica.ttc',
            ],
            'roboto': [
                '/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf',
                'Roboto-Bold.ttf',
            ],
            'montserrat': [
                '/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf',
                'Montserrat-Bold.ttf',
            ],
            'opensans': [
                '/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf',
                'OpenSans-Bold.ttf',
            ],
        }
    
    def get_font(self, font_name='helvetica', size=60, bold=True):
        """폰트 로드 (캐싱 사용)"""
        cache_key = f"{font_name}_{size}_{bold}"
        
        if cache_key in self.fonts_cache:
            return self.fonts_cache[cache_key]
        
        font_paths = self.font_paths.get(font_name.lower(), self.font_paths['helvetica'])
        
        # 폰트 파일 찾기
        for path in font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, size)
                    self.fonts_cache[cache_key] = font
                    return font
                except:
                    continue
        
        # 기본 폰트 사용
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
            self.fonts_cache[cache_key] = font
            return font
        except:
            font = ImageFont.load_default()
            self.fonts_cache[cache_key] = font
            return font
    
    def create_gradient_background(self, width, height, colors=None, direction='vertical'):
        """그라디언트 배경 생성"""
        if colors is None:
            colors = [(74, 144, 226), (155, 89, 182)]  # 기본 파란색-보라색
        
        base = Image.new('RGB', (width, height), colors[0])
        top = Image.new('RGB', (width, height), colors[1])
        mask = Image.new('L', (width, height))
        
        mask_data = []
        if direction == 'vertical':
            for y in range(height):
                mask_data.extend([int(255 * (y / height))] * width)
        else:  # horizontal
            for y in range(height):
                for x in range(width):
                    mask_data.append(int(255 * (x / width)))
        
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base
    
    def add_phone_frame(self, screenshot, frame_color=(20, 20, 20), 
                        corner_radius=60, shadow_strength=40):
        """iPhone 스타일 프레임 추가"""
        # 스크린샷 크기 + 프레임 여백
        frame_padding = 10
        shadow_offset = shadow_strength
        
        # 전체 이미지 크기 (그림자 포함)
        total_width = screenshot.width + frame_padding * 2 + shadow_offset * 2
        total_height = screenshot.height + frame_padding * 2 + shadow_offset * 2
        
        # 투명 배경 생성
        result = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
        
        # 그림자 생성
        shadow = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # 그림자 그리기
        shadow_draw.rounded_rectangle(
            [shadow_offset, shadow_offset,
             screenshot.width + frame_padding * 2 + shadow_offset,
             screenshot.height + frame_padding * 2 + shadow_offset],
            radius=corner_radius,
            fill=(0, 0, 0, 80)
        )
        
        # 그림자 블러 효과
        shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_strength // 2))
        result.paste(shadow, (0, 0), shadow)
        
        # 프레임 생성
        frame = Image.new('RGBA', 
                         (screenshot.width + frame_padding * 2,
                          screenshot.height + frame_padding * 2),
                         (*frame_color, 255))
        
        # 스크린샷을 RGBA로 변환
        if screenshot.mode != 'RGBA':
            screenshot = screenshot.convert('RGBA')
        
        # 스크린샷을 프레임에 붙이기
        frame.paste(screenshot, (frame_padding, frame_padding), screenshot)
        
        # 둥근 모서리 적용
        mask = Image.new('L', frame.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, frame.width, frame.height],
                                    radius=corner_radius, fill=255)
        
        # 프레임에 마스크 적용
        frame.putalpha(mask)
        
        # 최종 합성
        result.paste(frame, (shadow_offset // 2, shadow_offset // 2), frame)
        
        return result
    
    def add_perspective_effect(self, img, angle=15, scale=0.95):
        """3D 원근감 효과 추가"""
        width, height = img.size
        
        # 약간 회전
        rotated = img.rotate(angle, expand=True, resample=Image.BICUBIC)
        
        # 크기 조정
        new_width = int(rotated.width * scale)
        new_height = int(rotated.height * scale)
        scaled = rotated.resize((new_width, new_height), Image.LANCZOS)
        
        return scaled
    
    def create_single_layout(self, screenshot, background, text_config=None):
        """단일 스크린샷 레이아웃"""
        # 스크린샷 크기 조정
        target_width = int(self.TARGET_WIDTH * 0.75)
        aspect_ratio = screenshot.height / screenshot.width
        target_height = int(target_width * aspect_ratio)
        
        if target_height > self.TARGET_HEIGHT * 0.7:
            target_height = int(self.TARGET_HEIGHT * 0.7)
            target_width = int(target_height / aspect_ratio)
        
        screenshot_resized = screenshot.resize((target_width, target_height), Image.LANCZOS)
        
        # 프레임 추가
        screenshot_framed = self.add_phone_frame(screenshot_resized)
        
        # 중앙 배치
        x = (self.TARGET_WIDTH - screenshot_framed.width) // 2
        y = (self.TARGET_HEIGHT - screenshot_framed.height) // 2
        
        # 텍스트 위치에 따라 Y 조정
        if text_config and text_config.get('position') == self.TEXT_TOP:
            y = int(self.TARGET_HEIGHT * 0.35)
        elif text_config and text_config.get('position') == self.TEXT_BOTTOM:
            y = int(self.TARGET_HEIGHT * 0.15)
        
        background.paste(screenshot_framed, (x, y), screenshot_framed)
        
        return background
    
    def create_triple_layout(self, screenshots, background, text_config=None):
        """3개 스크린샷 레이아웃 (eBay 스타일)"""
        if len(screenshots) < 3:
            screenshots = screenshots * 3  # 부족하면 반복
        
        screenshots = screenshots[:3]
        
        # 각 스크린샷 크기 조정
        target_width = int(self.TARGET_WIDTH * 0.28)
        
        phone_images = []
        for i, screenshot in enumerate(screenshots):
            aspect_ratio = screenshot.height / screenshot.width
            target_height = int(target_width * aspect_ratio)
            
            if target_height > self.TARGET_HEIGHT * 0.65:
                target_height = int(self.TARGET_HEIGHT * 0.65)
                target_width_adjusted = int(target_height / aspect_ratio)
            else:
                target_width_adjusted = target_width
            
            resized = screenshot.resize((target_width_adjusted, target_height), Image.LANCZOS)
            
            # 원근감 효과 (중앙은 각도 작게)
            if i == 0:
                angle = -12
            elif i == 1:
                angle = 0
            else:
                angle = 12
            
            if angle != 0:
                resized = self.add_perspective_effect(resized, angle, scale=0.95)
            
            framed = self.add_phone_frame(resized)
            phone_images.append(framed)
        
        # 배치
        spacing = 20
        total_width = sum(img.width for img in phone_images) + spacing * 2
        start_x = (self.TARGET_WIDTH - total_width) // 2
        
        # 텍스트 공간 고려
        if text_config and text_config.get('position') == self.TEXT_TOP:
            start_y = int(self.TARGET_HEIGHT * 0.4)
        elif text_config and text_config.get('position') == self.TEXT_BOTTOM:
            start_y = int(self.TARGET_HEIGHT * 0.2)
        else:
            start_y = int(self.TARGET_HEIGHT * 0.3)
        
        x_offset = start_x
        for i, img in enumerate(phone_images):
            # Y 위치 약간씩 다르게 (더 자연스러운 느낌)
            y_offset = start_y + (i % 2) * 30
            background.paste(img, (x_offset, y_offset), img)
            x_offset += img.width + spacing
        
        return background
    
    def add_text_overlay(self, image, text_config):
        """텍스트 오버레이 추가"""
        draw = ImageDraw.Draw(image)
        
        title = text_config.get('title', '')
        subtitle = text_config.get('subtitle', '')
        position = text_config.get('position', self.TEXT_TOP)
        font_name = text_config.get('font', 'helvetica')
        title_color = text_config.get('title_color', (60, 120, 255))
        subtitle_color = text_config.get('subtitle_color', (80, 80, 80))
        
        # 폰트 크기
        title_size = text_config.get('title_size', 90)
        subtitle_size = text_config.get('subtitle_size', 45)
        
        # 폰트 로드
        title_font = self.get_font(font_name, title_size, bold=True)
        subtitle_font = self.get_font(font_name, subtitle_size, bold=False)
        
        # 텍스트 위치 계산
        margin = 60
        
        if position == self.TEXT_TOP:
            y_start = margin + 50
        elif position == self.TEXT_BOTTOM:
            y_start = self.TARGET_HEIGHT - 400
        else:
            y_start = self.TARGET_HEIGHT // 2 - 100
        
        # 제목 그리기 (멀티라인 지원)
        if title:
            lines = self._wrap_text(title, title_font, self.TARGET_WIDTH - margin * 2)
            y_offset = y_start
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=title_font)
                text_width = bbox[2] - bbox[0]
                x = (self.TARGET_WIDTH - text_width) // 2
                
                # 텍스트 그림자
                shadow_offset = 4
                draw.text((x + shadow_offset, y_offset + shadow_offset), 
                         line, font=title_font, fill=(0, 0, 0, 100))
                
                # 실제 텍스트
                draw.text((x, y_offset), line, font=title_font, fill=title_color)
                
                y_offset += bbox[3] - bbox[1] + 20
        
        # 부제목 그리기
        if subtitle:
            lines = self._wrap_text(subtitle, subtitle_font, self.TARGET_WIDTH - margin * 2)
            y_offset = y_start + 140 if title else y_start
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=subtitle_font)
                text_width = bbox[2] - bbox[0]
                x = (self.TARGET_WIDTH - text_width) // 2
                
                draw.text((x, y_offset), line, font=subtitle_font, fill=subtitle_color)
                y_offset += bbox[3] - bbox[1] + 15
        
        return image
    
    def _wrap_text(self, text, font, max_width):
        """텍스트를 여러 줄로 나누기"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def generate_marketing_image(self, screenshot_paths, output_path, 
                                 layout='single', background_style='gradient',
                                 background_colors=None, text_config=None):
        """마케팅 이미지 생성 메인 함수"""
        try:
            # 스크린샷 로드
            screenshots = []
            if isinstance(screenshot_paths, str):
                screenshot_paths = [screenshot_paths]
            
            for path in screenshot_paths:
                img = Image.open(path)
                screenshots.append(img)
            
            print(f"✅ {len(screenshots)}개 스크린샷 로드 완료")
            
            # 배경 생성
            if background_style == 'gradient':
                if background_colors is None:
                    background_colors = [(74, 144, 226), (155, 89, 182)]
                background = self.create_gradient_background(
                    self.TARGET_WIDTH, self.TARGET_HEIGHT, 
                    background_colors, 'vertical'
                )
            elif background_style == 'solid':
                color = background_colors[0] if background_colors else (255, 255, 255)
                background = Image.new('RGB', (self.TARGET_WIDTH, self.TARGET_HEIGHT), color)
            else:
                background = Image.new('RGB', (self.TARGET_WIDTH, self.TARGET_HEIGHT), (255, 255, 255))
            
            # 레이아웃 적용
            if layout == self.LAYOUT_TRIPLE and len(screenshots) >= 1:
                result = self.create_triple_layout(screenshots, background, text_config)
            else:
                result = self.create_single_layout(screenshots[0], background, text_config)
            
            # 텍스트 오버레이
            if text_config and (text_config.get('title') or text_config.get('subtitle')):
                result = self.add_text_overlay(result, text_config)
            
            # 저장
            result = result.convert('RGB')
            result.save(output_path, 'PNG', quality=95)
            
            print(f"✅ 마케팅 이미지 생성 완료: {output_path}")
            print(f"   크기: {result.size}")
            
            return True
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='고급 iOS 마케팅 이미지 생성기',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
예제:
  # 단일 스크린샷 + 텍스트
  python generator_advanced.py screenshot.png -o output.png \\
    --title "Save time" --subtitle "Zip through checkout."
  
  # 3개 스크린샷 레이아웃
  python generator_advanced.py screen1.png screen2.png screen3.png \\
    -o output.png --layout triple --title "Treat yourself"
  
  # 커스텀 그라디언트
  python generator_advanced.py screenshot.png -o output.png \\
    --gradient-colors "74,144,226" "155,89,182" --title "Free shipping"
        '''
    )
    
    parser.add_argument('screenshots', nargs='+', help='스크린샷 파일(들)')
    parser.add_argument('-o', '--output', required=True, help='출력 파일')
    parser.add_argument('--layout', choices=['single', 'triple'], 
                       default='single', help='레이아웃 타입')
    parser.add_argument('--background', choices=['gradient', 'solid', 'white'],
                       default='gradient', help='배경 스타일')
    parser.add_argument('--gradient-colors', nargs=2, metavar=('COLOR1', 'COLOR2'),
                       help='그라디언트 색상 (R,G,B 형식)')
    parser.add_argument('--title', help='제목 텍스트')
    parser.add_argument('--subtitle', help='부제목 텍스트')
    parser.add_argument('--text-position', choices=['top', 'bottom', 'center'],
                       default='top', help='텍스트 위치')
    parser.add_argument('--font', choices=['sf_pro', 'helvetica', 'roboto', 
                                          'montserrat', 'opensans'],
                       default='helvetica', help='폰트')
    parser.add_argument('--title-color', help='제목 색상 (R,G,B)')
    parser.add_argument('--title-size', type=int, default=90, help='제목 크기')
    
    args = parser.parse_args()
    
    # 색상 파싱
    gradient_colors = None
    if args.gradient_colors:
        gradient_colors = [
            tuple(map(int, color.split(','))) 
            for color in args.gradient_colors
        ]
    
    title_color = (60, 120, 255)
    if args.title_color:
        title_color = tuple(map(int, args.title_color.split(',')))
    
    # 텍스트 설정
    text_config = None
    if args.title or args.subtitle:
        text_config = {
            'title': args.title,
            'subtitle': args.subtitle,
            'position': args.text_position,
            'font': args.font,
            'title_color': title_color,
            'title_size': args.title_size,
        }
    
    # 생성
    generator = AdvancedMarketingGenerator()
    generator.generate_marketing_image(
        args.screenshots,
        args.output,
        layout=args.layout,
        background_style=args.background,
        background_colors=gradient_colors,
        text_config=text_config
    )


if __name__ == '__main__':
    main()
