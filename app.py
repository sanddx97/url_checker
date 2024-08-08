from flask import Flask, request, render_template, redirect, url_for
import os
import json
from monitor import start_monitoring

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        smtp_settings = {
            'smtp_server': request.form['smtp_server'],
            'smtp_port': request.form['smtp_port'],
            'smtp_user': request.form['smtp_user'],
            'smtp_password': request.form['smtp_password'],
            'from_email': request.form['from_email'],
            'to_email': request.form['to_email']
        }

        file = request.files['urls_file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'urls.txt')
            file.save(file_path)

            with open('smtp_settings.json', 'w') as f:
                json.dump(smtp_settings, f)

            start_monitoring(file_path, smtp_settings)

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
