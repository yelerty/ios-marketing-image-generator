#!/usr/bin/env python3
"""
Advanced Marketing Image Generator - Pro GUI
텍스트 오버레이, 멀티 레이아웃 지원
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except:
    HAS_DND = False
import os
from PIL import Image, ImageTk
from generator_advanced import AdvancedMarketingGenerator

class ProMarketingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("iOS Marketing Image Generator - Pro")
        self.root.geometry("1200x800")
        
        self.generator = AdvancedMarketingGenerator()
        self.input_files = []
        self.preview_image = None
        self.gradient_colors = [(74, 144, 226), (155, 89, 182)]
        
        self.setup_ui()
        if HAS_DND:
            self.setup_drag_drop()
    
    def setup_ui(self):
        # 메인 컨테이너
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)
        
        # 좌측 패널 (컨트롤)
        left_panel = tk.Frame(main_container, width=500, bg="#f8f9fa")
        left_panel.pack(side="left", fill="both", expand=False, padx=5, pady=5)
        
        # 우측 패널 (미리보기)
        right_panel = tk.Frame(main_container, bg="#e9ecef", relief="sunken", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # === 좌측 패널 구성 ===
        
        # 제목
        title_frame = tk.Frame(left_panel, bg="#f8f9fa")
        title_frame.pack(pady=10)
        
        tk.Label(
            title_frame,
            text="🎨 Pro Marketing\nImage Generator",
            font=("Arial", 20, "bold"),
            fg="#007AFF",
            bg="#f8f9fa"
        ).pack()
        
        # 스크롤 가능한 컨트롤 영역
        canvas = tk.Canvas(left_panel, bg="#f8f9fa", highlightthickness=0)
        scrollbar = tk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=5)
        scrollbar.pack(side="right", fill="y")
        
        # === 컨트롤 구성 ===
        
        # 1. 파일 선택
        file_frame = tk.LabelFrame(scrollable_frame, text="📁 이미지 선택", 
                                   padx=10, pady=10, bg="#f8f9fa")
        file_frame.pack(fill="x", pady=10, padx=10)
        
        self.drop_label = tk.Label(
            file_frame,
            text="이미지를 드래그하거나\n아래 버튼을 클릭",
            height=3,
            bg="#e8f4f8",
            relief="groove",
            bd=2
        )
        self.drop_label.pack(fill="x", pady=5)
        
        btn_frame = tk.Frame(file_frame, bg="#f8f9fa")
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="📄 파일", command=self.select_files, width=10).pack(side="left", padx=2)
        tk.Button(btn_frame, text="📂 폴더", command=self.select_folder, width=10).pack(side="left", padx=2)
        
        self.file_label = tk.Label(file_frame, text="선택된 파일 없음", 
                                   fg="gray", bg="#f8f9fa")
        self.file_label.pack(pady=5)
        
        # 2. 레이아웃 선택
        layout_frame = tk.LabelFrame(scrollable_frame, text="📱 레이아웃", 
                                     padx=10, pady=10, bg="#f8f9fa")
        layout_frame.pack(fill="x", pady=10, padx=10)
        
        self.layout_var = tk.StringVar(value="single")
        tk.Radiobutton(layout_frame, text="단일 스크린샷", variable=self.layout_var,
                      value="single", bg="#f8f9fa").pack(anchor="w")
        tk.Radiobutton(layout_frame, text="3개 스크린샷 (eBay 스타일)", 
                      variable=self.layout_var, value="triple", bg="#f8f9fa").pack(anchor="w")
        
        # 3. 배경 설정
        bg_frame = tk.LabelFrame(scrollable_frame, text="🎨 배경", 
                                padx=10, pady=10, bg="#f8f9fa")
        bg_frame.pack(fill="x", pady=10, padx=10)
        
        tk.Label(bg_frame, text="스타일:", bg="#f8f9fa").grid(row=0, column=0, sticky="w", pady=5)
        self.bg_style_var = tk.StringVar(value="gradient")
        bg_combo = ttk.Combobox(bg_frame, textvariable=self.bg_style_var,
                               values=["gradient", "solid", "white"],
                               state="readonly", width=15)
        bg_combo.grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(bg_frame, text="그라디언트:", bg="#f8f9fa").grid(row=1, column=0, sticky="w", pady=5)
        self.gradient_btn = tk.Button(bg_frame, text="색상 선택", 
                                     command=self.choose_gradient, width=15)
        self.gradient_btn.grid(row=1, column=1, sticky="w", pady=5)
        
        # 4. 텍스트 오버레이
        text_frame = tk.LabelFrame(scrollable_frame, text="📝 텍스트 오버레이", 
                                  padx=10, pady=10, bg="#f8f9fa")
        text_frame.pack(fill="x", pady=10, padx=10)
        
        tk.Label(text_frame, text="제목:", bg="#f8f9fa").grid(row=0, column=0, sticky="w", pady=5)
        self.title_entry = tk.Entry(text_frame, width=30)
        self.title_entry.grid(row=0, column=1, sticky="w", pady=5, columnspan=2)
        
        tk.Label(text_frame, text="부제목:", bg="#f8f9fa").grid(row=1, column=0, sticky="w", pady=5)
        self.subtitle_entry = tk.Entry(text_frame, width=30)
        self.subtitle_entry.grid(row=1, column=1, sticky="w", pady=5, columnspan=2)
        
        tk.Label(text_frame, text="위치:", bg="#f8f9fa").grid(row=2, column=0, sticky="w", pady=5)
        self.text_pos_var = tk.StringVar(value="top")
        pos_combo = ttk.Combobox(text_frame, textvariable=self.text_pos_var,
                                values=["top", "bottom", "center"],
                                state="readonly", width=12)
        pos_combo.grid(row=2, column=1, sticky="w", pady=5)
        
        tk.Label(text_frame, text="폰트:", bg="#f8f9fa").grid(row=3, column=0, sticky="w", pady=5)
        self.font_var = tk.StringVar(value="helvetica")
        font_combo = ttk.Combobox(text_frame, textvariable=self.font_var,
                                 values=["sf_pro", "helvetica", "roboto", 
                                        "montserrat", "opensans"],
                                 state="readonly", width=12)
        font_combo.grid(row=3, column=1, sticky="w", pady=5)
        
        tk.Label(text_frame, text="제목 크기:", bg="#f8f9fa").grid(row=4, column=0, sticky="w", pady=5)
        self.title_size_var = tk.IntVar(value=90)
        size_spin = tk.Spinbox(text_frame, from_=40, to=150, textvariable=self.title_size_var,
                              width=10)
        size_spin.grid(row=4, column=1, sticky="w", pady=5)
        
        tk.Label(text_frame, text="제목 색상:", bg="#f8f9fa").grid(row=5, column=0, sticky="w", pady=5)
        self.title_color = (60, 120, 255)
        self.title_color_btn = tk.Button(text_frame, text="색상 선택",
                                        command=self.choose_title_color, width=12)
        self.title_color_btn.grid(row=5, column=1, sticky="w", pady=5)
        self.title_color_btn.config(bg="#3c78ff")
        
        # 생성 버튼
        generate_frame = tk.Frame(scrollable_frame, bg="#f8f9fa")
        generate_frame.pack(pady=20)
        
        tk.Button(
            generate_frame,
            text="🎨 마케팅 이미지 생성",
            command=self.generate_images,
            bg="#34C759",
            fg="white",
            font=("Arial", 13, "bold"),
            width=25,
            height=2
        ).pack()
        
        self.status_label = tk.Label(scrollable_frame, text="준비됨", 
                                     fg="#007AFF", bg="#f8f9fa")
        self.status_label.pack(pady=5)
        
        # === 우측 패널 (미리보기) ===
        preview_title = tk.Label(right_panel, text="미리보기", 
                                font=("Arial", 14, "bold"), bg="#e9ecef")
        preview_title.pack(pady=10)
        
        self.preview_label = tk.Label(
            right_panel,
            text="이미지를 선택하면\n여기에 미리보기가 표시됩니다",
            bg="#e9ecef",
            fg="gray",
            font=("Arial", 12)
        )
        self.preview_label.pack(expand=True)
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        try:
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind('<<Drop>>', self.drop_files)
        except:
            pass
    
    def drop_files(self, event):
        """드래그 앤 드롭 처리"""
        files = self.root.tk.splitlist(event.data)
        self.process_file_selection(files)
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="스크린샷 선택",
            filetypes=[("이미지", "*.png *.jpg *.jpeg"), ("모든 파일", "*.*")]
        )
        if files:
            self.process_file_selection(list(files))
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="폴더 선택")
        if folder:
            files = [os.path.join(folder, f) for f in os.listdir(folder)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if files:
                self.process_file_selection(files)
            else:
                messagebox.showwarning("경고", "이미지 파일이 없습니다.")
    
    def process_file_selection(self, files):
        """파일 선택 처리"""
        valid_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if valid_files:
            self.input_files = valid_files
            self.file_label.config(text=f"✓ {len(valid_files)}개 선택됨", fg="#34C759")
            self.show_preview(valid_files[0])
        else:
            messagebox.showwarning("경고", "유효한 이미지가 없습니다.")
    
    def choose_gradient(self):
        """그라디언트 색상 선택"""
        color1 = colorchooser.askcolor(title="그라디언트 시작 색상")
        if color1[0]:
            color2 = colorchooser.askcolor(title="그라디언트 끝 색상")
            if color2[0]:
                self.gradient_colors = [
                    tuple(int(c) for c in color1[0]),
                    tuple(int(c) for c in color2[0])
                ]
                messagebox.showinfo("완료", "그라디언트 색상이 설정되었습니다.")
    
    def choose_title_color(self):
        """제목 색상 선택"""
        color = colorchooser.askcolor(title="제목 색상 선택")
        if color[0]:
            self.title_color = tuple(int(c) for c in color[0])
            self.title_color_btn.config(bg=color[1])
    
    def show_preview(self, image_path):
        """미리보기 표시"""
        try:
            img = Image.open(image_path)
            img.thumbnail((600, 800), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo
        except Exception as e:
            self.preview_label.config(text=f"미리보기 오류:\n{str(e)}", image="")
    
    def generate_images(self):
        if not self.input_files:
            messagebox.showwarning("경고", "이미지를 먼저 선택하세요.")
            return
        
        output_dir = filedialog.askdirectory(title="저장 폴더 선택")
        if not output_dir:
            return
        
        self.status_label.config(text="생성 중...", fg="#FF9500")
        self.root.update()
        
        # 텍스트 설정
        text_config = None
        title = self.title_entry.get().strip()
        subtitle = self.subtitle_entry.get().strip()
        
        if title or subtitle:
            text_config = {
                'title': title,
                'subtitle': subtitle,
                'position': self.text_pos_var.get(),
                'font': self.font_var.get(),
                'title_color': self.title_color,
                'title_size': self.title_size_var.get(),
            }
        
        success_count = 0
        
        # 레이아웃에 따라 처리
        layout = self.layout_var.get()
        
        if layout == 'triple':
            # 3개씩 묶어서 처리
            for i in range(0, len(self.input_files), 3):
                batch = self.input_files[i:i+3]
                output_filename = f"marketing_triple_{i//3+1}.png"
                output_path = os.path.join(output_dir, output_filename)
                
                self.status_label.config(text=f"처리 중... ({i+1}/{len(self.input_files)})")
                self.root.update()
                
                if self.generator.generate_marketing_image(
                    batch, output_path, layout=layout,
                    background_style=self.bg_style_var.get(),
                    background_colors=self.gradient_colors,
                    text_config=text_config
                ):
                    success_count += 1
        else:
            # 단일 처리
            for i, input_file in enumerate(self.input_files, 1):
                filename = os.path.basename(input_file)
                output_filename = f"marketing_{os.path.splitext(filename)[0]}.png"
                output_path = os.path.join(output_dir, output_filename)
                
                self.status_label.config(text=f"처리 중... ({i}/{len(self.input_files)})")
                self.root.update()
                
                if self.generator.generate_marketing_image(
                    [input_file], output_path, layout=layout,
                    background_style=self.bg_style_var.get(),
                    background_colors=self.gradient_colors,
                    text_config=text_config
                ):
                    success_count += 1
        
        self.status_label.config(text=f"✓ 완료! {success_count}개 성공", fg="#34C759")
        messagebox.showinfo("완료", f"{success_count}개 생성 완료!\n\n{output_dir}")


def main():
    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
        print("알림: 드래그 앤 드롭을 사용하려면 'pip install tkinterdnd2'")
    
    app = ProMarketingGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
