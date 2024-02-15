import os
from datetime import datetime, timedelta
from subprocess import Popen, PIPE

from celery import Celery
from celery.schedules import crontab

from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

# 配置 Celery
app.config['CELERY_BROKER_URL'] = 'redis://:@Ljx62149079@www.sakebow.cn:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://:@Ljx62149079@www.sakebow.cn:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

UPLOAD_FOLDER = './uploads'

# 确保上传和输出目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'curxptheme'}

@celery.task
def clear_old_files():
  cutoff_time = datetime.now() - timedelta(hours = 1)
  for filename in os.listdir(UPLOAD_FOLDER):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
    if file_mtime < cutoff_time:
      os.remove(file_path)

@celery.task(bind=True)
def process_file(self, input_filename):
  # 构建 Perl 脚本的命令行
  command = ['perl', '104659-sd2xc-2.5.pl', input_filename]
  # 运行 Perl 脚本并捕获输出
  process = Popen(command, stdout=PIPE, stderr=PIPE)
  stdout, stderr = process.communicate()
  if process.returncode == 0:
    # 假设脚本输出的最后一行是输出文件名
    output_filename = stdout.decode().strip().split('\n')[-1]
    return {'status': 'success', 'output_file': output_filename}
  else:
    return {'status': 'failure', 'error': stderr.decode()}

@app.route('/upload', methods=['POST'])
def upload_file():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'}), 400
  file = request.files['file']
  if file.filename == '' or not allowed_file(file.filename):
    return jsonify({'error': 'No selected file or file type not allowed'}), 400
  filename = os.path.join(UPLOAD_FOLDER, file.filename)
  task = process_file.apply_async(args=[filename])
  return jsonify({'task_id': task.id}), 202

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
  task = process_file.AsyncResult(task_id)
  if task.state == 'PENDING':
    response = {
      'state': task.state,
      'status': 'Pending...'
    }
  elif task.state != 'FAILURE':
    response = {
      'state': task.state,
      'status': task.info.get('status', ''),
      'output_file': task.info.get('output_file', '')
    }
  else:
    # something went wrong in the background job
    response = {
      'state': task.state,
      'status': str(task.info),  # this is the exception raised
    }
  return jsonify(response)

# 在 app.config 中添加定时任务配置
app.config['CELERYBEAT_SCHEDULE'] = {
  'clear_old_files': {
    'task': 'app.clear_old_files',
    'schedule': crontab(hour=0, minute=0),  # 每天午夜执行
  },
}

celery.conf.update(app.config)
'''
if __name__ == '__main__':
  app.run(port=40080)
'''
