import os
from flask import Flask, json, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# Lambda Upload function, which takes in a python file and stores it locally, and it also takes a CRON parameter that stores how often the Lambda function should run
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = f.filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # There is a CRON dictionary that stores the CRON parameters for each Lambda function
        # Retrieve it, add this new function to the dictionary, and store the dictionary back as a JSON file
        try:
            with open('CRON.json', 'r') as f:
                cron = json.load(f)
        except:
            cron = {}        
        cron[filename] = request.form['cron']
        with open('CRON.json', 'w') as f:
            print(cron)
            json.dump(cron, f)
        # Finally, add the actual CRON job to the crontab
        os.system('crontab -l > tempcron')
        with open('tempcron', 'a') as f:
            f.write(request.form['cron'] + ' python3 ' + os.path.join(app.config['UPLOAD_FOLDER'], filename) + '\n')
        f.close()
        os.system('crontab tempcron')
        os.remove('tempcron')
        return 'File uploaded successfully'
    else:
        return 'Method not allowed'
    
# Lambda Delete function, which deletes a python file
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        filename = request.form['filename']
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # There is a CRON dictionary that stores the CRON parameters for each Lambda function
        # Retrieve it, remove this function from the dictionary, and store the dictionary back as a JSON file
        try:
            with open('CRON.json', 'r') as f:
                cron = json.load(f)
        except:
            cron = {}        
        cron.pop(filename, None)
        with open('CRON.json', 'w') as f:
            json.dump(cron, f)
        # Finally, remove the actual CRON job from the crontab
        os.system('crontab -l > tempcron')
        with open('tempcron', 'r') as f:
            lines = f.readlines()
        with open('tempcron', 'w') as f:
            for line in lines:
                if filename not in line:
                    f.write(line)
        os.system('crontab tempcron')
        os.remove('tempcron')
        return 'File deleted successfully'
    else:
        return 'Method not allowed'
    
# Lambda List function, which lists all python files
@app.route('/list', methods=['GET'])
def list():
    if request.method == 'GET':
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return files
    else:
        return 'Method not allowed'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)