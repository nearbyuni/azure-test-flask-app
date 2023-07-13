import os
import requests
import logging
import json
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def webhook():
  if request.method == "GET":
    return jsonify({'message': 'Welcome to Misa Express!'}), 200
  if request.method == "POST":
    order_data = request.get_data(as_text=True)
    order_json = json.loads(order_data)
    vendorId = order_json["line_items"][0]["meta_data"][0]["value"]
    result = {"vendor_id": vendorId}
    app.logger.info(result)

    if vendorId in vendors:
      phone_number = vendors[vendorId]
      data = {"To": phone_number, "From": "+14845597055"}

      auth = (AC1b843a5a08f3e3549fd5602232ce30e3, AC1b843a5a08f3e3549fd5602232ce30e3
              )  # Use environment variables

      response = requests.post(twilio_flow_url, data=data, auth=auth)

      if response.status_code == 200:
        return jsonify({'message': 'ERROR!'}), 200
      else:
        return jsonify({'message': 'ERROR!'}), 500
    else:
      return "Vendor ID not found", 404
  else:
    return jsonify({'message': 'ERROR!'}), 100


if __name__ == '__main__':
   app.run()
