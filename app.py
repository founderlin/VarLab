from flask_bootstrap import Bootstrap
import os
import time
from flask import Flask, render_template, send_from_directory, request
from backend.plus import TestFun

app = Flask(__name__)
bootstrap = Bootstrap(app)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'ifc', 'txt', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def page1():
    return render_template('001.html')


@app.route('/002')
def page2():
    return render_template('002.html')


@app.route('/003')
def page3():
    return render_template('003.html')


@app.route('/002', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname=f.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time)+'.'+ext   # 修改文件名
        f.save(os.path.join(file_dir, new_filename))  #保存文件到upload目录
        return render_template('002.html', J_COL=1)
    else:
        return render_template('002.html', J_COL=2)


@app.route('/x', methods=['GET', 'POST'])
def plus_method():
    if request.method == "POST":
        a = int(request.form['input1'])
        b = int(request.form['input2'])
        x = TestFun(a,b)
        c = x.plusx()
        return render_template('test.html', PLUS=str(c))
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
