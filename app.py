from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import io
import base64

app = Flask(__name__)

def original(image):
    return image

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def invert(image):
    return cv2.bitwise_not(image)

def pencil_sketch(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_gray = cv2.bitwise_not(gray_image)
    blurred_image = cv2.GaussianBlur(inverted_gray, (21, 21), 0)
    inverted_blurred = cv2.bitwise_not(blurred_image)
    return cv2.divide(inverted_gray, blurred_image, scale=256.0)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        image_stream1 = io.BytesIO(file.read())
        image_stream1.seek(0)
        image_np = np.frombuffer(image_stream1.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
        image_stream = original(image)
        grayscale_image = grayscale(image)
        inverted_image = invert(grayscale_image)
        pencil_sketch_image = pencil_sketch(image)

        # Convert images to base64 strings
        image_stream_base64 = base64.b64encode(cv2.imencode('.jpg', image_stream)[1]).decode()
        grayscale_base64 = base64.b64encode(cv2.imencode('.jpg', grayscale_image)[1]).decode()
        inverted_base64 = base64.b64encode(cv2.imencode('.jpg', inverted_image)[1]).decode()
        pencil_sketch_base64 = base64.b64encode(cv2.imencode('.jpg', pencil_sketch_image)[1]).decode()

        return {
            'original': image_stream_base64,
            'grayscale': grayscale_base64,
            'inverted': inverted_base64,
            'pencil_sketch': pencil_sketch_base64
        }

if __name__ == '__main__':
    app.run(debug=True)
