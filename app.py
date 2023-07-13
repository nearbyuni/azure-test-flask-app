import os
import requests
import json
import logging
from flask import (Flask, redirect, render_template, request, jsonify,
                   send_from_directory, url_for)

app = Flask(__name__)


# Load environment variables
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

twilio_flow_url = "https://studio.twilio.com/v1/Flows/FW563f040ea706b6677eef8fdfd345ff3c/Executions"
vendor_db = "https://api.onedrive.com/v1.0/shares/u!aHR0cHM6Ly8xZHJ2Lm1zL3UvcyFBdXZyMHpMTjdDeWhnYU1neXFGZ1c3UVlrM2ZyQVE_ZT1GSWludnU/root/content"
response = requests.get(vendor_db)
vendors = response.json()



@app.route('/')
def index():
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

@app.route('/notify-vendor', methods=['GET','POST'])
def notify():
  if request.method == "GET":
    return jsonify({'message': 'Welcome to Misa Express!'}), 200
  if request.method == "POST":
    order_data = request.get_data(as_text=True)
    order_json = json.loads(order_data)
    vendorId = order_json["line_items"][0]["meta_data"][0]["value"]

    if vendorId in vendors:
      phone_number = vendors[vendorId]
      data = {"To": phone_number, "From": "+14845597055"}

      auth = ("AC1b843a5a08f3e3549fd5602232ce30e3", "972bbcb94892ac8c484c7e9e2156fac3")

      response = requests.post(twilio_flow_url, data=data, auth=auth)

      if response.status_code == 200:
        return jsonify({'message': 'SUCCESS!'}), 200
      else:
        return jsonify({'message': 'ERROR!'}), 500
    else:
      return "Vendor ID not found", 404
  else:
    return jsonify({'message': 'ERROR!'}), 100



if __name__ == '__main__':
   app.run()
