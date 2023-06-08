from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import openpyxl

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'stl', 'step', 'stp', 'f3d', 'obj'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    html_content = """
<html>
<head>
  <title>Form</title>
  <style>
    /* 전체 body 스타일 */
    body {
      font-family: Arial, sans-serif;
      background-color: #f2f2f2;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 140vh;
    }

    /* 폼 컨테이너 스타일 */
    .form-container {
      width: 500px;
      padding: 30px;
      background-color: #f9f9f9;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* 제목 스타일 */
    h1 {
      color: #333;
      font-size: 24px;
      margin-bottom: 30px;
      text-align: center;
    }

    /* 입력 필드 스타일 */
    label {
      display: block;
      margin-top: 20px;
      font-weight: bold;
      color: #555;
    }

    input[type="text"],
    input[type="file"] {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
      margin-top: 5px;
      font-family: Arial, sans-serif;
    }

    /* 제출 버튼 스타일 */
    input[type="submit"] {
      background-color: #4CAF50;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 16px;
      margin-top: 20px;
      width: 100%;
    }

    input[type="submit"]:hover {
      background-color: #45a049;
    }

    /* 오류 메시지 스타일 */
    .error-message {
      color: #ff0000;
      margin-top: 5px;
    }

    /* 성공 메시지 스타일 */
    .success-message {
      color: #008000;
      margin-top: 5px;
    }
  </style>
</head>
<body>
  <div class="form-container">
    <h1>양식 작성</h1>
    <form method="post" enctype="multipart/form-data" action="/submit">
      <label for="width">가로 길이:</label>
      <input type="text" name="width" id="width">

      <label for="height">세로 길이:</label>
      <input type="text" name="height" id="height">

      <label for="depth">높이:</label>
      <input type="text" name="depth" id="depth">

      <label for="weight">파트 무게:</label>
      <input type="text" name="weight" id="weight">

      <label for="material">소재:</label>
      <input type="text" name="material" id="material">

      <label for="purpose">용도:</label>
      <input type="text" name="purpose" id="purpose">

      <label for="image1">파일 첨부 1(STL, STEP 등 3D 설계파일):</label>
      <input type="file" name="image1" id="image1" required>

      <label for="image2">파일 첨부 2(JPG, PNG 등 파트 사진 - 선택사항):</label>
      <input type="file" name="image2" id="image2">

      <input type="submit" value="제출">
    </form>
  </div>
</body>
</html>
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
    image1 = request.files['image1']
    image2 = request.files.get('image2')

    filename1 = secure_filename(image1.filename)
    image1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

    filename2 = None
    if image2 and allowed_file(image2.filename):
        filename2 = secure_filename(image2.filename)
        image2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))


    #if image and allowed_file(image.filename):
    #filename = secure_filename(image.filename)
    #image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Create Excel file and write data
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = '가로(mm)'
    sheet['B1'] = '세로(mm)'
    sheet['C1'] = '높이(mm)'
    sheet['D1'] = '현재 파트 무게(g)'
    sheet['E1'] = '현재 소재'
    sheet['F1'] = '용도'
    sheet['G1'] = '파일명'
    sheet['A2'] = width
    sheet['B2'] = height
    sheet['C2'] = depth
    sheet['D2'] = weight
    sheet['E2'] = material
    sheet['F2'] = purpose
    sheet['G2'] = filename1
 
    if filename2:
      sheet['H1'] = '파일명'
      sheet['H2'] = filename2


    excel_filename = f"{filename1}.xlsx"
    wb.save(os.path.join(app.config['UPLOAD_FOLDER'], excel_filename))

    return '양식이 제출되었습니다.'

   # return jsonify({'message': '양식이 제출되었습니다.'})

   # else:
   #     return jsonify({'error': '올바른 이미지 파일을 첨부해야 합니다.'})

@app.route('/uploads')
def list_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
