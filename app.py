import requests
from flask import Flask,request,jsonify
app = Flask(__name__)
from decouple import config



API_KEY = config("KEY")
def get_conversion(source_currency,target_currency,source_amount):
        global API_KEY
        response = requests.get(f"https://exchange-rates.abstractapi.com/v1/live/?api_key={API_KEY}&base={source_currency}&target={target_currency}")
        context =response.json()
        rate = context["exchange_rates"][target_currency]
        return rate*source_amount
        

@app.route('/',methods=['POST'])
def index():
    print('request sent')
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    target_currency = data['queryResult']['parameters']['currency-name']
    source_amount = data['queryResult']['parameters']['unit-currency']['amount']
    conversion =round(get_conversion(source_currency,target_currency,source_amount),2)
    response = {
        'fulfillmentText':f"{source_amount} {source_currency} To {target_currency} is {conversion} {target_currency}"
    }
    print(response)
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
    