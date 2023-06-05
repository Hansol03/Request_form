from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import openpyxl

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    html_content = """
    <h1>양식 작성</h1>
    <form method="post" enctype="multipart/form-data" action="/submit">
        <label for="width">가로 길이:</label>
        <input type="text" name="width" id="width"><br>

        <label for="height">세로 길이:</label>
        <input type="text" name="height" id="height"><br>

        <label for="depth">높이:</label>
        <input type="text" name="depth" id="depth"><br>

        <label for="weight">파트 무게:</label>
        <input type="text" name="weight" id="weight"><br>

        <label for="material">소재:</label>
        <input type="text" name="material" id="material"><br>

        <label for="purpose">용도:</label>
        <input type="text" name="purpose" id="purpose"><br>

        <label for="image">사진 첨부:</label>
        <input type="file" name="image" id="image"><br>

        <input type="submit" value="제출">
    </form>
    """
    return html_content

@app.route('/submit', methods=['POST'])
def submit():
    width = request.form.get('width')
    height = request.form.get('height')
    depth = request.form.get('depth')
    weight = request.form.get('weight')
    material = request.form.get('material')
    purpose = request.form.get('purpose')
    image = request.files['image']

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Create Excel file and write data
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet['A1'] = 'Width'
        sheet['B1'] = 'Height'
        sheet['C1'] = 'Depth'
        sheet['D1'] = 'Weight'
        sheet['E1'] = 'Material'
        sheet['F1'] = 'Purpose'
        sheet['G1'] = 'Image Filename'
        sheet['A2'] = width
        sheet['B2'] = height
        sheet['C2'] = depth
        sheet['D2'] = weight
        sheet['E2'] = material
        sheet['F2'] = purpose
        sheet['G2'] = filename

        excel_filename = f"{filename}.xlsx"
        wb.save(os.path.join(app.config['UPLOAD_FOLDER'], excel_filename))

        return jsonify({'message': '양식이 제출되었습니다.'})
    else:
        return jsonify({'error': '올바른 이미지 파일을 첨부해야 합니다.'})

@app.route('/uploads')
def list_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
