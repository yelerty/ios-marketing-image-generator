#!/usr/bin/env python3
"""
iOS Marketing Image Generator - Batch Processing
진행률 표시와 함께 대량 이미지 처리
"""

import os
import sys
from pathlib import Path
from tqdm import tqdm
import argparse
from generator import MarketingImageGenerator
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_single_image(args):
    """단일 이미지 처리 (멀티스레딩용)"""
    generator, input_path, output_path, add_frame, background = args
    try:
        success = generator.generate_marketing_image(
            input_path, output_path, add_frame, background
        )
        return (input_path, success, None)
    except Exception as e:
        return (input_path, False, str(e))

def batch_process_parallel(input_dir, output_dir, background='white', 
                          add_frame=True, workers=4):
    """병렬 처리로 여러 이미지 일괄 변환"""
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 입력 파일 찾기
    supported_formats = ('.png', '.jpg', '.jpeg')
    input_files = []
    
    if os.path.isdir(input_dir):
        for ext in supported_formats:
            input_files.extend(Path(input_dir).glob(f'*{ext}'))
            input_files.extend(Path(input_dir).glob(f'*{ext.upper()}'))
    else:
        input_files = [Path(input_dir)]
    
    if not input_files:
        print("❌ 처리할 이미지를 찾을 수 없습니다.")
        return
    
    print(f"\n{'='*60}")
    print(f"📁 입력 폴더: {input_dir}")
    print(f"📁 출력 폴더: {output_dir}")
    print(f"🎨 배경 스타일: {background}")
    print(f"✨ 프레임 효과: {'예' if add_frame else '아니오'}")
    print(f"📊 총 파일 수: {len(input_files)}")
    print(f"⚡ 워커 수: {workers}")
    print(f"{'='*60}\n")
    
    # 작업 준비
    generator = MarketingImageGenerator()
    tasks = []
    
    for input_path in input_files:
        output_filename = f"marketing_{input_path.stem}.png"
        output_path = os.path.join(output_dir, output_filename)
        tasks.append((generator, str(input_path), output_path, add_frame, background))
    
    # 병렬 처리
    success_count = 0
    failed_files = []
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # 작업 제출
        futures = {executor.submit(process_single_image, task): task for task in tasks}
        
        # 진행률 표시
        with tqdm(total=len(tasks), desc="이미지 처리 중", unit="개") as pbar:
            for future in as_completed(futures):
                input_path, success, error = future.result()
                
                if success:
                    success_count += 1
                    pbar.set_postfix({"성공": success_count, "실패": len(failed_files)})
                else:
                    failed_files.append((input_path, error))
                
                pbar.update(1)
    
    # 결과 출력
    print(f"\n{'='*60}")
    print(f"✅ 완료: {success_count}/{len(tasks)}개 성공")
    
    if failed_files:
        print(f"\n❌ 실패한 파일:")
        for path, error in failed_files:
            print(f"   - {os.path.basename(path)}: {error}")
    
    print(f"{'='*60}\n")
    print(f"💾 출력 폴더: {output_dir}")

def main():
    parser = argparse.ArgumentParser(
        description='iOS 마케팅 이미지 대량 생성기',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
예제:
  # 기본 사용
  python batch_processor.py screenshots/ -o output/
  
  # 그라디언트 배경으로 4개의 워커 사용
  python batch_processor.py screenshots/ -o output/ -b gradient_blue -w 4
  
  # 프레임 없이 생성
  python batch_processor.py screenshots/ -o output/ --no-frame
        '''
    )
    
    parser.add_argument('input', help='입력 스크린샷 파일 또는 디렉토리')
    parser.add_argument('-o', '--output', required=True, help='출력 디렉토리')
    parser.add_argument('-b', '--background', 
                       choices=['white', 'black', 'gradient_blue', 'app_store_gray'],
                       default='white',
                       help='배경 스타일 (기본값: white)')
    parser.add_argument('--no-frame', action='store_true', 
                       help='프레임/그림자 효과 제거')
    parser.add_argument('-w', '--workers', type=int, default=4,
                       help='병렬 처리 워커 수 (기본값: 4)')
    
    args = parser.parse_args()
    
    # 입력 경로 확인
    if not os.path.exists(args.input):
        print(f"❌ 오류: '{args.input}' 경로를 찾을 수 없습니다.")
        sys.exit(1)
    
    # 배치 처리 실행
    batch_process_parallel(
        args.input,
        args.output,
        background=args.background,
        add_frame=not args.no_frame,
        workers=args.workers
    )

if __name__ == '__main__':
    main()
