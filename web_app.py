#!/usr/bin/env python3
"""
iOS Marketing Image Generator - Web Interface
Flask 기반 웹 인터페이스
"""

from flask import Flask, render_template, request, send_file, jsonify, url_for
from werkzeug.utils import secure_filename
import os
import tempfile
import shutil
from datetime import datetime
from generator import MarketingImageGenerator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB 제한
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['OUTPUT_FOLDER'] = tempfile.mkdtemp()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

generator = MarketingImageGenerator()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': '파일이 없습니다'}), 400
    
    files = request.files.getlist('files[]')
    background = request.form.get('background', 'white')
    add_frame = request.form.get('add_frame', 'true') == 'true'
    
    if not files:
        return jsonify({'error': '파일을 선택해주세요'}), 400
    
    output_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            # 파일 저장
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # 마케팅 이미지 생성
            output_filename = f"marketing_{os.path.splitext(filename)[0]}.png"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            try:
                if generator.generate_marketing_image(input_path, output_path, add_frame, background):
                    output_files.append({
                        'original': filename,
                        'output': output_filename,
                        'url': url_for('download_file', filename=output_filename)
                    })
            except Exception as e:
                print(f"오류: {e}")
    
    if output_files:
        return jsonify({
            'success': True,
            'files': output_files,
            'message': f'{len(output_files)}개의 이미지가 생성되었습니다'
        })
    else:
        return jsonify({'error': '이미지 생성에 실패했습니다'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(app.config['OUTPUT_FOLDER'], filename),
        as_attachment=True,
        download_name=filename
    )

@app.route('/preview/<filename>')
def preview_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))

@app.route('/cleanup', methods=['POST'])
def cleanup():
    """임시 파일 정리"""
    try:
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                try:
                    os.remove(file_path)
                except:
                    pass
        return jsonify({'success': True})
    except:
        return jsonify({'error': '정리 실패'}), 500

def create_templates():
    """HTML 템플릿 생성"""
    template_dir = 'templates'
    os.makedirs(template_dir, exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iOS Marketing Image Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .upload-area {
            border: 3px dashed #007AFF;
            border-radius: 15px;
            padding: 60px 40px;
            text-align: center;
            background: #f8f9ff;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 30px;
        }
        
        .upload-area:hover {
            background: #f0f2ff;
            border-color: #5856D6;
        }
        
        .upload-area.dragover {
            background: #e8ebff;
            border-color: #5856D6;
            transform: scale(1.02);
        }
        
        .upload-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .upload-text {
            font-size: 1.2em;
            color: #333;
            margin-bottom: 10px;
        }
        
        .upload-subtext {
            color: #666;
            font-size: 0.9em;
        }
        
        .options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .option-group {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }
        
        .option-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }
        
        .option-group select {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            background: white;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        
        .generate-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
        }
        
        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(52, 199, 89, 0.4);
        }
        
        .generate-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .status {
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
        }
        
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
        }
        
        .results {
            display: none;
            margin-top: 30px;
        }
        
        .results h3 {
            margin-bottom: 20px;
            color: #333;
        }
        
        .result-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .result-item {
            background: #f8f9fa;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .result-item:hover {
            transform: translateY(-5px);
        }
        
        .result-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }
        
        .result-info {
            padding: 15px;
        }
        
        .result-name {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .download-btn {
            width: 100%;
            padding: 10px;
            background: #007AFF;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }
        
        .download-btn:hover {
            background: #0051D5;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 30px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #007AFF;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        input[type="file"] {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 iOS Marketing Image Generator</h1>
            <p>iPhone 14 Pro 스크린샷을 1290x2796 마케팅 이미지로 변환</p>
        </div>
        
        <div class="content">
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📤</div>
                <div class="upload-text">이미지를 드래그하거나 클릭하여 선택</div>
                <div class="upload-subtext">PNG, JPG, JPEG 지원 (최대 50MB)</div>
                <input type="file" id="fileInput" multiple accept=".png,.jpg,.jpeg">
            </div>
            
            <div class="options">
                <div class="option-group">
                    <label>배경 스타일</label>
                    <select id="background">
                        <option value="white">흰색</option>
                        <option value="black">검정색</option>
                        <option value="gradient_blue">파란색 그라디언트</option>
                        <option value="app_store_gray">App Store 회색</option>
                    </select>
                </div>
                
                <div class="option-group">
                    <label>효과</label>
                    <div class="checkbox-group">
                        <input type="checkbox" id="addFrame" checked>
                        <label for="addFrame" style="margin: 0;">그림자/프레임 추가</label>
                    </div>
                </div>
            </div>
            
            <button class="generate-btn" id="generateBtn" disabled>
                🎨 마케팅 이미지 생성
            </button>
            
            <div class="status" id="status"></div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <div>이미지 생성 중...</div>
            </div>
            
            <div class="results" id="results">
                <h3>✅ 생성된 이미지</h3>
                <div class="result-grid" id="resultGrid"></div>
            </div>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const generateBtn = document.getElementById('generateBtn');
        const status = document.getElementById('status');
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');
        const resultGrid = document.getElementById('resultGrid');
        
        let selectedFiles = [];
        
        // 클릭으로 파일 선택
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // 파일 선택 처리
        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });
        
        // 드래그 앤 드롭
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });
        
        function handleFiles(files) {
            selectedFiles = Array.from(files).filter(file => 
                file.type.match('image/(png|jpeg|jpg)')
            );
            
            if (selectedFiles.length > 0) {
                uploadArea.querySelector('.upload-text').textContent = 
                    `✓ ${selectedFiles.length}개 파일 선택됨`;
                generateBtn.disabled = false;
                showStatus('info', `${selectedFiles.length}개의 이미지가 선택되었습니다.`);
            } else {
                showStatus('error', '유효한 이미지 파일을 선택해주세요.');
            }
        }
        
        generateBtn.addEventListener('click', async () => {
            if (selectedFiles.length === 0) return;
            
            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('files[]', file);
            });
            
            formData.append('background', document.getElementById('background').value);
            formData.append('add_frame', document.getElementById('addFrame').checked);
            
            // UI 업데이트
            generateBtn.disabled = true;
            loading.style.display = 'block';
            results.style.display = 'none';
            status.style.display = 'none';
            
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                loading.style.display = 'none';
                
                if (data.success) {
                    showStatus('success', data.message);
                    displayResults(data.files);
                } else {
                    showStatus('error', data.error || '이미지 생성에 실패했습니다.');
                }
            } catch (error) {
                loading.style.display = 'none';
                showStatus('error', '서버 오류가 발생했습니다.');
                console.error(error);
            } finally {
                generateBtn.disabled = false;
            }
        });
        
        function showStatus(type, message) {
            status.className = `status ${type}`;
            status.textContent = message;
            status.style.display = 'block';
        }
        
        function displayResults(files) {
            resultGrid.innerHTML = '';
            results.style.display = 'block';
            
            files.forEach(file => {
                const item = document.createElement('div');
                item.className = 'result-item';
                item.innerHTML = `
                    <img src="/preview/${file.output}" alt="${file.original}" class="result-image">
                    <div class="result-info">
                        <div class="result-name">${file.output}</div>
                        <a href="${file.url}" download>
                            <button class="download-btn">⬇️ 다운로드</button>
                        </a>
                    </div>
                `;
                resultGrid.appendChild(item);
            });
        }
    </script>
</body>
</html>'''
    
    with open(os.path.join(template_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    create_templates()
    print("=" * 60)
    print("🚀 iOS Marketing Image Generator - Web Server")
    print("=" * 60)
    print("서버 주소: http://localhost:5000")
    print("브라우저에서 위 주소로 접속하세요!")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
