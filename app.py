from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from PIL import Image

# app = Flask(__name__, static_folder='uploads')
app = Flask(__name__)
os.makedirs('uploads', exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():

    # if 'file' not in request.files:
    #     return 'No file part'
    # file = request.files['file']
    # print(file)  # <FileStorage: '特実_国内文献.csv' ('text/csv')>
    file = request.files.get('file')
    print(file)
    # print(file.filename.endswith('.csv'))
    return render_template('index2.html')

    if file and file.filename.endswith('.csv'):
        # CSVファイルを適切なディレクトリに保存する処理
        # file.save(os.path.join('files', file.filename))
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        return render_template('index.html')
        # return render_template('index2.html', file_path=file_path)
        # return render_template('index2.html')
        # return redirect(url_for('index'))
    else:
        return 'Please select a CSV file.'
    # if 'file' not in request.files:
    #     return jsonify({'error': 'No file uploaded'})

    # file = request.files['file']
    # if file.filename == '':
    #     return jsonify({'error': 'No file selected'})

    # if file.type != 'text/csv':
    #     return jsonify({'error': 'Invalid file type'})

    # Read the CSV file
    # df = pd.read_csv(file.stream)

    # Process and analyze the CSV data(df variable)
    # ...

    # Prepare response data
    # response_data = {
    #     'message': 'CSV uploaded and analyzed successfully',
    #     'data': processed_data  # Replace with processed data
    # }

    # return render_template('index.html')
    # return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
