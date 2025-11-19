#!/usr/bin/env python3
"""
iOS Marketing Image Generator - GUI Version
간단한 GUI로 마케팅 이미지 생성
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from generator import MarketingImageGenerator

class MarketingImageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("iOS Marketing Image Generator")
        self.root.geometry("600x400")
        
        self.generator = MarketingImageGenerator()
        self.input_files = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # 제목
        title_label = tk.Label(
            self.root, 
            text="iOS Marketing Image Generator",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)
        
        # 설명
        desc_label = tk.Label(
            self.root,
            text="iPhone 14 Pro 스크린샷을 1290x2796 마케팅 이미지로 변환",
            font=("Arial", 10)
        )
        desc_label.pack(pady=5)
        
        # 파일 선택 프레임
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Button(
            file_frame,
            text="📁 이미지 선택",
            command=self.select_files,
            width=15,
            height=2
        ).pack(side="left", padx=5)
        
        tk.Button(
            file_frame,
            text="📂 폴더 선택",
            command=self.select_folder,
            width=15,
            height=2
        ).pack(side="left", padx=5)
        
        # 선택된 파일 표시
        self.file_label = tk.Label(
            self.root,
            text="선택된 파일 없음",
            fg="gray"
        )
        self.file_label.pack(pady=10)
        
        # 옵션 프레임
        options_frame = tk.LabelFrame(self.root, text="옵션", padx=10, pady=10)
        options_frame.pack(pady=10, padx=20, fill="x")
        
        # 배경 스타일
        tk.Label(options_frame, text="배경 스타일:").grid(row=0, column=0, sticky="w", pady=5)
        self.background_var = tk.StringVar(value="white")
        background_combo = ttk.Combobox(
            options_frame,
            textvariable=self.background_var,
            values=["white", "black", "gradient_blue", "app_store_gray"],
            state="readonly",
            width=20
        )
        background_combo.grid(row=0, column=1, sticky="w", pady=5)
        
        # 프레임 옵션
        self.frame_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="그림자/프레임 효과 추가",
            variable=self.frame_var
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        
        # 생성 버튼
        generate_btn = tk.Button(
            self.root,
            text="🎨 마케팅 이미지 생성",
            command=self.generate_images,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2
        )
        generate_btn.pack(pady=20)
        
        # 상태 표시
        self.status_label = tk.Label(
            self.root,
            text="",
            fg="blue"
        )
        self.status_label.pack(pady=5)
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="스크린샷 선택",
            filetypes=[
                ("이미지 파일", "*.png *.jpg *.jpeg"),
                ("모든 파일", "*.*")
            ]
        )
        if files:
            self.input_files = list(files)
            self.file_label.config(
                text=f"{len(files)}개 파일 선택됨",
                fg="green"
            )
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="스크린샷 폴더 선택")
        if folder:
            supported_formats = ('.png', '.jpg', '.jpeg')
            files = [
                os.path.join(folder, f) 
                for f in os.listdir(folder) 
                if f.lower().endswith(supported_formats)
            ]
            if files:
                self.input_files = files
                self.file_label.config(
                    text=f"{len(files)}개 파일 선택됨",
                    fg="green"
                )
            else:
                messagebox.showwarning("경고", "이미지 파일을 찾을 수 없습니다.")
    
    def generate_images(self):
        if not self.input_files:
            messagebox.showwarning("경고", "먼저 이미지를 선택해주세요.")
            return
        
        # 출력 폴더 선택
        output_dir = filedialog.askdirectory(title="저장 폴더 선택")
        if not output_dir:
            return
        
        self.status_label.config(text="생성 중...", fg="blue")
        self.root.update()
        
        success_count = 0
        background = self.background_var.get()
        add_frame = self.frame_var.get()
        
        for i, input_file in enumerate(self.input_files, 1):
            filename = os.path.basename(input_file)
            output_filename = f"marketing_{os.path.splitext(filename)[0]}.png"
            output_path = os.path.join(output_dir, output_filename)
            
            self.status_label.config(
                text=f"처리 중... ({i}/{len(self.input_files)})",
                fg="blue"
            )
            self.root.update()
            
            if self.generator.generate_marketing_image(
                input_file, output_path, add_frame, background
            ):
                success_count += 1
        
        self.status_label.config(
            text=f"완료! {success_count}/{len(self.input_files)}개 성공",
            fg="green"
        )
        
        messagebox.showinfo(
            "완료",
            f"{success_count}개의 마케팅 이미지가 생성되었습니다!\n\n저장 위치: {output_dir}"
        )


def main():
    root = tk.Tk()
    app = MarketingImageGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
