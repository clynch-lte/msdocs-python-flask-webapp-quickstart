import os
import logging
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, make_response,
                   Response)

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
else:
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
   app.logger.info('Hello world log entry')
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if (request.args.get('validationToken')):
        token = request.args.get('validationToken')
        print(token)

        response = make_response(token, 200)
        response.mimetype = "text/plain"
        return response
    else:
        print(request.json)
        return Response("Hello, World!", status=200)
    
if __name__ == '__main__':
   app.run()