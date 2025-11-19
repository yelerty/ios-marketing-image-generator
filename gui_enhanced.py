#!/usr/bin/env python3
"""
iOS Marketing Image Generator - Enhanced GUI Version
드래그 앤 드롭, 미리보기, 텍스트 오버레이 기능 포함
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from PIL import Image, ImageTk
from generator import MarketingImageGenerator

class EnhancedMarketingImageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("iOS Marketing Image Generator - Enhanced")
        self.root.geometry("900x700")

        self.generator = MarketingImageGenerator()
        self.input_files = []
        self.preview_image = None

        # 최근 경로 저장 (Downloads 폴더를 기본값으로)
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.last_input_dir = downloads_path if os.path.exists(downloads_path) else os.path.expanduser("~")
        self.last_output_dir = downloads_path if os.path.exists(downloads_path) else os.path.expanduser("~")

        # 배경 이미지
        self.background_image_path = None
        self.background_image = None
        self.bg_image_scale = 1.0  # 배경 이미지 스케일 (1.0 = 100%)

        # 출력 이미지 사이즈
        self.output_width = 1290
        self.output_height = 2796

        # iPhone 17 프레임 오버레이
        self.iphone_frame = None
        self.iphone_frame_path = None

        self.setup_ui()
        self.setup_drag_drop()
    
    def setup_ui(self):
        # 메인 컨테이너
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 왼쪽 패널 프레임 (스크롤바 포함)
        left_frame_container = tk.Frame(main_container, width=320)
        left_frame_container.pack(side="left", fill="both", expand=False, padx=(0, 10))

        # 캔버스와 스크롤바
        canvas = tk.Canvas(left_frame_container, width=300)
        scrollbar = tk.Scrollbar(left_frame_container, orient="vertical", command=canvas.yview)

        left_panel = tk.Frame(canvas)

        left_panel.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=left_panel, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 마우스 휠 스크롤 지원
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 오른쪽 패널 (미리보기)
        right_panel = tk.Frame(main_container, bg="#f0f0f0", relief="sunken", bd=2)
        right_panel.pack(side="right", fill="both", expand=True)

        # === 왼쪽 패널 구성 ===
        
        # 제목
        title_label = tk.Label(
            left_panel,
            text="iOS Marketing\nImage Generator",
            font=("Arial", 14, "bold"),
            fg="#007AFF"
        )
        title_label.pack(pady=5)

        # 드래그 앤 드롭 영역
        drop_frame = tk.LabelFrame(left_panel, text="📁 파일 선택", padx=3, pady=3)
        drop_frame.pack(fill="x", pady=3)
        
        self.drop_label = tk.Label(
            drop_frame,
            text="이미지를 드래그하거나\n버튼 클릭",
            height=2,
            bg="#e8f4f8",
            relief="groove",
            bd=2,
            font=("Arial", 8)
        )
        self.drop_label.pack(anchor="w", pady=3, padx=3)

        tk.Button(
            drop_frame,
            text="📄 파일 선택",
            command=self.select_files,
            width=10
        ).pack(anchor="w", pady=3, padx=3)
        
        # 선택된 파일 표시
        self.file_label = tk.Label(
            drop_frame,
            text="선택된 파일 없음",
            fg="gray",
            font=("Arial", 8)
        )
        self.file_label.pack(pady=3)

        # 출력 이미지 사이즈 설정
        size_frame = tk.LabelFrame(left_panel, text="📐 출력 이미지 사이즈", padx=3, pady=3)
        size_frame.pack(fill="x", pady=3)

        tk.Label(size_frame, text="사이즈:").grid(row=0, column=0, sticky="w", pady=2)
        self.size_var = tk.StringVar(value="1290x2796")
        size_combo = ttk.Combobox(
            size_frame,
            textvariable=self.size_var,
            values=["1290x2796 (App Store)", "1242x2688 (iPhone 11 Pro)", "1080x1920 (Full HD)", "커스텀"],
            state="readonly",
            width=14
        )
        size_combo.grid(row=0, column=1, sticky="w", pady=2)
        size_combo.bind("<<ComboboxSelected>>", self.on_size_change)

        # 커스텀 사이즈 입력
        tk.Label(size_frame, text="너비:").grid(row=1, column=0, sticky="w", pady=2)
        self.width_entry = tk.Entry(size_frame, width=8, state="disabled")
        self.width_entry.insert(0, "1290")
        self.width_entry.grid(row=1, column=1, sticky="w", pady=2)

        tk.Label(size_frame, text="높이:").grid(row=2, column=0, sticky="w", pady=2)
        self.height_entry = tk.Entry(size_frame, width=8, state="disabled")
        self.height_entry.insert(0, "2796")
        self.height_entry.grid(row=2, column=1, sticky="w", pady=2)

        # 현재 사이즈 표시
        self.current_size_label = tk.Label(
            size_frame,
            text="현재: 1290 x 2796",
            fg="#007AFF",
            font=("Arial", 9, "bold")
        )
        self.current_size_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=2)

        # 배경 옵션
        bg_frame = tk.LabelFrame(left_panel, text="🎨 배경 설정", padx=3, pady=3)
        bg_frame.pack(fill="x", pady=3)
        
        tk.Label(bg_frame, text="배경 스타일:").grid(row=0, column=0, sticky="w", pady=2)
        self.background_var = tk.StringVar(value="image")
        background_combo = ttk.Combobox(
            bg_frame,
            textvariable=self.background_var,
            values=["image", "white", "black", "gradient_blue", "app_store_gray", "custom"],
            state="readonly",
            width=14
        )
        background_combo.grid(row=0, column=1, sticky="w", pady=5)
        background_combo.bind("<<ComboboxSelected>>", self.on_background_change)

        # 커스텀 색상 버튼
        self.custom_color_btn = tk.Button(
            bg_frame,
            text="색상 선택",
            command=self.choose_custom_color,
            state="disabled",
            width=10
        )
        self.custom_color_btn.grid(row=1, column=1, sticky="w", pady=5)
        self.custom_color = (255, 255, 255)

        # 배경 이미지 버튼
        tk.Label(bg_frame, text="배경 이미지:").grid(row=2, column=0, sticky="w", pady=5)
        self.bg_image_btn = tk.Button(
            bg_frame,
            text="이미지 선택",
            command=self.choose_background_image,
            state="disabled",
            width=10
        )
        self.bg_image_btn.grid(row=2, column=1, sticky="w", pady=5)

        self.bg_image_label = tk.Label(
            bg_frame,
            text="없음",
            fg="gray",
            font=("Arial", 8)
        )
        self.bg_image_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=2)

        # 배경 이미지 크기 조절
        tk.Label(bg_frame, text="배경 크기:").grid(row=4, column=0, sticky="w", pady=5)

        scale_frame = tk.Frame(bg_frame)
        scale_frame.grid(row=4, column=1, sticky="w", pady=5)

        self.bg_scale_slider = tk.Scale(
            scale_frame,
            from_=50,
            to=200,
            orient=tk.HORIZONTAL,
            length=80,
            command=self.on_bg_scale_change,
            state="disabled"
        )
        self.bg_scale_slider.set(100)
        self.bg_scale_slider.pack(side="left")

        self.bg_scale_label = tk.Label(scale_frame, text="100%", width=4)
        self.bg_scale_label.pack(side="left", padx=3)

        # 실제 크기 맞추기 버튼
        self.bg_fit_btn = tk.Button(
            bg_frame,
            text="실제 크기 맞추기",
            command=self.fit_background_to_actual_size,
            state="disabled",
            width=12
        )
        self.bg_fit_btn.grid(row=5, column=1, sticky="w", pady=3)

        # 효과 옵션
        effect_frame = tk.LabelFrame(left_panel, text="✨ 효과", padx=3, pady=3)
        effect_frame.pack(fill="x", pady=3)
        
        self.frame_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            effect_frame,
            text="그림자/프레임 효과",
            variable=self.frame_var
        ).pack(anchor="w", pady=2)
        
        self.rounded_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            effect_frame,
            text="모서리 둥글게",
            variable=self.rounded_var
        ).pack(anchor="w", pady=2)

        self.border_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            effect_frame,
            text="최종 이미지 테두리 표시",
            variable=self.border_var
        ).pack(anchor="w", pady=2)

        # iPhone 17 프레임 오버레이
        frame_overlay = tk.LabelFrame(left_panel, text="📱 iPhone 17 프레임", padx=3, pady=3)
        frame_overlay.pack(fill="x", pady=3)

        tk.Label(frame_overlay, text="프레임 색상:", font=("Arial", 9, "bold")).pack(anchor="w", pady=2)

        btn_frame = tk.Frame(frame_overlay)
        btn_frame.pack(pady=3)

        tk.Button(
            btn_frame,
            text="Lavender",
            command=lambda: self.select_iphone_frame("Lavender"),
            bg="#E6D7FF",
            width=7
        ).pack(side="left", padx=2)

        tk.Button(
            btn_frame,
            text="Mist Blue",
            command=lambda: self.select_iphone_frame("Mist Blue"),
            bg="#C5E1F5",
            width=7
        ).pack(side="left", padx=2)

        tk.Button(
            btn_frame,
            text="Sage",
            command=lambda: self.select_iphone_frame("Sage"),
            bg="#D4E8D4",
            width=7
        ).pack(side="left", padx=2)

        tk.Button(
            btn_frame,
            text="제거",
            command=self.remove_iphone_frame,
            bg="#FFE0E0",
            width=6
        ).pack(side="left", padx=2)

        self.frame_status_label = tk.Label(
            frame_overlay,
            text="선택 안됨",
            fg="gray",
            font=("Arial", 8)
        )
        self.frame_status_label.pack(pady=2)

        # 텍스트 오버레이 옵션
        text_frame = tk.LabelFrame(left_panel, text="📝 텍스트 추가", padx=3, pady=3)
        text_frame.pack(fill="x", pady=3)
        
        self.text_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            text_frame,
            text="텍스트 오버레이 활성화",
            variable=self.text_var,
            command=self.toggle_text_options
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=2)

        tk.Label(text_frame, text="텍스트:").grid(row=1, column=0, sticky="w", pady=5)
        self.text_entry = tk.Entry(text_frame, width=18, state="disabled")
        self.text_entry.grid(row=1, column=1, sticky="w", pady=5)

        # 텍스트 입력창에 우클릭 메뉴 추가
        self.text_context_menu = tk.Menu(self.text_entry, tearoff=0)
        self.text_context_menu.add_command(label="잘라내기", command=lambda: self.text_entry.event_generate("<<Cut>>"))
        self.text_context_menu.add_command(label="복사", command=lambda: self.text_entry.event_generate("<<Copy>>"))
        self.text_context_menu.add_command(label="붙여넣기", command=lambda: self.text_entry.event_generate("<<Paste>>"))
        self.text_context_menu.add_separator()
        self.text_context_menu.add_command(label="전체 선택", command=lambda: self.text_entry.select_range(0, tk.END))

        def show_text_context_menu(event):
            self.text_context_menu.post(event.x_root, event.y_root)

        self.text_entry.bind("<Button-2>", show_text_context_menu)  # macOS 우클릭
        self.text_entry.bind("<Button-3>", show_text_context_menu)  # Windows/Linux 우클릭

        tk.Label(text_frame, text="텍스트 위치:").grid(row=2, column=0, sticky="w", pady=5)
        self.text_position_var = tk.StringVar(value="bottom")
        text_pos_combo = ttk.Combobox(
            text_frame,
            textvariable=self.text_position_var,
            values=["top", "center", "bottom"],
            state="readonly",
            width=14
        )
        text_pos_combo.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(text_frame, text="텍스트 크기:").grid(row=3, column=0, sticky="w", pady=5)
        self.text_size_var = tk.IntVar(value=60)
        text_size_spinner = tk.Spinbox(
            text_frame,
            from_=20,
            to=150,
            textvariable=self.text_size_var,
            width=16,
            state="disabled"
        )
        text_size_spinner.grid(row=3, column=1, sticky="w", pady=5)
        self.text_size_spinner = text_size_spinner

        # 텍스트 색상 선택
        tk.Label(text_frame, text="텍스트 색상:").grid(row=4, column=0, sticky="w", pady=5)
        self.text_color_btn = tk.Button(
            text_frame,
            text="색상 선택",
            command=self.choose_text_color,
            state="disabled",
            width=10,
            bg="white"
        )
        self.text_color_btn.grid(row=4, column=1, sticky="w", pady=5)
        self.text_color = (255, 255, 255)  # 기본 흰색

        # 생성 전 미리보기 버튼 (크기 증가, 파란색 텍스트)
        tk.Button(
            left_panel,
            text="👁️ 미리보기",
            command=self.preview_marketing_image,
            bg="#E8F4FF",
            fg="#007AFF",
            font=("Arial", 13, "bold"),
            width=18,
            height=2,
            relief="raised",
            bd=3
        ).pack(anchor="w", pady=5, padx=3)

        # 생성 버튼 (파란색 텍스트)
        tk.Button(
            left_panel,
            text="🎨 마케팅 이미지 생성",
            command=self.generate_images,
            bg="#E8F4FF",
            fg="#007AFF",
            font=("Arial", 13, "bold"),
            width=18,
            height=2,
            relief="raised",
            bd=3
        ).pack(anchor="w", pady=15, padx=3)
        
        # 상태 표시
        self.status_label = tk.Label(
            left_panel,
            text="준비됨",
            fg="#007AFF",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=5)
        
        # === 오른쪽 패널 (미리보기) ===
        preview_title = tk.Label(
            right_panel,
            text="미리보기",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        )
        preview_title.pack(pady=10)
        
        self.preview_label = tk.Label(
            right_panel,
            text="이미지를 선택하면\n여기에 미리보기가 표시됩니다",
            bg="#f0f0f0",
            fg="gray",
            font=("Arial", 11)
        )
        self.preview_label.pack(expand=True, fill="both", padx=20, pady=20)

        # 초기 배경 스타일이 'image'이므로 버튼 활성화
        self.on_background_change()

    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        try:
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind('<<Drop>>', self.drop_files)
        except:
            # tkinterdnd2가 없으면 무시
            pass
    
    def drop_files(self, event):
        """드래그 앤 드롭된 파일 처리"""
        files = self.root.tk.splitlist(event.data)
        supported_formats = ('.png', '.jpg', '.jpeg')
        
        valid_files = []
        for file_path in files:
            if os.path.isfile(file_path) and file_path.lower().endswith(supported_formats):
                valid_files.append(file_path)
            elif os.path.isdir(file_path):
                # 폴더인 경우 내부 이미지 파일 가져오기
                for f in os.listdir(file_path):
                    full_path = os.path.join(file_path, f)
                    if f.lower().endswith(supported_formats):
                        valid_files.append(full_path)
        
        if valid_files:
            self.input_files = valid_files
            self.file_label.config(
                text=f"✓ {len(valid_files)}개 파일 선택됨",
                fg="#34C759"
            )
            # 배경 이미지를 유지하기 위해 show_preview 제거
            # 사용자가 미리보기 버튼을 눌러야 미리보기 업데이트
        else:
            messagebox.showwarning("경고", "유효한 이미지 파일이 없습니다.")
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="스크린샷 선택",
            initialdir=self.last_input_dir,
            filetypes=[
                ("이미지 파일", "*.png *.jpg *.jpeg"),
                ("모든 파일", "*.*")
            ]
        )
        if files:
            self.input_files = list(files)
            # 선택한 파일의 디렉토리를 저장
            self.last_input_dir = os.path.dirname(files[0])
            self.file_label.config(
                text=f"✓ {len(files)}개 파일 선택됨",
                fg="#34C759"
            )
            # 메인 이미지 선택 시 자동 미리보기
            self.preview_marketing_image()
    
    def select_folder(self):
        folder = filedialog.askdirectory(
            title="스크린샷 폴더 선택",
            initialdir=self.last_input_dir
        )
        if folder:
            # 선택한 폴더를 저장
            self.last_input_dir = folder
            supported_formats = ('.png', '.jpg', '.jpeg')
            files = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(supported_formats)
            ]
            if files:
                self.input_files = files
                self.file_label.config(
                    text=f"✓ {len(files)}개 파일 선택됨",
                    fg="#34C759"
                )
                # 배경 이미지를 유지하기 위해 show_preview 제거
            else:
                messagebox.showwarning("경고", "이미지 파일을 찾을 수 없습니다.")
    
    def on_size_change(self, event=None):
        """출력 사이즈 변경"""
        size_selection = self.size_var.get()

        if size_selection == "커스텀":
            self.width_entry.config(state="normal")
            self.height_entry.config(state="normal")
        else:
            self.width_entry.config(state="disabled")
            self.height_entry.config(state="disabled")

            # 프리셋 사이즈 적용
            if "1290x2796" in size_selection:
                width, height = 1290, 2796
            elif "1242x2688" in size_selection:
                width, height = 1242, 2688
            elif "1080x1920" in size_selection:
                width, height = 1080, 1920
            else:
                width, height = 1290, 2796

            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, str(width))
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, str(height))

        # 현재 사이즈 업데이트
        self.update_output_size()

    def update_output_size(self):
        """출력 사이즈 업데이트"""
        try:
            self.output_width = int(self.width_entry.get())
            self.output_height = int(self.height_entry.get())
            self.current_size_label.config(
                text=f"현재: {self.output_width} x {self.output_height}"
            )
        except ValueError:
            pass

    def on_background_change(self, event=None):
        """배경 스타일 변경 시 처리"""
        bg_style = self.background_var.get()

        if bg_style == "custom":
            self.custom_color_btn.config(state="normal")
            self.bg_image_btn.config(state="disabled")
        elif bg_style == "image":
            self.custom_color_btn.config(state="disabled")
            self.bg_image_btn.config(state="normal")
        else:
            self.custom_color_btn.config(state="disabled")
            self.bg_image_btn.config(state="disabled")
    
    def choose_custom_color(self):
        """커스텀 배경 색상 선택"""
        color = colorchooser.askcolor(title="배경 색상 선택")
        if color[0]:
            self.custom_color = tuple(int(c) for c in color[0])
            self.custom_color_btn.config(bg=color[1])

    def select_iphone_frame(self, color):
        """iPhone 17 프레임 선택"""
        frame_filename = f"iPhone 17 - {color} - Portrait.png"
        frame_path = os.path.join(os.getcwd(), frame_filename)

        if os.path.exists(frame_path):
            try:
                self.iphone_frame = Image.open(frame_path)
                self.iphone_frame_path = frame_path
                self.frame_status_label.config(
                    text=f"✓ {color} 선택됨",
                    fg="#34C759"
                )
                print(f"iPhone 17 프레임 로드: {color}")
                # 프레임 선택 시 자동 미리보기
                if self.input_files:
                    self.preview_marketing_image()
            except Exception as e:
                messagebox.showerror("오류", f"프레임 이미지를 열 수 없습니다:\n{str(e)}")
        else:
            messagebox.showerror("오류", f"프레임 파일을 찾을 수 없습니다:\n{frame_filename}")

    def remove_iphone_frame(self):
        """iPhone 17 프레임 제거"""
        self.iphone_frame = None
        self.iphone_frame_path = None
        self.frame_status_label.config(
            text="선택 안됨",
            fg="gray"
        )
        print("iPhone 17 프레임 제거됨")
        # 프레임 제거 시 자동 미리보기
        if self.input_files:
            self.preview_marketing_image()

    def choose_background_image(self):
        """배경 이미지 선택"""
        file_path = filedialog.askopenfilename(
            title="배경 이미지 선택",
            initialdir=self.last_input_dir,
            filetypes=[
                ("이미지 파일", "*.png *.jpg *.jpeg"),
                ("모든 파일", "*.*")
            ]
        )
        if file_path:
            try:
                # 이미지 열어서 확인
                img = Image.open(file_path)
                self.background_image_path = file_path
                self.background_image = img

                # 파일명 표시
                filename = os.path.basename(file_path)
                if len(filename) > 30:
                    filename = filename[:27] + "..."
                self.bg_image_label.config(
                    text=f"✓ {filename}",
                    fg="#34C759"
                )

                # 크기 조절 슬라이더와 버튼 활성화
                self.bg_scale_slider.config(state="normal")
                self.bg_fit_btn.config(state="normal")

                # 배경 이미지 선택 시 자동 미리보기
                if self.input_files:
                    self.preview_marketing_image()
                else:
                    self.show_background_preview()

            except Exception as e:
                messagebox.showerror("오류", f"이미지를 열 수 없습니다:\n{str(e)}")

    def fit_background_to_actual_size(self):
        """배경 이미지를 출력 사이즈에 맞춰 실제 크기로 조정"""
        if not self.background_image:
            return

        # 출력 사이즈 업데이트
        self.update_output_size()

        # 배경 이미지 원본 크기
        bg_width = self.background_image.width
        bg_height = self.background_image.height

        # 출력 사이즈에 맞는 비율 계산
        width_ratio = self.output_width / bg_width
        height_ratio = self.output_height / bg_height

        # 둘 중 큰 비율을 선택 (출력 사이즈를 완전히 채우도록)
        scale_ratio = max(width_ratio, height_ratio)

        # 백분율로 변환 (50~200 범위로 제한)
        scale_percent = int(scale_ratio * 100)
        scale_percent = max(50, min(200, scale_percent))

        # 슬라이더 업데이트
        self.bg_scale_slider.set(scale_percent)
        self.bg_scale_label.config(text=f"{scale_percent}%")
        self.bg_image_scale = scale_percent / 100.0

        # 미리보기 업데이트
        if self.input_files:
            self.preview_marketing_image()
        else:
            self.show_background_preview()

    def on_bg_scale_change(self, value):
        """배경 이미지 크기 슬라이더 변경"""
        scale_percent = int(float(value))
        self.bg_scale_label.config(text=f"{scale_percent}%")
        self.bg_image_scale = scale_percent / 100.0

        # 배경 이미지가 있으면 미리보기 업데이트
        if self.background_image:
            if self.input_files:
                self.preview_marketing_image()
            else:
                self.show_background_preview()

    def show_background_preview(self):
        """선택한 배경 이미지를 미리보기에 표시 (스케일 적용)"""
        try:
            if self.background_image:
                # 출력 사이즈 업데이트
                self.update_output_size()

                # 배경 이미지 복사 및 원본 비율 계산
                bg_preview = self.background_image.copy()
                original_aspect = bg_preview.width / bg_preview.height

                # 스케일 적용된 크기 계산 (원본 비율 유지)
                base_width = int(self.output_width * self.bg_image_scale)
                base_height = int(base_width / original_aspect)

                # 배경 이미지를 스케일 적용하여 리사이즈 (원본 비율 유지)
                bg_preview = bg_preview.resize(
                    (base_width, base_height),
                    Image.Resampling.LANCZOS
                )

                # 타겟 크기의 캔버스 생성
                canvas = Image.new('RGB', (self.output_width, self.output_height), (0, 0, 0))

                # 배경 이미지가 캔버스보다 크면 중앙 기준으로 크롭
                if bg_preview.width > self.output_width or bg_preview.height > self.output_height:
                    # 이미지 중앙에서 캔버스 크기만큼 크롭
                    left = (bg_preview.width - self.output_width) // 2
                    top = (bg_preview.height - self.output_height) // 2
                    right = left + self.output_width
                    bottom = top + self.output_height

                    # 음수 방지
                    left = max(0, left)
                    top = max(0, top)
                    right = min(bg_preview.width, right)
                    bottom = min(bg_preview.height, bottom)

                    bg_preview = bg_preview.crop((left, top, right, bottom))
                    # 크롭된 이미지를 중앙에 배치
                    x = (self.output_width - bg_preview.width) // 2
                    y = (self.output_height - bg_preview.height) // 2
                else:
                    # 이미지가 작으면 중앙에 배치
                    x = (self.output_width - bg_preview.width) // 2
                    y = (self.output_height - bg_preview.height) // 2

                canvas.paste(bg_preview, (x, y))

                # 미리보기 크기로 축소
                max_size = (400, 600)
                canvas.thumbnail(max_size, Image.Resampling.LANCZOS)

                # PhotoImage로 변환
                photo = ImageTk.PhotoImage(canvas)

                # 레이블 업데이트
                self.preview_label.config(image=photo, text="")
                self.preview_label.image = photo  # 참조 유지

        except Exception as e:
            print(f"배경 이미지 미리보기 오류: {e}")
    
    def toggle_text_options(self):
        """텍스트 옵션 활성화/비활성화"""
        if self.text_var.get():
            self.text_entry.config(state="normal")
            self.text_size_spinner.config(state="normal")
            self.text_color_btn.config(state="normal")
        else:
            self.text_entry.config(state="disabled")
            self.text_size_spinner.config(state="disabled")
            self.text_color_btn.config(state="disabled")

    def choose_text_color(self):
        """텍스트 색상 선택"""
        from tkinter import colorchooser

        # 색상 선택 다이얼로그 표시
        color = colorchooser.askcolor(
            color='#%02x%02x%02x' % self.text_color,
            title="텍스트 색상 선택"
        )

        if color[0]:  # 사용자가 색상을 선택한 경우
            # RGB 값 저장
            self.text_color = tuple(int(c) for c in color[0])
            # 버튼 배경색 업데이트
            self.text_color_btn.config(bg='#%02x%02x%02x' % self.text_color)

            # 미리보기 업데이트
            if self.input_files:
                self.preview_marketing_image()

    def show_preview(self, image_path):
        """이미지 미리보기 표시"""
        try:
            # 이미지 열기
            img = Image.open(image_path)

            # 미리보기 크기로 조정 (비율 유지)
            max_size = (400, 600)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # PhotoImage로 변환
            photo = ImageTk.PhotoImage(img)

            # 레이블 업데이트
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo  # 참조 유지

        except Exception as e:
            self.preview_label.config(
                text=f"미리보기 오류:\n{str(e)}",
                image=""
            )

    def create_background(self, background_style):
        """배경 생성 헬퍼 함수 - 항상 배경 레이어"""
        # 출력 사이즈 업데이트
        self.update_output_size()

        if background_style == 'gradient_blue':
            return self.generator.create_gradient_background(
                self.output_width,
                self.output_height
            )
        elif background_style == 'image':
            if not self.background_image:
                messagebox.showwarning("경고", "배경 이미지를 먼저 선택해주세요!")
                return Image.new('RGB', (self.output_width, self.output_height), (255, 255, 255))

            # 배경 이미지를 스케일 적용하여 리사이즈 (원본 비율 유지)
            bg_img = self.background_image.copy()

            # 원본 비율 계산
            original_aspect = bg_img.width / bg_img.height

            # 스케일 적용된 크기 계산 (원본 비율 유지)
            base_width = int(self.output_width * self.bg_image_scale)
            base_height = int(base_width / original_aspect)

            # 이미지 리사이즈 (원본 비율 유지)
            bg_img = bg_img.resize(
                (base_width, base_height),
                Image.Resampling.LANCZOS
            )

            # 타겟 크기의 캔버스 생성 (배경)
            canvas = Image.new('RGB', (self.output_width, self.output_height), (0, 0, 0))

            # 배경 이미지가 캔버스보다 크면 중앙 기준으로 크롭
            if bg_img.width > self.output_width or bg_img.height > self.output_height:
                # 이미지 중앙에서 캔버스 크기만큼 크롭
                left = (bg_img.width - self.output_width) // 2
                top = (bg_img.height - self.output_height) // 2
                right = left + self.output_width
                bottom = top + self.output_height

                # 음수 방지
                left = max(0, left)
                top = max(0, top)
                right = min(bg_img.width, right)
                bottom = min(bg_img.height, bottom)

                bg_img = bg_img.crop((left, top, right, bottom))
                # 크롭된 이미지를 중앙에 배치
                x = (self.output_width - bg_img.width) // 2
                y = (self.output_height - bg_img.height) // 2
            else:
                # 이미지가 작으면 중앙에 배치
                x = (self.output_width - bg_img.width) // 2
                y = (self.output_height - bg_img.height) // 2

            canvas.paste(bg_img, (x, y))
            return canvas.convert('RGB')
        else:
            bg_color = self.generator.BACKGROUND_COLORS.get(background_style, (255, 255, 255))
            if background_style == "custom":
                bg_color = self.custom_color
            return Image.new('RGB', (self.output_width, self.output_height), bg_color)

    def add_rounded_corners(self, img, radius=60):
        """이미지에 둥근 모서리 추가 (iPhone 스타일)"""
        from PIL import ImageDraw

        # RGBA 모드로 변환
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 둥근 모서리 마스크 생성
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)

        # 둥근 사각형 그리기
        draw.rounded_rectangle(
            [(0, 0), img.size],
            radius=radius,
            fill=255
        )

        # 결과 이미지 생성
        result = Image.new('RGBA', img.size, (0, 0, 0, 0))
        result.paste(img, (0, 0))
        result.putalpha(mask)

        return result

    def add_border_to_image(self, img, border_width=5, border_color=(200, 200, 200)):
        """이미지에 테두리 추가"""
        from PIL import ImageDraw

        img_with_border = img.copy()
        draw = ImageDraw.Draw(img_with_border)

        # 테두리 그리기
        draw.rectangle(
            [0, 0, img.width - 1, img.height - 1],
            outline=border_color,
            width=border_width
        )

        return img_with_border

    def add_text_to_image(self, img, text, position="bottom", font_size=60):
        """이미지에 텍스트 추가"""
        from PIL import ImageDraw, ImageFont

        # 이미지 복사
        img_with_text = img.copy()
        draw = ImageDraw.Draw(img_with_text)

        # 폰트 설정 시도 (San Francisco 우선)
        try:
            # San Francisco 폰트 경로 시도 (macOS)
            font_paths = [
                "/System/Library/Fonts/SF-Pro-Display-Bold.otf",  # macOS SF Pro Display
                "/System/Library/Fonts/SF-Pro-Text-Bold.otf",  # macOS SF Pro Text
                "/System/Library/Fonts/SF-Pro.ttf",  # macOS SF Pro
                "/Library/Fonts/SF-Pro-Display-Bold.otf",  # macOS user fonts
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",  # macOS fallback
                "/Library/Fonts/Arial.ttf",  # macOS fallback
                "C:\\Windows\\Fonts\\arialbd.ttf",  # Windows
                "C:\\Windows\\Fonts\\arial.ttf",  # Windows
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
            ]

            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    break

            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # 텍스트 줄바꿈 처리
        max_width = img_with_text.width - 100  # 좌우 여백 50px씩
        lines = []
        words = text.split(' ')
        current_line = ""

        for word in words:
            test_line = current_line + word + " " if current_line else word + " "
            bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = bbox[2] - bbox[0]

            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                    current_line = word + " "
                else:
                    # 단어가 너무 길면 강제로 추가
                    lines.append(word)
                    current_line = ""

        if current_line:
            lines.append(current_line.strip())

        # 전체 텍스트 높이 계산
        line_height = font_size + 10  # 줄 간격
        total_height = len(lines) * line_height

        # 시작 Y 위치 계산
        if position == "top":
            start_y = 100
        elif position == "center":
            start_y = (img_with_text.height - total_height) // 2
        else:  # bottom
            start_y = img_with_text.height - total_height - 150

        # 각 줄 그리기
        text_color = self.text_color + (255,)  # RGBA 변환
        shadow_color = (0, 0, 0, 128)
        shadow_offset = 3

        for i, line in enumerate(lines):
            # 텍스트 크기 계산 (중앙 정렬용)
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (img_with_text.width - text_width) // 2
            y = start_y + i * line_height

            # 텍스트 그림자 효과
            draw.text((x + shadow_offset, y + shadow_offset), line, font=font, fill=shadow_color)

            # 텍스트 그리기 (선택된 색상)
            draw.text((x, y), line, font=font, fill=text_color)

        return img_with_text

    def preview_marketing_image(self):
        """생성 전 마케팅 이미지 미리보기"""
        if not self.input_files:
            messagebox.showwarning("경고", "먼저 이미지를 선택해주세요.")
            return

        try:
            self.status_label.config(text="미리보기 생성 중...", fg="#FF9500")
            self.root.update()

            # 출력 사이즈 업데이트
            self.update_output_size()

            # 첫 번째 이미지로 미리보기 생성 (메인 이미지)
            screenshot = Image.open(self.input_files[0])

            # 1단계: 배경 레이어 생성 (항상 맨 아래)
            background_style = self.background_var.get()
            background = self.create_background(background_style)

            # 2단계: 메인 스크린샷 크기 조정 (배경 위에 올림)
            # iPhone 17 프레임이 있으면 프레임 크기(90%)에 맞춤, 없으면 80%
            if self.iphone_frame:
                # 프레임 크기(90%)보다 약간 작게 (85%)
                max_width_ratio = 0.85
                max_height_ratio = 0.85
            else:
                max_width_ratio = 0.8
                max_height_ratio = 0.85

            target_screenshot_width = int(self.output_width * max_width_ratio)
            aspect_ratio = screenshot.height / screenshot.width
            target_screenshot_height = int(target_screenshot_width * aspect_ratio)

            if target_screenshot_height > self.output_height * max_height_ratio:
                target_screenshot_height = int(self.output_height * max_height_ratio)
                target_screenshot_width = int(target_screenshot_height / aspect_ratio)

            screenshot_resized = screenshot.resize(
                (target_screenshot_width, target_screenshot_height),
                Image.Resampling.LANCZOS
            )

            # iPhone 17 프레임이 있으면 둥근 모서리 추가
            if self.iphone_frame:
                # 둥근 모서리 반지름 (이미지 크기에 비례) - 15%
                corner_radius = int(min(screenshot_resized.width, screenshot_resized.height) * 0.15)
                screenshot_resized = self.add_rounded_corners(screenshot_resized, radius=corner_radius)

            # 프레임 추가
            if self.frame_var.get():
                screenshot_with_frame = self.generator.add_device_frame(screenshot_resized)
            else:
                screenshot_with_frame = screenshot_resized
                if screenshot_with_frame.mode != 'RGBA':
                    screenshot_with_frame = screenshot_with_frame.convert('RGBA')

            # 3단계: 메인 스크린샷을 배경 위에 합성 (중앙 배치 + 14% 아래로)
            x = (self.output_width - screenshot_with_frame.width) // 2
            y = (self.output_height - screenshot_with_frame.height) // 2
            y = int(y * 0.8)
            # 14% 아래로 이동 (16% - 2%)
            y = y + int(self.output_height * 0.14)

            print(f"[미리보기] 배경 크기: {background.size}, 모드: {background.mode}")
            print(f"[미리보기] 메인 이미지 크기: {screenshot_with_frame.size}, 모드: {screenshot_with_frame.mode}")
            print(f"[미리보기] 메인 이미지 위치: ({x}, {y})")

            # 배경(하위 레이어) + 메인 스크린샷(상위 레이어) 합성
            # RGBA 이미지를 마스크로 사용하여 투명도 적용
            background.paste(screenshot_with_frame, (x, y), screenshot_with_frame)

            # 4단계: 텍스트 추가 (최상위 레이어)
            if self.text_var.get() and self.text_entry.get().strip():
                text = self.text_entry.get().strip()
                position = self.text_position_var.get()
                font_size = self.text_size_var.get()
                background = self.add_text_to_image(background, text, position, font_size)

            # RGB 변환
            final_image = background.convert('RGB')

            # 5단계: iPhone 17 프레임 오버레이 (최최상위 레이어)
            if self.iphone_frame:
                # 프레임을 출력 사이즈의 90%로 리사이즈
                frame_resized = self.iphone_frame.copy()
                frame_width = int(self.output_width * 0.9)
                frame_height = int(self.output_height * 0.9)
                frame_resized = frame_resized.resize(
                    (frame_width, frame_height),
                    Image.Resampling.LANCZOS
                )
                # RGBA로 변환
                if frame_resized.mode != 'RGBA':
                    frame_resized = frame_resized.convert('RGBA')

                # 중앙에 배치 + 13% 아래로 이동
                x_offset = (self.output_width - frame_width) // 2
                y_offset = (self.output_height - frame_height) // 2
                y_offset = y_offset + int(self.output_height * 0.13)

                # 최종 이미지를 RGBA로 변환하여 프레임 합성
                final_image_rgba = final_image.convert('RGBA')
                final_image_rgba.paste(frame_resized, (x_offset, y_offset), frame_resized)
                final_image = final_image_rgba.convert('RGB')

            # 테두리 추가
            if self.border_var.get():
                final_image = self.add_border_to_image(final_image, border_width=5, border_color=(150, 150, 150))

            # 미리보기 표시
            preview_img = final_image.copy()
            max_size = (400, 600)
            preview_img.thumbnail(max_size, Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(preview_img)
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo

            self.status_label.config(text="✓ 미리보기 생성 완료", fg="#34C759")

        except Exception as e:
            messagebox.showerror("오류", f"미리보기 생성 중 오류가 발생했습니다:\n{str(e)}")
            self.status_label.config(text="미리보기 생성 실패", fg="red")
            import traceback
            traceback.print_exc()
    
    def generate_images(self):
        if not self.input_files:
            messagebox.showwarning("경고", "먼저 이미지를 선택해주세요.")
            return

        # 출력 폴더 선택
        output_dir = filedialog.askdirectory(
            title="저장 폴더 선택",
            initialdir=self.last_output_dir
        )
        if not output_dir:
            return

        # 선택한 출력 폴더를 저장
        self.last_output_dir = output_dir
        
        self.status_label.config(text="생성 중...", fg="#FF9500")
        self.root.update()
        
        success_count = 0
        background = self.background_var.get()
        add_frame = self.frame_var.get()
        
        # 커스텀 배경인 경우 generator에 색상 설정
        if background == "custom":
            self.generator.background_color = self.custom_color
        
        for i, input_file in enumerate(self.input_files, 1):
            filename = os.path.basename(input_file)
            output_filename = f"marketing_{os.path.splitext(filename)[0]}.png"
            output_path = os.path.join(output_dir, output_filename)

            self.status_label.config(
                text=f"처리 중... ({i}/{len(self.input_files)})",
                fg="#FF9500"
            )
            self.root.update()

            try:
                # 출력 사이즈 업데이트
                self.update_output_size()

                # 메인 스크린샷 열기
                screenshot = Image.open(input_file)

                # 1단계: 배경 레이어 생성 (항상 맨 아래)
                img_background = self.create_background(background)

                # 2단계: 메인 스크린샷 크기 조정 (배경 위에 올림)
                # iPhone 17 프레임이 있으면 프레임 크기(90%)에 맞춤, 없으면 80%
                if self.iphone_frame:
                    # 프레임 크기(90%)보다 약간 작게 (85%)
                    max_width_ratio = 0.85
                    max_height_ratio = 0.85
                else:
                    max_width_ratio = 0.8
                    max_height_ratio = 0.85

                target_screenshot_width = int(self.output_width * max_width_ratio)
                aspect_ratio = screenshot.height / screenshot.width
                target_screenshot_height = int(target_screenshot_width * aspect_ratio)

                if target_screenshot_height > self.output_height * max_height_ratio:
                    target_screenshot_height = int(self.output_height * max_height_ratio)
                    target_screenshot_width = int(target_screenshot_height / aspect_ratio)

                screenshot_resized = screenshot.resize(
                    (target_screenshot_width, target_screenshot_height),
                    Image.Resampling.LANCZOS
                )

                # iPhone 17 프레임이 있으면 둥근 모서리 추가
                if self.iphone_frame:
                    # 둥근 모서리 반지름 (이미지 크기에 비례) - 15%
                    corner_radius = int(min(screenshot_resized.width, screenshot_resized.height) * 0.15)
                    screenshot_resized = self.add_rounded_corners(screenshot_resized, radius=corner_radius)

                # 프레임 추가
                if add_frame:
                    screenshot_with_frame = self.generator.add_device_frame(screenshot_resized)
                else:
                    screenshot_with_frame = screenshot_resized
                    if screenshot_with_frame.mode != 'RGBA':
                        screenshot_with_frame = screenshot_with_frame.convert('RGBA')

                # 3단계: 메인 스크린샷을 배경 위에 합성 (중앙 배치 + 14% 아래로)
                x = (self.output_width - screenshot_with_frame.width) // 2
                y = (self.output_height - screenshot_with_frame.height) // 2
                y = int(y * 0.8)
                # 14% 아래로 이동 (16% - 2%)
                y = y + int(self.output_height * 0.14)

                # 배경(하위 레이어) + 메인 스크린샷(상위 레이어) 합성
                img_background.paste(screenshot_with_frame, (x, y), screenshot_with_frame)

                # 4단계: 텍스트 추가 (최상위 레이어)
                if self.text_var.get() and self.text_entry.get().strip():
                    text = self.text_entry.get().strip()
                    position = self.text_position_var.get()
                    font_size = self.text_size_var.get()
                    img_background = self.add_text_to_image(img_background, text, position, font_size)

                # RGB 변환
                final_image = img_background.convert('RGB')

                # 5단계: iPhone 17 프레임 오버레이 (최최상위 레이어)
                if self.iphone_frame:
                    # 프레임을 출력 사이즈의 90%로 리사이즈
                    frame_resized = self.iphone_frame.copy()
                    frame_width = int(self.output_width * 0.9)
                    frame_height = int(self.output_height * 0.9)
                    frame_resized = frame_resized.resize(
                        (frame_width, frame_height),
                        Image.Resampling.LANCZOS
                    )
                    # RGBA로 변환
                    if frame_resized.mode != 'RGBA':
                        frame_resized = frame_resized.convert('RGBA')

                    # 중앙에 배치 + 13% 아래로 이동
                    x_offset = (self.output_width - frame_width) // 2
                    y_offset = (self.output_height - frame_height) // 2
                    y_offset = y_offset + int(self.output_height * 0.13)

                    # 최종 이미지를 RGBA로 변환하여 프레임 합성
                    final_image_rgba = final_image.convert('RGBA')
                    final_image_rgba.paste(frame_resized, (x_offset, y_offset), frame_resized)
                    final_image = final_image_rgba.convert('RGB')

                # 테두리 추가
                if self.border_var.get():
                    final_image = self.add_border_to_image(final_image, border_width=5, border_color=(150, 150, 150))

                # 저장
                final_image.save(output_path, 'PNG', quality=95)
                success_count += 1

            except Exception as e:
                print(f"오류 발생 ({filename}): {e}")
                import traceback
                traceback.print_exc()
        
        self.status_label.config(
            text=f"✓ 완료! {success_count}/{len(self.input_files)}개 성공",
            fg="#34C759"
        )
        
        messagebox.showinfo(
            "완료",
            f"{success_count}개의 마케팅 이미지가 생성되었습니다!\n\n저장 위치: {output_dir}"
        )
        
        # 생성된 첫 번째 이미지 미리보기
        if success_count > 0:
            first_output = os.path.join(output_dir, f"marketing_{os.path.splitext(os.path.basename(self.input_files[0]))[0]}.png")
            if os.path.exists(first_output):
                self.show_preview(first_output)


def main():
    try:
        root = TkinterDnD.Tk()
    except:
        # tkinterdnd2가 없으면 일반 Tk 사용
        root = tk.Tk()
        print("알림: 드래그 앤 드롭 기능을 사용하려면 'pip install tkinterdnd2'를 실행하세요.")
    
    app = EnhancedMarketingImageGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
