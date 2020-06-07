import requests
import hashlib
import work_with_db
from datetime import datetime
from dateutil import parser

merchant_id = '78eb06d1ad3d3beccee0bc623a5551d5'
invoice_amount = 10
invoice_currency ='usd'
language = 'ru'
secret = '59f58b2e36ce94c0e48364fbf7c76039'


class Api:
    url = 'https://api.cryptonator.com/api/merchant/v1/'

    def __init__(self, merchant_id, secret, language):
        self.merchant_id = merchant_id
        self.secret = secret
        self.language = language
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        self.headers = {"User-Agent": self.user_agent}

    def create_invoice(self, item_name, invoice_amount, invoice_currency):
        response = requests.get(url=self.url + 'startpayment', params={
            'merchant_id': self.merchant_id,
            'item_name': item_name,
            'invoice_amount': invoice_amount,
            'invoice_currency': invoice_currency,
        }, headers=self.headers)
        invoice_id = str(response.url).split('/')[-1]
        return response.url, invoice_id

    def check_invoice(self, invoice_id):
        hash = hashlib.sha1(f'{self.merchant_id}&{invoice_id}&{self.secret}'.encode())
        response = requests.post(url=self.url + 'getinvoice', headers=self.headers,
                                 data={
                                     'merchant_id': self.merchant_id,
                                     'invoice_id': invoice_id,
                                     'secret_hash': hash.hexdigest()
                                 })
        return response.json()


def create_invoice(amount):
    api = Api(merchant_id, secret, language)

    response = api.create_invoice(
          item_name='Pay',
          invoice_amount=amount,
          invoice_currency='usd')

    return response  # returning url


def check_result(invoice_id):
    api = Api(merchant_id, secret, language)
    response = api.check_invoice(invoice_id)
    if response['status'] == 'paid':
        return True, response['amount']
    else:
        return False


def checking_payments():
    data = work_with_db.dump_payments()
    waiting_payments, deleted_payments, completed_payments = 0, 0, 0
    for values in data:
        if check_result(values[1]):
            work_with_db.payment(values[1], check_result(values[1])[1])  # add new completed payment in database
            completed_payments += 1
        elif int(str(datetime.now() - parser.parse(values[2]))[2]) > 3:  # delete invoice if minutes == 40
            work_with_db.deleting_invoices(values[1])
            deleted_payments += 1
        else:
            waiting_payments += 1
    with open('logs.txt', 'a') as logs:
        log = "{} Checked payments: {} Wait for pay: {} Deleted: {} Completed: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M"), len(data), waiting_payments, deleted_payments, completed_payments)
        logs.write(log)
