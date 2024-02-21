from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        image_path = request.files['image_path']
        if 'image_path' not in request.files:
            return render_template('home.html', message='No file part')
        if image_path.filename == '':
            return render_template('home.html', message='No selected file')
    return render_template('home.html')


if __name__ == '__main__':
  app.run(debug=True)
