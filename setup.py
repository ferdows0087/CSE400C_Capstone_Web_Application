import os

def create_project_structure():
    # Create templates directory
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create index.html template
    index_html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Classification</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            padding: 40px;
            max-width: 500px;
            width: 100%;
            text-align: center;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.2em;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .upload-area {
            border: 2px dashed #ddd;
            border-radius: 10px;
            padding: 40px 20px;
            margin-bottom: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #fafafa;
        }
        
        .upload-area:hover {
            border-color: #667eea;
            background: #f0f4ff;
        }
        
        .upload-area.highlight {
            border-color: #667eea;
            background: #f0f4ff;
        }
        
        .upload-icon {
            font-size: 48px;
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .upload-text {
            color: #666;
            margin-bottom: 15px;
        }
        
        #file-input {
            display: none;
        }
        
        .browse-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: background 0.3s ease;
        }
        
        .browse-btn:hover {
            background: #5a6fd8;
        }
        
        .preview-container {
            margin-bottom: 20px;
            display: none;
        }
        
        #image-preview {
            max-width: 100%;
            max-height: 300px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .predict-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.1em;
            transition: background 0.3s ease;
            display: none;
            margin: 0 auto;
        }
        
        .predict-btn:hover {
            background: #218838;
        }
        
        .predict-btn:disabled {
            background: #6c757d;
            cursor: not-allowed;
        }
        
        .results {
            margin-top: 30px;
            padding: 20px;
            border-radius: 10px;
            background: #f8f9fa;
            display: none;
        }
        
        .result-title {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .prediction {
            font-size: 1.4em;
            font-weight: bold;
            color: #28a745;
            margin-bottom: 10px;
        }
        
        .confidence {
            font-size: 1.1em;
            color: #666;
        }
        
        .error {
            color: #dc3545;
            background: #f8d7da;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
        
        .loading {
            display: none;
            margin: 20px 0;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Image Classification</h1>
        <p class="subtitle">Upload an image to classify using our AI model</p>
        
        <div class="upload-area" id="upload-area">
            <div class="upload-icon">📁</div>
            <p class="upload-text">Drag & drop your image here or click to browse</p>
            <button class="browse-btn" onclick="document.getElementById('file-input').click()">
                Browse Files
            </button>
            <input type="file" id="file-input" accept="image/*">
        </div>
        
        <div class="preview-container" id="preview-container">
            <img id="image-preview" alt="Image preview">
        </div>
        
        <button class="predict-btn" id="predict-btn" onclick="predictImage()">
            Predict Image
        </button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyzing image...</p>
        </div>
        
        <div class="results" id="results">
            <h3 class="result-title">Prediction Result</h3>
            <div class="prediction" id="prediction-text"></div>
            <div class="confidence" id="confidence-text"></div>
        </div>
        
        <div class="error" id="error-message"></div>
    </div>

    <script>
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        const previewContainer = document.getElementById('preview-container');
        const imagePreview = document.getElementById('image-preview');
        const predictBtn = document.getElementById('predict-btn');
        const results = document.getElementById('results');
        const predictionText = document.getElementById('prediction-text');
        const confidenceText = document.getElementById('confidence-text');
        const errorMessage = document.getElementById('error-message');
        const loading = document.getElementById('loading');
        
        let currentFile = null;
        
        // Drag and drop functionality
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            uploadArea.classList.add('highlight');
        }
        
        function unhighlight() {
            uploadArea.classList.remove('highlight');
        }
        
        uploadArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }
        
        fileInput.addEventListener('change', function() {
            handleFiles(this.files);
        });
        
        function handleFiles(files) {
            if (files.length > 0) {
                const file = files[0];
                if (file.type.startsWith('image/')) {
                    currentFile = file;
                    showPreview(file);
                    hideError();
                    hideResults();
                    predictBtn.style.display = 'block';
                } else {
                    showError('Please select a valid image file.');
                }
            }
        }
        
        function showPreview(file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewContainer.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
        
        function predictImage() {
            if (!currentFile) {
                showError('Please select an image first.');
                return;
            }
            
            const formData = new FormData();
            formData.append('image', currentFile);
            
            showLoading();
            hideError();
            hideResults();
            predictBtn.disabled = true;
            
            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                predictBtn.disabled = false;
                
                if (data.error) {
                    showError(data.error);
                } else {
                    showResults(data.prediction, data.confidence);
                }
            })
            .catch(error => {
                hideLoading();
                predictBtn.disabled = false;
                showError('Network error: ' + error.message);
            });
        }
        
        function showLoading() {
            loading.style.display = 'block';
        }
        
        function hideLoading() {
            loading.style.display = 'none';
        }
        
        function showResults(prediction, confidence) {
            predictionText.textContent = prediction;
            confidenceText.textContent = `Confidence: ${(confidence * 100).toFixed(2)}%`;
            results.style.display = 'block';
        }
        
        function hideResults() {
            results.style.display = 'none';
        }
        
        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
        }
        
        function hideError() {
            errorMessage.style.display = 'none';
        }
        
        // Click on upload area to trigger file input
        uploadArea.addEventListener('click', function(e) {
            if (e.target !== this.querySelector('.browse-btn')) {
                fileInput.click();
            }
        });
    </script>
</body>
</html>'''
    
    index_html_path = os.path.join(templates_dir, 'index.html')
    with open(index_html_path, 'w', encoding='utf-8') as f:
        f.write(index_html_content)
    
    print("Project structure created successfully!")
    print(f"Template created at: {index_html_path}")

if __name__ == "__main__":
    create_project_structure()