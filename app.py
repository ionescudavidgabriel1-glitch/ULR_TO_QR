from flask import Flask, render_template, request, send_file
from URL_TO_QR import generate_qr_code
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    url = data.get('url', '').strip()
    ec_level = data.get('ec_level', 'L')
    
    if not url:
        return {"error": "URL is required"}, 400

    try:
        # Run your Python logic and get the image in memory
        img_buffer = generate_qr_code(url, ec_level)
        return send_file(img_buffer, mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)