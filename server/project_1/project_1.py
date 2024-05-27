import os
from ..utils.server import app, request
import json

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

def load_cron_file():
    try:
        with open('CRON.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_cron_file(cron):
    with open('CRON.json', 'w') as f:
        json.dump(cron, f)

def add_cron_job(cron, filename, cron_expression):
    cron[filename] = cron_expression
    save_cron_file(cron)

def remove_cron_job(cron, filename):
    cron.pop(filename, None)
    save_cron_file(cron)

def update_crontab(cron_expression, filename):
    os.system('crontab -l > tempcron')
    with open('tempcron', 'a') as f:
        f.write(f"{cron_expression} python3 {os.path.join(app.config['UPLOAD_FOLDER'], filename)}\n")
    os.system('crontab tempcron')
    os.remove('tempcron')

def remove_crontab_job(filename):
    os.system('crontab -l > tempcron')
    with open('tempcron', 'r') as f:
        lines = f.readlines()
    with open('tempcron', 'w') as f:
        for line in lines:
            if filename not in line:
                f.write(line)
    os.system('crontab tempcron')
    os.remove('tempcron')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = f.filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cron = load_cron_file()
        add_cron_job(cron, filename, request.form['cron'])
        update_crontab(request.form['cron'], filename)
        return 'File uploaded successfully'
    else:
        return 'Method not allowed'

@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        filename = request.form['filename']
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cron = load_cron_file()
        remove_cron_job(cron, filename)
        remove_crontab_job(filename)
        return 'File deleted successfully'
    else:
        return 'Method not allowed'

@app.route('/list', methods=['GET'])
def list_files():
    if request.method == 'GET':
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return files
    else:
        return 'Method not allowed'

if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(host='0.0.0.0', port=8000)