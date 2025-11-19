#!/usr/bin/env python3
"""
iOS Marketing Image Generator
iPhone 14 Pro 스크린샷을 1290x2796 마케팅 이미지로 변환
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

class MarketingImageGenerator:
    # iPhone 14 Pro 스크린샷 해상도
    IPHONE_14_PRO_WIDTH = 1179
    IPHONE_14_PRO_HEIGHT = 2556
    
    # 마케팅 이미지 타겟 해상도
    TARGET_WIDTH = 1290
    TARGET_HEIGHT = 2796
    
    # 배경 색상 (흰색, 검정색 등 선택 가능)
    BACKGROUND_COLORS = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'gradient_blue': None,  # 그라디언트는 별도 처리
        'app_store_gray': (242, 242, 247)
    }
    
    def __init__(self, background='white'):
        self.background_color = self.BACKGROUND_COLORS.get(background, (255, 255, 255))
    
    def create_gradient_background(self, width, height, color_start=(74, 144, 226), color_end=(155, 89, 182)):
        """그라디언트 배경 생성"""
        base = Image.new('RGB', (width, height), color_start)
        top = Image.new('RGB', (width, height), color_end)
        mask = Image.new('L', (width, height))
        mask_data = []
        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base
    
    def add_device_frame(self, screenshot):
        """디바이스 프레임 추가 (선택사항)"""
        # 간단한 그림자 효과 추가
        shadow_offset = 20
        shadow_color = (0, 0, 0, 50)
        
        # 그림자용 이미지 생성
        shadow = Image.new('RGBA', 
                          (screenshot.width + shadow_offset * 2, 
                           screenshot.height + shadow_offset * 2), 
                          (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            [shadow_offset, shadow_offset, 
             screenshot.width + shadow_offset, 
             screenshot.height + shadow_offset],
            radius=40,
            fill=shadow_color
        )
        
        # 스크린샷을 RGBA로 변환
        if screenshot.mode != 'RGBA':
            screenshot = screenshot.convert('RGBA')
        
        # 그림자에 스크린샷 합성
        shadow.paste(screenshot, (shadow_offset, shadow_offset), screenshot)
        
        return shadow
    
    def generate_marketing_image(self, screenshot_path, output_path, add_frame=True, background_style='white'):
        """마케팅 이미지 생성"""
        try:
            # 스크린샷 불러오기
            screenshot = Image.open(screenshot_path)
            print(f"원본 이미지 크기: {screenshot.size}")
            
            # 배경 생성
            if background_style == 'gradient_blue':
                background = self.create_gradient_background(self.TARGET_WIDTH, self.TARGET_HEIGHT)
            else:
                bg_color = self.BACKGROUND_COLORS.get(background_style, (255, 255, 255))
                background = Image.new('RGB', (self.TARGET_WIDTH, self.TARGET_HEIGHT), bg_color)
            
            # 스크린샷 크기 조정 (비율 유지하면서 적절한 크기로)
            # 마케팅 이미지에서 좌우 여백을 고려하여 80% 크기로 조정
            target_screenshot_width = int(self.TARGET_WIDTH * 0.8)
            aspect_ratio = screenshot.height / screenshot.width
            target_screenshot_height = int(target_screenshot_width * aspect_ratio)
            
            # 높이가 너무 크면 높이 기준으로 재조정
            if target_screenshot_height > self.TARGET_HEIGHT * 0.85:
                target_screenshot_height = int(self.TARGET_HEIGHT * 0.85)
                target_screenshot_width = int(target_screenshot_height / aspect_ratio)
            
            screenshot_resized = screenshot.resize(
                (target_screenshot_width, target_screenshot_height),
                Image.Resampling.LANCZOS
            )
            
            # 프레임/그림자 추가
            if add_frame:
                screenshot_with_frame = self.add_device_frame(screenshot_resized)
            else:
                screenshot_with_frame = screenshot_resized
                if screenshot_with_frame.mode != 'RGBA':
                    screenshot_with_frame = screenshot_with_frame.convert('RGBA')
            
            # 중앙에 배치
            x = (self.TARGET_WIDTH - screenshot_with_frame.width) // 2
            y = (self.TARGET_HEIGHT - screenshot_with_frame.height) // 2
            
            # 약간 위쪽으로 배치 (하단에 텍스트 공간 확보)
            y = int(y * 0.8)
            
            # 배경에 스크린샷 합성
            background.paste(screenshot_with_frame, (x, y), screenshot_with_frame)
            
            # RGB로 변환 후 저장
            final_image = background.convert('RGB')
            final_image.save(output_path, 'PNG', quality=95)
            
            print(f"✅ 마케팅 이미지 생성 완료: {output_path}")
            print(f"   최종 크기: {final_image.size}")
            
            return True
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False
    
    def batch_process(self, input_dir, output_dir, add_frame=True, background_style='white'):
        """여러 스크린샷 일괄 처리"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        supported_formats = ('.png', '.jpg', '.jpeg')
        files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_formats)]
        
        print(f"총 {len(files)}개의 이미지를 처리합니다...\n")
        
        success_count = 0
        for i, filename in enumerate(files, 1):
            input_path = os.path.join(input_dir, filename)
            output_filename = f"marketing_{os.path.splitext(filename)[0]}.png"
            output_path = os.path.join(output_dir, output_filename)
            
            print(f"[{i}/{len(files)}] 처리 중: {filename}")
            if self.generate_marketing_image(input_path, output_path, add_frame, background_style):
                success_count += 1
            print()
        
        print(f"완료: {success_count}/{len(files)}개 성공")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='iOS 마케팅 이미지 생성기')
    parser.add_argument('input', help='입력 스크린샷 파일 또는 디렉토리')
    parser.add_argument('-o', '--output', help='출력 파일 또는 디렉토리', default='output')
    parser.add_argument('-b', '--background', 
                       choices=['white', 'black', 'gradient_blue', 'app_store_gray'],
                       default='white',
                       help='배경 스타일 선택')
    parser.add_argument('--no-frame', action='store_true', help='프레임/그림자 효과 제거')
    
    args = parser.parse_args()
    
    generator = MarketingImageGenerator()
    
    # 디렉토리인 경우 일괄 처리
    if os.path.isdir(args.input):
        generator.batch_process(args.input, args.output, not args.no_frame, args.background)
    # 단일 파일인 경우
    else:
        if os.path.isdir(args.output):
            output_file = os.path.join(args.output, 'marketing_image.png')
        else:
            output_file = args.output
        
        generator.generate_marketing_image(args.input, output_file, not args.no_frame, args.background)


if __name__ == '__main__':
    main()
