#!/usr/bin/env python3
"""
Interactive Marketing Image Generator
마우스로 텍스트 위치를 자유롭게 조정할 수 있는 GUI
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class InteractiveMarketingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Marketing Image Generator")
        self.root.geometry("1400x900")
        
        # 상태 변수
        self.screenshots = []
        self.background_image = None
        self.canvas_image = None
        self.text_items = []  # [(text, x, y, font_size, color), ...]
        self.dragging_item = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # 설정
        self.gradient_colors = [(230, 230, 245), (255, 255, 255)]
        self.current_font = 'helvetica'
        self.current_color = (60, 120, 255)
        
        self.setup_ui()
    
    def setup_ui(self):
        # 메인 컨테이너
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)
        
        # 왼쪽 패널 (컨트롤)
        left_panel = tk.Frame(main_container, width=350, bg="#f8f9fa")
        left_panel.pack(side="left", fill="y", padx=5, pady=5)
        left_panel.pack_propagate(False)
        
        # 오른쪽 패널 (캔버스)
        right_panel = tk.Frame(main_container, bg="#e9ecef")
        right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # === 왼쪽 패널 ===
        
        # 제목
        tk.Label(
            left_panel,
            text="🎨 Interactive\nMarketing Generator",
            font=("Arial", 18, "bold"),
            fg="#007AFF",
            bg="#f8f9fa"
        ).pack(pady=15)
        
        # 1. 이미지 선택
        img_frame = tk.LabelFrame(left_panel, text="📱 이미지", padx=10, pady=10, bg="#f8f9fa")
        img_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(img_frame, text="📄 스크린샷 추가", command=self.add_screenshots,
                 width=20).pack(pady=5)
        tk.Button(img_frame, text="🖼️ 배경 이미지 선택", command=self.select_background,
                 width=20).pack(pady=5)
        
        self.img_label = tk.Label(img_frame, text="이미지 없음", fg="gray", bg="#f8f9fa")
        self.img_label.pack(pady=5)
        
        # 2. 텍스트 추가
        text_frame = tk.LabelFrame(left_panel, text="📝 텍스트 추가", padx=10, pady=10, bg="#f8f9fa")
        text_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(text_frame, text="텍스트:", bg="#f8f9fa").pack(anchor="w")
        self.text_entry = tk.Entry(text_frame, width=30)
        self.text_entry.pack(pady=5)
        
        tk.Label(text_frame, text="폰트 크기:", bg="#f8f9fa").pack(anchor="w")
        self.font_size_var = tk.IntVar(value=90)
        tk.Scale(text_frame, from_=30, to=150, orient="horizontal",
                variable=self.font_size_var, bg="#f8f9fa").pack(fill="x", pady=5)
        
        tk.Label(text_frame, text="폰트:", bg="#f8f9fa").pack(anchor="w")
        self.font_var = tk.StringVar(value="helvetica")
        font_combo = ttk.Combobox(text_frame, textvariable=self.font_var,
                                 values=["helvetica", "sf_pro", "roboto", "montserrat"],
                                 state="readonly", width=27)
        font_combo.pack(pady=5)
        
        tk.Button(text_frame, text="🎨 텍스트 색상", command=self.choose_text_color,
                 width=20).pack(pady=5)
        
        tk.Button(text_frame, text="➕ 텍스트 추가", command=self.add_text,
                 bg="#34C759", fg="white", font=("Arial", 11, "bold"),
                 width=20, height=2).pack(pady=10)
        
        # 3. 텍스트 목록
        list_frame = tk.LabelFrame(left_panel, text="📋 텍스트 목록", padx=10, pady=10, bg="#f8f9fa")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.text_listbox = tk.Listbox(list_frame, height=8)
        self.text_listbox.pack(fill="both", expand=True)
        
        btn_frame = tk.Frame(list_frame, bg="#f8f9fa")
        btn_frame.pack(fill="x", pady=5)
        
        tk.Button(btn_frame, text="🗑️ 삭제", command=self.delete_text, width=15).pack(side="left", padx=2)
        tk.Button(btn_frame, text="🔄 새로고침", command=self.refresh_canvas, width=15).pack(side="left", padx=2)
        
        # 4. 저장
        save_frame = tk.Frame(left_panel, bg="#f8f9fa")
        save_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(save_frame, text="💾 이미지 저장", command=self.save_image,
                 bg="#007AFF", fg="white", font=("Arial", 12, "bold"),
                 width=25, height=2).pack()
        
        self.status_label = tk.Label(left_panel, text="준비됨", fg="#007AFF", bg="#f8f9fa")
        self.status_label.pack(pady=5)
        
        # === 오른쪽 패널 (캔버스) ===
        
        canvas_title = tk.Label(right_panel, text="🖼️ 마케팅 이미지 미리보기 (텍스트를 드래그하여 위치 조정)",
                               font=("Arial", 12, "bold"), bg="#e9ecef")
        canvas_title.pack(pady=10)
        
        # 스크롤 가능한 캔버스
        canvas_frame = tk.Frame(right_panel, bg="#e9ecef")
        canvas_frame.pack(fill="both", expand=True)
        
        h_scroll = tk.Scrollbar(canvas_frame, orient="horizontal")
        v_scroll = tk.Scrollbar(canvas_frame, orient="vertical")
        
        self.canvas = tk.Canvas(canvas_frame, bg="white",
                               xscrollcommand=h_scroll.set,
                               yscrollcommand=v_scroll.set,
                               width=1000, height=700)
        
        h_scroll.config(command=self.canvas.xview)
        v_scroll.config(command=self.canvas.yview)
        
        h_scroll.pack(side="bottom", fill="x")
        v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        # 초기 캔버스
        self.create_initial_canvas()
    
    def create_initial_canvas(self):
        """초기 빈 캔버스 생성"""
        self.working_image = Image.new('RGB', (1290, 2796), (240, 240, 245))
        self.refresh_canvas()
    
    def add_screenshots(self):
        """스크린샷 추가"""
        files = filedialog.askopenfilenames(
            title="스크린샷 선택",
            filetypes=[("이미지", "*.png *.jpg *.jpeg")]
        )
        if files:
            for file in files:
                self.screenshots.append(Image.open(file))
            self.img_label.config(text=f"✓ {len(self.screenshots)}개 스크린샷", fg="#34C759")
            self.compose_image()
    
    def select_background(self):
        """배경 이미지 선택"""
        file = filedialog.askopenfilename(
            title="배경 이미지 선택",
            filetypes=[("이미지", "*.png *.jpg *.jpeg")]
        )
        if file:
            self.background_image = Image.open(file)
            self.img_label.config(text="✓ 배경 이미지 선택됨", fg="#34C759")
            self.compose_image()
    
    def compose_image(self):
        """스크린샷과 배경을 합성"""
        # 배경 이미지 사용 또는 기본 배경
        if self.background_image:
            self.working_image = self.background_image.resize((1290, 2796), Image.LANCZOS).convert('RGB')
        else:
            # 그라디언트 배경 생성
            self.working_image = self.create_gradient()
        
        # 스크린샷 추가
        if self.screenshots:
            if len(self.screenshots) == 1:
                self.add_single_screenshot()
            else:
                self.add_multiple_screenshots()
        
        self.refresh_canvas()
    
    def create_gradient(self):
        """그라디언트 배경 생성"""
        width, height = 1290, 2796
        base = Image.new('RGB', (width, height), self.gradient_colors[0])
        top = Image.new('RGB', (width, height), self.gradient_colors[1])
        mask = Image.new('L', (width, height))
        
        mask_data = []
        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)
        mask.putdata(mask_data)
        
        base.paste(top, (0, 0), mask)
        return base
    
    def add_single_screenshot(self):
        """단일 스크린샷 추가"""
        screenshot = self.screenshots[0]
        
        # 크기 조정
        target_width = int(1290 * 0.75)
        aspect_ratio = screenshot.height / screenshot.width
        target_height = int(target_width * aspect_ratio)
        
        if target_height > 2796 * 0.7:
            target_height = int(2796 * 0.7)
            target_width = int(target_height / aspect_ratio)
        
        resized = screenshot.resize((target_width, target_height), Image.LANCZOS)
        
        # 프레임 추가
        framed = self.add_phone_frame(resized)
        
        # 중앙 배치
        x = (1290 - framed.width) // 2
        y = (2796 - framed.height) // 2
        
        self.working_image.paste(framed, (x, y), framed if framed.mode == 'RGBA' else None)
    
    def add_multiple_screenshots(self):
        """여러 스크린샷 추가 (최대 3개)"""
        screenshots = self.screenshots[:3]
        target_width = int(1290 * 0.28)
        
        phone_images = []
        for i, screenshot in enumerate(screenshots):
            aspect_ratio = screenshot.height / screenshot.width
            target_height = int(target_width * aspect_ratio)
            
            if target_height > 2796 * 0.65:
                target_height = int(2796 * 0.65)
                target_width_adj = int(target_height / aspect_ratio)
            else:
                target_width_adj = target_width
            
            resized = screenshot.resize((target_width_adj, target_height), Image.LANCZOS)
            
            # 회전 효과
            if i == 0:
                angle = -12
            elif i == 2:
                angle = 12
            else:
                angle = 0
            
            if angle != 0:
                resized = resized.rotate(angle, expand=True, resample=Image.BICUBIC)
            
            framed = self.add_phone_frame(resized)
            phone_images.append(framed)
        
        # 배치
        spacing = 20
        total_width = sum(img.width for img in phone_images) + spacing * 2
        start_x = (1290 - total_width) // 2
        start_y = int(2796 * 0.4)
        
        x_offset = start_x
        for i, img in enumerate(phone_images):
            y_offset = start_y + (i % 2) * 30
            self.working_image.paste(img, (x_offset, y_offset), img if img.mode == 'RGBA' else None)
            x_offset += img.width + spacing
    
    def add_phone_frame(self, screenshot):
        """iPhone 스타일 프레임"""
        from PIL import ImageFilter
        
        frame_padding = 10
        shadow_offset = 40
        corner_radius = 60
        
        total_width = screenshot.width + frame_padding * 2 + shadow_offset * 2
        total_height = screenshot.height + frame_padding * 2 + shadow_offset * 2
        
        result = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
        
        # 그림자
        shadow = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            [shadow_offset, shadow_offset,
             screenshot.width + frame_padding * 2 + shadow_offset,
             screenshot.height + frame_padding * 2 + shadow_offset],
            radius=corner_radius, fill=(0, 0, 0, 80)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(20))
        result.paste(shadow, (0, 0), shadow)
        
        # 프레임
        frame = Image.new('RGBA', 
                         (screenshot.width + frame_padding * 2,
                          screenshot.height + frame_padding * 2),
                         (20, 20, 20, 255))
        
        if screenshot.mode != 'RGBA':
            screenshot = screenshot.convert('RGBA')
        
        frame.paste(screenshot, (frame_padding, frame_padding), screenshot)
        
        # 둥근 모서리
        mask = Image.new('L', frame.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, frame.width, frame.height],
                                    radius=corner_radius, fill=255)
        frame.putalpha(mask)
        
        result.paste(frame, (shadow_offset // 2, shadow_offset // 2), frame)
        
        return result
    
    def choose_text_color(self):
        """텍스트 색상 선택"""
        color = colorchooser.askcolor(title="텍스트 색상")
        if color[0]:
            self.current_color = tuple(int(c) for c in color[0])
            messagebox.showinfo("완료", "텍스트 색상이 설정되었습니다.")
    
    def add_text(self):
        """텍스트 추가"""
        text = self.text_entry.get().strip()
        if not text:
            messagebox.showwarning("경고", "텍스트를 입력하세요.")
            return
        
        # 중앙 위치에 추가
        x = 1290 // 2
        y = 200
        font_size = self.font_size_var.get()
        
        self.text_items.append({
            'text': text,
            'x': x,
            'y': y,
            'font_size': font_size,
            'color': self.current_color,
            'font': self.font_var.get()
        })
        
        self.text_listbox.insert(tk.END, f"{text} ({font_size}px)")
        self.text_entry.delete(0, tk.END)
        self.refresh_canvas()
    
    def delete_text(self):
        """선택된 텍스트 삭제"""
        selection = self.text_listbox.curselection()
        if selection:
            idx = selection[0]
            self.text_items.pop(idx)
            self.text_listbox.delete(idx)
            self.refresh_canvas()
    
    def refresh_canvas(self):
        """캔버스 새로고침"""
        # 작업 이미지 복사
        display_image = self.working_image.copy()
        draw = ImageDraw.Draw(display_image)
        
        # 텍스트 그리기
        for item in self.text_items:
            try:
                font = self.get_font(item['font'], item['font_size'])
            except:
                font = ImageFont.load_default()
            
            text = item['text']
            x = item['x']
            y = item['y']
            color = item['color']
            
            # 중앙 정렬을 위해 텍스트 크기 계산
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            
            # 그림자
            draw.text((x - text_width//2 + 3, y + 3), text, font=font, fill=(0, 0, 0, 100))
            # 텍스트
            draw.text((x - text_width//2, y), text, font=font, fill=color)
        
        # 캔버스 크기에 맞게 조정
        display_scale = 0.4  # 화면 표시용 스케일
        display_width = int(1290 * display_scale)
        display_height = int(2796 * display_scale)
        
        display_resized = display_image.resize((display_width, display_height), Image.LANCZOS)
        
        self.canvas_photo = ImageTk.PhotoImage(display_resized)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.canvas_photo)
        self.canvas.config(scrollregion=(0, 0, display_width, display_height))
        
        self.status_label.config(text=f"✓ {len(self.text_items)}개 텍스트", fg="#34C759")
    
    def get_font(self, font_name, size):
        """폰트 로드"""
        font_paths = {
            'helvetica': ['/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'],
            'roboto': ['/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf'],
            'sf_pro': ['/System/Library/Fonts/SF-Pro-Display-Bold.otf'],
            'montserrat': ['/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf'],
        }
        
        paths = font_paths.get(font_name, font_paths['helvetica'])
        
        for path in paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    continue
        
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except:
            return ImageFont.load_default()
    
    def on_canvas_click(self, event):
        """캔버스 클릭"""
        # 실제 좌표로 변환 (스케일 고려)
        scale = 0.4
        real_x = int(event.x / scale)
        real_y = int(event.y / scale)
        
        # 클릭한 텍스트 찾기
        for i, item in enumerate(self.text_items):
            # 텍스트 범위 체크 (대략적)
            if abs(real_x - item['x']) < 300 and abs(real_y - item['y']) < 100:
                self.dragging_item = i
                self.drag_start_x = real_x - item['x']
                self.drag_start_y = real_y - item['y']
                self.text_listbox.selection_clear(0, tk.END)
                self.text_listbox.selection_set(i)
                break
    
    def on_canvas_drag(self, event):
        """캔버스 드래그"""
        if self.dragging_item is not None:
            scale = 0.4
            real_x = int(event.x / scale)
            real_y = int(event.y / scale)
            
            self.text_items[self.dragging_item]['x'] = real_x - self.drag_start_x
            self.text_items[self.dragging_item]['y'] = real_y - self.drag_start_y
            
            self.refresh_canvas()
    
    def on_canvas_release(self, event):
        """마우스 버튼 릴리스"""
        self.dragging_item = None
    
    def save_image(self):
        """이미지 저장"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")],
            initialfile="marketing_image.png"
        )
        
        if file_path:
            # 최종 이미지 생성
            final_image = self.working_image.copy()
            draw = ImageDraw.Draw(final_image)
            
            for item in self.text_items:
                try:
                    font = self.get_font(item['font'], item['font_size'])
                except:
                    font = ImageFont.load_default()
                
                text = item['text']
                x = item['x']
                y = item['y']
                color = item['color']
                
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                
                # 그림자
                draw.text((x - text_width//2 + 3, y + 3), text, font=font, fill=(0, 0, 0, 100))
                # 텍스트
                draw.text((x - text_width//2, y), text, font=font, fill=color)
            
            final_image.save(file_path, quality=95)
            messagebox.showinfo("완료", f"저장 완료!\n{file_path}")
            self.status_label.config(text="✓ 이미지 저장 완료!", fg="#34C759")


def main():
    root = tk.Tk()
    app = InteractiveMarketingGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
