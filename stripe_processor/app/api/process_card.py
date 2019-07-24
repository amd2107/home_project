from datetime import datetime
import json
import logging
import re
import stripe

from app.api.models import Traceback

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

class ProcessCard:
    request_traceback_id = None

    logger = logging.getLogger(__name__)

    def process(self, data):

        self.request_traceback_id = None

        card = data['card']
        cvv = data['cvv']
        date = data['date']
        transaction_id = data['transaction_id']

        validateCard_resp = self.validateCard(card)
        validateCvv_resp = self.validateCvv(cvv)
        validateDate_resp = self.validateDate(date)


        if not validateCard_resp['success']:
            return validateCard_resp

        if not validateCvv_resp['success']:
            return validateCvv_resp

        if not validateDate_resp['success']:
            return validateDate_resp

        parsed_data = {
            "card": validateCard_resp['data']['card'],
            "cvv": validateCvv_resp['data']['cvv'],
            "month": validateDate_resp['data']['month'],
            "year": validateDate_resp['data']['year'],
            "transaction_id": transaction_id
        }

        executeSlipstream_resp = self.executeSlipstream(parsed_data)

        if not executeSlipstream_resp['success']:
            return executeSlipstream_resp

        return executeSlipstream_resp


    def validateCard(self, card):
        # Validate that just came numbers in the card
        validate_numbers = re.match('^[0-9]+$', card)

        if validate_numbers == None:
            return {
                "success": False,
                "status": 400,
                "error": "Please only use numbers in the card input"
            }

        return {
            "success": True,
            "data": {
                "card": card
            }
        }

    def validateCvv(self, cvv):
        # Validate that just came numbers in the card
        validate_numbers = re.match('^[0-9]+$', cvv)

        if validate_numbers == None:
            return {
                "success": False,
                "status": 400,
                "error": "Please only use numbers in the cvv input"
            }

        return {
            "success": True,
            "data": {
                "cvv": cvv
            }
        }

    def validateDate(self, date):
        # Validate that just came numbers in the card
        validate_numbers = re.match('^[0-9]+$', date)

        if validate_numbers == None:
            return {
                "success": False,
                "status": 400,
                "error": "Please only use numbers in the date input"
            }

        month = date[:2]
        year = date[2:4]

        

        #Validate The Month
        if int(month) < 1 or int(month) > 12:
            return {
                "success": False,
                "status": 400,
                "error": "The month is invalid, please use a value between 01 and 12"
            }

        #Validate The Year
   
        now = datetime.now() # current date and time

        full_year = str(now.strftime("%Y"))
        short_year = now.strftime("%-y")

        max_year = int(short_year) + 8

        if int(year) < int(short_year) or int(year) > max_year:
            return {
                "success": False,
                "status": 400,
                "error": "The year is invalid, please use a value between the actual year and 8 years more as maximum"
            }

        parsed_year = full_year[:2] + str(year)

        return {
            "success": True,
            "data": {
                "month": month,
                "year": int(parsed_year)
            }
        }


    def executeSlipstream(self, parsed_data):

        parsed_data_to_log = {}
        parsed_data_to_log['card'] = 'xxxx xxxx xxxx ' + parsed_data['card'][-4:]
        parsed_data_to_log['cvv'] = 'xxx'
        parsed_data_to_log['month'] = parsed_data['month'],
        parsed_data_to_log['year'] = parsed_data['year'],
        parsed_data_to_log['transaction_id'] = parsed_data['transaction_id']

        self.logger.info(json.dumps(parsed_data_to_log))

        traceback = Traceback(data = json.dumps(parsed_data_to_log))
        traceback.save()

        self.request_traceback_id = traceback

        print (parsed_data_to_log)
        print (parsed_data)

        try:

            resp = stripe.PaymentMethod.create(
                type='card',
                card={
                    'number': parsed_data['card'],
                    'exp_month': parsed_data['month'],
                    'exp_year': parsed_data['year'],
                    'cvc': parsed_data['cvv'],
                },
            )

        except Exception as e:

            body = e.json_body
            err  = body.get('error', {})
            
            self.logger.error(e)

            traceback = Traceback(data = e, is_request = False, trace_id = self.request_traceback_id)
            traceback.save()

            return {
                "success": False,
                "status": e.http_status,
                "error": err.get('message')
            }


        self.logger.info(json.dumps(resp))
        traceback = Traceback(data = json.dumps(resp), is_request = False, trace_id = self.request_traceback_id)
        traceback.save()


        return {
            "success": True,
            "data": resp
        }

