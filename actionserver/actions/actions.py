import requests
import json
import time

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from typing import Any, Text, Dict, List
from rasa_sdk.events import Restarted

RML_WHATSAPP_API = "https://apis.rmlconnect.net/wba/v1/messages"
WHATSAPP_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiRGVtbzEiLCJ1c2VybmFtZSI6IkRlbW8xIiwiZXhwIjoxODg2NDA4NDY0LCJlbWFpbCI6ImFrYXNyYW5qYW5AZ21haWwuY29tIiwib3JpZ19pYXQiOjE1NzEwNDg0NjQsImN1c3RvbWVyX2lkIjoiOWlyNURnN2J2c0NBIn0.shTadbC8N4bCSsPz7WyTTX6_stGe8G5Yuz-CIiQ3ZAI"
welcome_image_url = "https://node-media-uploader.s3.ap-south-1.amazonaws.com/2bd0da70-a41c-11ec-9098-63c92365b7b0-Airtel_Logo.jpg"
DEFAULT_VALUE="--"

class ActionReset(Action):

    def name(self) -> Text:
        return "action_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            return [Restarted()]

class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            HelperServices.send_image(tracker, welcome_image_url)
            time.sleep(2)
            HelperServices.sending_interactive_message(tracker.sender_id, "welcome_page", "interactive_list", "Options")
            return []

class ValidateMainMenuForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_main_menu_form"
        # main menu form

    def validate_main_menu(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            if slot_value.lower() == "ussd":
                HelperServices.sending_interactive_message(tracker.sender_id, "ussd_page_1", "interactive_list", "Options")
                return {"main_menu":slot_value.lower(),"invalid_form_count":None}
            elif slot_value.lower() == "vas":
                HelperServices.sending_interactive_message(tracker.sender_id, "vas_page_1", "interactive_list", "Options")
                return {"main_menu":slot_value.lower(),"ussd_menu": '-',"invalid_form_count":None}
            elif slot_value.lower() == "products":
                HelperServices.sending_interactive_message(tracker.sender_id, "products_page_1", "interactive_list", "Options")
                return {"main_menu":slot_value.lower(), "ussd_menu": '-', "vas_menu": '-',"invalid_form_count":None}
            elif slot_value.lower() == "data":
                HelperServices.sending_interactive_message(tracker.sender_id, "data", "interactive_list", "Options")
                return {"main_menu":slot_value.lower(), "ussd_menu": '-', "vas_menu": '-', "products_menu": '-', "invalid_form_count":None}
            elif slot_value.lower() == "useful_numbers":
                text_message = "▪️ Code: **311*2*Airtel Number#* \nDescription: Family and Friends (To add Numbers). \nAccessibility: Smart Connect 2.0 Subscribers.\n \n▪️ Code: **311*3*Airtel number#* \nDescription: Family and Friends (To remove Numbers). \nAccessibility: Smart Connect 2.0 Subscribers.\n \n▪️ Code: **311*4#* \nDescription: Family and Friends (To view Numbers). \nAccessibility: Smart Connect 2.0 Subscribers.\n \n▪️ Code: **140#* \nDescription: Data Account Balance. \nAccessibility: All Subscribers.\n \n▪️ Code: **452#* \nDescription: Data Bundles(N5,000/30 days). \nAccessibility: All Subscribers.\n \n▪️ Code: **462*10#* \nDescription: Data Bundles(N10,000/30 days). \nAccessibility: All Subscribers.\n \n▪️ Code: **496#* \nDescription: Data Bundles(N1,000/30 days). \nAccessibility: All Subscribers.\n \n▪️ Code: *111* \nDescription: Customer care line. \nAccessibility: Accessible to all subscribers.\n \n▪️ Code: *131* \nDescription: Postpaid Helpline. \nAccessibility: Calling accessible to only Postpaid subscribers.\n \n▪️ Code: **123#* \nDescription: Balance Confirmation. \nAccessibility: All Subscribers.\n \n▪️ Code: **126*rechargepin number#* \nDescription: Recharge card/Voucher loading. \nAccessibility: All Subscribers.\n \n▪️ Code: *743* \nDescription: Dealer Helpline. \nAccessibility: Calling accessible to registered dealer lines/SMS to SWAP available.\n \n▪️ Code: **123*1#* \nDescription: To view bonus. \nAccessibility: All Subscribers with bonuses. \n \n \nPlease type *Hi* to Start Conversation."
                # dispatcher.utter_message(text=text_message)
                HelperServices.send_text_message(tracker.sender_id, text_message)
                return {"main_menu":None,"invalid_form_count":None, "requested_slot":None}
            else:
                return HelperServices.invalid_count_step_fun(tracker,dispatcher,"main_menu", "welcome_page")
        except Exception as ex:
            print("exception",ex)
            return HelperServices.invalid_count_step_fun(tracker, dispatcher,"main_menu", "welcome_page")

    def validate_ussd_menu(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            text_message_data = {
                'self_service_code': "You don't need to memorize all the codes to manage your line Simply dial **121#* for self service.",
                'my_number': 'Simply Dial **121#*, Select Manage my account and Select My number.',
                'data_balance': 'Dial **140#* to view all your data subscriptions.',
                'data_bundle': 'Simply dial **141#* to view all the available bundle types.',
                'add_family_friends': '**311*2*Airtel Number#* to add, **311*3*Airtel Number#* to delete and **311*4#* (This only apply to lines on Smart Connect Package 2.0 & 5.0).',
                'check_airtime': 'Dial **123#* to view your account balance.',
                'take_loan': 'Dial **500#* to acccess the credit loan sercice and check eligibility.',
                'view_or_payback_loan': 'Dial **123#* to view your loan balance and **500*00#* to pay back the loan(**500*00#* doesn\'t give that option anymore).',
                'check_bonus': 'Kindly Dial **123*1#*  to see your bonus breakdown.',
                'cheap_calls': 'Simply dial **315#* to migrate to Smart talk to make calls at 11k/sec after N7 Access fee charge.',
                'transfer_credit': 'Dial **432#* to transfer credit.',
                'transfer_data': 'Dial **141#* and select Data Gifting & Sharing.',
                'talk_more': 'Dial **234#* and Select your preferred option.',
                'premier_connect': 'Dial **254#* and Select your preferred option.',
                'ring_back_tones': 'Dial **791#* and follow options to select your desired tone.',
                'call_notifications': 'Dial **362*1#* to Activate \nDial **362*2#* to Deactivate.',
                'sms_pack': 'Dial **160#* and Seleck your desired bundle.',
                'locate_shop': 'Dial **386#* to view list of shops and KYC locations.'}

            if slot_value.lower() in text_message_data.keys():
                text_message = text_message_data.get(slot_value.lower())
                HelperServices.sending_interactive_message(tracker.sender_id, "acknowledge_exit", "interactive_reply",data_message={'body_message': text_message, 'text_message': slot_value.replace('_', ' ').title()})
                return {"invalid_form_count":None, "faq_text_message": text_message, "ussd_menu": slot_value.lower() , "vas_menu": "-", "products_menu": "-", "data_menu": "-", "useful_numbers_menu": "-"}
            elif slot_value.lower() == "more options":
                HelperServices.sending_interactive_message(tracker.sender_id, "ussd_page_2", "interactive_list", "Options")
                return {"ussd_menu":None, "invalid_form_count":None}
            elif slot_value.lower() == "main menu":
                HelperServices.sending_interactive_message(tracker.sender_id, "welcome_page", "interactive_list", "Options", invalid_input='True')
                return {"main_menu":None, "data_menu": None,"products_menu":None, "ussd_menu":None, "vas_menu":None,"useful_numbers_menu": None,  "invalid_form_count":None, "acknowledge": None}
            else:
                return HelperServices.invalid_count_step_fun(tracker,dispatcher,"ussd_menu", "ussd_page_1")
        except Exception as ex:
            print("exception",ex)
            return HelperServices.invalid_count_step_fun(tracker, dispatcher,"ussd_menu", "ussd_page_1")

    def validate_vas_menu(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            text_message_data = {
            'transfer_credit': 'Dial **432#* and follow the options to transfer credit.',
            'me2u_pin': 'The default PIN is 1234. To change the PIN Dial **432#* and\n1. select *PIN CHANGE* \n2.Enter *Current PIN* (This will be the default PIN if the PIN has never been changed before) \n3.Enter *New PIN* \n4. Confirm *New PIN*',
            'stop_promotions': 'Text *HELP* to 2442 to receive a list of options to stop promotional SMS, however for FULL DND to stall all Promotional messages, Simply text *STOP* to *2442*',
            'sms_services': 'Simply dial **902#* and select either *START* or *STOP* to Activate/Deactivate your preferred SMS Based service.',
            'loan_eligibility': 'A minimum age of 2 months on the network is required. \nIf the desired amount is 50, 100, 200 or 500 and Recharge of the desired amount at least 3 times monthly for 2 consecutive months. \nIf the desired amount is 1000 – 2000 - Recharge of the desired amount at least 5 times for 2 consecutive months is required.',
            'take_loan': 'Dial **500#* to Acccess the credit loan sercice and check eligibility.',
            'view_or_payback_loan': 'Dial **123#* to view your loan balance (*500*00# doesn’t give that option anymore, recharges trigger recovery).',
            'service_charges': 'Yes. A service charge of 15% for loan from #50 - #6000 and a service charge of 20% for #25 loan.',
            'sms_pack': 'Dial **160#* and Seleck your desired bundle.',
            'ring_back_tones': 'Dial **791#* and follow options to select your desired tone.'}

            if slot_value.lower() in text_message_data.keys():
                text_message = text_message_data.get(slot_value.lower())
                HelperServices.sending_interactive_message(tracker.sender_id, "acknowledge_exit", "interactive_reply",data_message={'body_message': text_message, 'text_message': slot_value.replace('_', ' ').title()})
                return {"invalid_form_count":None, "faq_text_message": text_message,"vas_menu": slot_value.lower(), "products_menu": "-", "data_menu": "-", "useful_numbers_menu": "-"}
            elif slot_value.lower() == "more options":
                HelperServices.sending_interactive_message(tracker.sender_id, "vas_page_2", "interactive_list", "Options")
                return {"vas_menu":None, "invalid_form_count":None}
            elif slot_value.lower() == "main menu":
                HelperServices.sending_interactive_message(tracker.sender_id, "welcome_page", "interactive_list", "Options", invalid_input='True')
                return {"main_menu":None, "data_menu": None,"products_menu":None, "ussd_menu":None, "vas_menu":None,"useful_numbers_menu": None,  "invalid_form_count":None, "acknowledge": None}
            else:
                return HelperServices.invalid_count_step_fun(tracker,dispatcher,"vas_menu", "vas_page_1")
        except Exception as ex:
            print("exception",ex)
            return HelperServices.invalid_count_step_fun(tracker, dispatcher,"vas_menu", "vas_page_1")

    def validate_products_menu(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            text_message_data = {
                'add_family_friends': '**311*2*Airtel Number#* to add, **311*3*Airtel Number#* to delete and **311*4#* (This only applies to lines on Smart Connect 2.0 & 5.0).',
                'tariff_plan': 'Simply Dial **121#* and \nSelect  Manage my account \nSelect My Tariff Plan.',
                'free_data': '1. If you are on Smart Connect (Which is the default Plan on Airtel) Simply recharge between N100 to N1000 and you will receive free data upon every recharge valid for 7 days. \n2. You can also migrate to Smart Premier for more data upon recharge \nTo Opt in:Dial **318#* OR Text *YES* to *318* \nOn recharge of N100-198 - 5MB Bonus 1 day Validity \nOn recharge of N200-498 - 15MB Bonus 1 day Validity \nOn recharge of N500-998 - 50MB Bonus 3 day Validity \nOn recharge of N1000 above - 150MB Bonus 7 day Validity.',
                'check_bonus': 'Kindly Dial **123*1#* to see your bonus balance, **123*2#* for voice bundle balance.',
                'cheap_calls': 'Simply dial **315#* to migrate to Smart talk to make calls at 11k/sec.',
                'smart_talk': 'A daily access fee of NN7 will be charged upon Your first call of the day, However if you do not make call on any day, access fee will not apply.',
                'smart_connect': 'Recharge #100, #200, #300, #500 or #1000 to get 8 times (800% bonus!) value of your recharge valid for 7 days.',
                'ovajara': 'To enjoy benefits of Overjara, as a new customer,buy a new sim and activate it. You get a bonus of 8x  of #100 and above. N500 will be credited for voice, while N300 will be credited for data. Existing customers would dial **544#* to get the 8X bonus. They will however not get the N1000 naira activation fee.',
                'voice_bonus': 'To use voice bonus, make first minute Call of the day from your main account.',
                'night_browsing': 'You can enjoy discounted night browsing on Smart Trybe 2.0 \nSimply Dial **312#* to migrate and select your preferred night data plan. \nN500 for IGB  Bundle is valid for 7 days and can be used between 12AM and 5AM.',
                '10_times_reward': 'Simply Recharge With *220*Recharge PIN#. \nThe Smart Recharge option can also be accessed via alternative charnels i.e. Mobile Apps , ATMs, WEB, POS Terminals etc.',
                'talk_more': 'Dial **234#* and Select your preferred option.',
                'premier_connect': 'Dial **254#* and Select your preferred option.'}

            if slot_value.lower() in text_message_data.keys():
                text_message = text_message_data.get(slot_value.lower())
                HelperServices.sending_interactive_message(tracker.sender_id, "acknowledge_exit", "interactive_reply",data_message={'body_message': text_message, 'text_message': slot_value.replace('_', ' ').title()})
                return {"invalid_form_count":None, "faq_text_message": text_message, "products_menu": slot_value.lower(), "data_menu": "-", "useful_numbers_menu": "-"}
            elif slot_value.lower() == "more options":
                HelperServices.sending_interactive_message(tracker.sender_id, "products_page_2", "interactive_list", "Options")
                return {"products_menu":None, "invalid_form_count":None}
            elif slot_value.lower() == "main menu":
                HelperServices.sending_interactive_message(tracker.sender_id, "welcome_page", "interactive_list", "Options", invalid_input='True')
                return {"main_menu":None, "data_menu": None,"products_menu":None, "ussd_menu":None, "vas_menu":None,"useful_numbers_menu": None,  "invalid_form_count":None, "acknowledge": None}
            else:
                return HelperServices.invalid_count_step_fun(tracker,dispatcher,"products_menu", "products_page_1")
        except Exception as ex:
            print("exception",ex)
            return HelperServices.invalid_count_step_fun(tracker, dispatcher,"products_menu", "products_page_1")

    def validate_data_menu(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            text_message_data = {
                'subscribe': 'Simply dial **141#* to view all the available bundle types.',
                'check_balance': 'Dial **140#* to view all your data subscriptions.',
                'transfer_data': 'Dial **141#* and select Data Gifting & Sharing.',
                'configure': 'For Automatic Settings Simply Text Internet to 232 \nFor manual Settings Input the below settings \nAPN: Internet.ng.airtel.com \nUsername: Internet \nPassword:  Internet \nPlease ensure your Mobile data is turned on.',
                'deactivate': '*To deactivate* Android, Mega, Daily/Weekly bundles: **141*bundle price*1#* .',
                'social_bundle': 'The Social bundle is specially designed for Whats app,Twitter,Facebook,wechat, the bundle cannot be used to surf the internet on your regular browser.'}

            if slot_value.lower() in text_message_data.keys():
                text_message = text_message_data.get(slot_value.lower())
                HelperServices.sending_interactive_message(tracker.sender_id, "acknowledge_exit", "interactive_reply",data_message={'body_message': text_message, 'text_message': slot_value.replace('_', ' ').title()})
                return {"invalid_form_count":None, "faq_text_message": text_message, "data_menu": slot_value.lower(), "useful_numbers_menu": "-"}
            elif slot_value.lower() == "main menu":
                HelperServices.sending_interactive_message(tracker.sender_id, "welcome_page", "interactive_list", "Options", invalid_input='True')
                return {"main_menu":None, "data_menu": None,"products_menu":None, "ussd_menu":None, "vas_menu":None,"useful_numbers_menu": None,  "invalid_form_count":None, "acknowledge": None}
            else:
                return HelperServices.invalid_count_step_fun(tracker,dispatcher,"data_menu", "data")
        except Exception as ex:
            print("exception",ex)
            return HelperServices.invalid_count_step_fun(tracker, dispatcher,"data_menu", "data")

    def validate_acknowledge(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            pass
            if slot_value.lower() == "main_menu":
                HelperServices.sending_interactive_message(tracker.sender_id, "welcome_page", "interactive_list", "Options", invalid_input='True')
                return {"main_menu":None, "data_menu": None,"products_menu":None, "ussd_menu":None, "vas_menu":None,"useful_numbers_menu": None, "faq_text_message": None, "invalid_form_count":None, "acknowledge": None}
            else:
                return HelperServices.invalid_count_step_fun(tracker, dispatcher,"acknowledge", "acknowledge_exit", "interactive_reply")
        except Exception as ex:
            print("exception",ex)
            return HelperServices.invalid_count_step_fun(tracker, dispatcher,"acknowledge", "acknowledge_exit", "interactive_reply")


class HelperServices():
    
    def invalid_count_step_fun(tracker, dispatcher,slot_name, slot_value=None, message_type="interactive_list"):
        try:
            invalid_form_count = tracker.slots.get('invalid_form_count')
            if invalid_form_count:
                if invalid_form_count == 1:
                    dispatcher.utter_message(response="utter_invalid_exit_msg")              
                    return {slot_name:None,"requested_slot":None}
            else:
                if slot_value:
                    if slot_value == "acknowledge_exit":
                        HelperServices.sending_interactive_message(tracker.sender_id, slot_value, message_type, "Options", invalid_input=True, data_message={'body_message': tracker.slots.get('faq_text_message'), 'text_message': ''})
                    else:
                        HelperServices.sending_interactive_message(tracker.sender_id, slot_value, message_type, "Options", invalid_input=True)
                else:
                    dispatcher.utter_message(response="utter_invalid_input")
                return {slot_name: None, 'invalid_form_count':1}

        except Exception as error:
            print("error :", error)

    def send_text_message(phone_number, message):
        """
        use this method to send text message.
        """
        try:
            headers_data = {
                "Authorization": WHATSAPP_TOKEN,
                'Content-Type': 'application/json'
            }
            request_body = {
                'phone': '+' + phone_number,
                'text': message
            }
            requests.post(RML_WHATSAPP_API, headers=headers_data, data=json.dumps(request_body))
        except Exception as ex:
            print("Sending Text Message Exception:", ex)

    def sending_interactive_message(phone_number, keyword, request_type, button_text="", invalid_input=False,image_url=None, data_message=None):
        """
        use this method as a common handler for sending Interactive reply and list.
        """
        payload_data = HelperServices.get_templates_data(keyword)
        try:
            if payload_data:
                body_message = payload_data.get('body_message')
                text_message = payload_data.get('text_message')
                option_data = payload_data.get('data')

                if keyword == "welcome_page" and invalid_input and isinstance(invalid_input, str):
                    text_message = 'Main menu'
                    body_message = 'Please select a menu option.'
                elif invalid_input:
                    text_message = "Invalid input, try again"
                    if keyword == "acknowledge_exit" and data_message:
                        body_message = data_message.get('body_message')

                if not invalid_input and (keyword == "acknowledge_exit" and data_message):
                    body_message = data_message.get('body_message')
                    text_message = data_message.get('text_message')

                headers_data = {
                    "Authorization": WHATSAPP_TOKEN,
                    'Content-Type': 'application/json'
                }
                media_headers = {
                    "text": text_message
                }
                if image_url:
                    media_headers = {
                        "type": "image",
                        "url": image_url,
                    }
                media_dict = {
                        "type": request_type,
                        "header": media_headers,
                        "body": body_message,
                        "footer_text": " ",
                        "button": option_data,
                }

                if request_type == 'interactive_list':
                     media_dict.update({'button_text': button_text})

                body = {
                    "phone": "+"+phone_number,
                    "extra": "{your value}",
                    "media": media_dict
                }
                
                response_data = requests.post(RML_WHATSAPP_API, headers=headers_data, data=json.dumps(body))
                # va = response_data
                # HelperServices.save_chat_api(phone_number, body)
            else:
                raise Exception('No template registered for keyword: {}'.format(keyword))

        except Exception as ex:
            print("Sending Interactive Message Exception:", ex)

    def get_templates_data(keyword):
        """
        this method is used to set body , data(options) and text message
        """
        text_message, body_message, option_data = '','',[]
        payload_data = {
            "welcome_page": {
                'text_message': 'We will be happy to assist you.',
                'body_message': 'To begin, Please select a menu option.',
                'data': [{
                "section_title": "Select Option",
                "row": [
                    {
                        "id": "ussd",
                        "title": "USSD",
                        "description": ""
                    },
                    {
                        "id": "vas",
                        "title": "VAS",
                        "description": ""
                    },
                    {
                        "id": "products",
                        "title": "Products",
                        "description": ""
                    },
                    {
                        "id": "data",
                        "title": "Data",
                        "description": ""
                    },
                    {
                        "id": "useful_numbers",
                        "title": "Useful Numbers",
                        "description": ""
                    }
                ]
            }]
            },
            "ussd_page_1": {
                'text_message': 'USSD Codes Page 1',
                'body_message': 'Please select an option.',
                'data': [{
                "section_title": "Select Option",
                "row": [
                    {
                        "id": "self_service_code",
                        "title": "Self Service Code",
                        "description": "What is the SelfService code?"
                    },
                    {
                        "id": "my_number",
                        "title": "My Number",
                        "description": "How do I know my number?"
                    },
                    {
                        "id": "data_balance",
                        "title": "My Data Balance",
                        "description": "How can I check my data balance?"
                    },
                    {
                        "id": "data_bundle",
                        "title": "Data Bundles",
                        "description": "How can I subscribe for a data bundle?"
                    },
                    {
                        "id": "add_family_friends",
                        "title": "Add Family & Friends",
                        "description": "How can I add Family and Friends on my line?"
                    },
                    {
                        "id": "check_airtime",
                        "title": "Check My Airtime",
                        "description": "How can I check my airtime?"
                    },
                    {
                        "id": "take_loan",
                        "title": "Take Loan",
                        "description": "How can I take a loan from the network?"
                    },
                    {
                        "id": "view_or_payback_loan",
                        "title": "View or Payback Loan",
                        "description": "How can I view my loan balance and Payback my loan?"
                    },
                    {
                        "id": "check_bonus",
                        "title": "Check Bonus",
                        "description": "How do I check my bonus?"
                    },
                    {
                        "id": "more options",
                        "title": "More Options",
                        "description": "Click here to view more options"
                    }
                ]
            }]
            },
            "ussd_page_2": {
                'text_message': 'USSD Codes Page 2',
                'body_message': 'Please select an option.',
                'data': [{
                "section_title": "Select Option",
                "row": [
                    {
                        "id": "cheap_calls",
                        "title": "Make Cheap Calls",
                        "description": "How do I make cheap calls to all networks in Nigeria?"
                    },
                    {
                        "id": "transfer_credit",
                        "title": "Transfer Credit",
                        "description": "How do i to transfer credit?"
                    },
                    {
                        "id": "transfer_data",
                        "title": "Transfer Data",
                        "description": "How can I transfer data from my line to another line?"
                    },
                    {
                        "id": "talk_more",
                        "title": "Talk More",
                        "description": "How can I buy the talk more & 6x bundles?"
                    },
                    {
                        "id": "premier_connect",
                        "title": "Premier connect",
                        "description": "How can I buy the  Premier connect bundle?"
                    },
                    {
                        "id": "ring_back_tones",
                        "title": "Ring Back Tones",
                        "description": "How can I activate caller ring back tones?"
                    },
                    {
                        "id": "call_notifications",
                        "title": "Call Notifications",
                        "description": "How do I activate/Deactivate end of call notifications?"
                    },
                    {
                        "id": "sms_pack",
                        "title": "SMS Pack",
                        "description": "How do I subscribe to the SMS Pack ?"
                    },
                    {
                        "id": "locate_shop",
                        "title": "Nearest Shop",
                        "description": "How do I locate the nearest Airtel shop?"
                    },
                    {
                        "id": "main menu",
                        "title": "Main Menu",
                        "description": "Click here to go to Main menu"
                    },
                ]
            }]
            },
            "vas_page_1": {
                'text_message': 'VAS Page 1',
                'body_message': 'Please select an option.',
                'data': [{
                "section_title": "Select Option",
                "row": [
                    {
                        "id": "transfer_credit",
                        "title": "Transfer Credit",
                        "description": "How can I transfer credit from my line to another line?"
                    },
                    {
                        "id": "me2u_pin",
                        "title": "Me2u PIN",
                        "description": "How do I change my Me2u PIN?"
                    },
                    {
                        "id": "stop_promotions",
                        "title": "Stop Promotions",
                        "description": "How do I stop promotional messages from coming into my line?"
                    },
                    {
                        "id": "sms_services",
                        "title": "SMS Based Services",
                        "description": "How can I activate or Deactivate SMS Based services billied on my line?"
                    },
                    {
                        "id": "loan_eligibility",
                        "title": "Loan Eligibility",
                        "description": "How do I qualify for airtime Loan on the network?"
                    },
                    {
                        "id": "more options",
                        "title": "More Options",
                        "description": "Click here to view more options"
                    }
                ]
            }]
            },
            "vas_page_2": {
                'text_message': 'VAS Page 2',
                'body_message': 'Please select an option.',
                'data': [{
                "section_title": "Select Option",
                "row": [
                    {
                        "id": "take_loan",
                        "title": "Take Loan",
                        "description": "How can I take a loan from the network?"
                    },
                    {
                        "id": "view_or_payback_loan",
                        "title": "View or Payback Loan",
                        "description": "How can I view my loan balance and Payback my loan?"
                    },
                    {
                        "id": "service_charges",
                        "title": "Service Charges",
                        "description": "Is there any service charge when I take a loan?"
                    },
                    {
                        "id": "sms_pack",
                        "title": "SMS Pack",
                        "description": "How do I subscribe to the SMS Pack?"
                    },
                    {
                        "id": "ring_back_tones",
                        "title": "Ring Back Tones",
                        "description": "How can I activate caller ring back tones?"
                    },
                    {
                        "id": "main menu",
                        "title": "Main Menu",
                        "description": "Click here to go to Main menu"
                    }
                ]
            }]
            },
            "products_page_1": {
                'text_message': 'Products Page 1',
                'body_message': 'Please select an option.',
                'data': [{
                "section_title": "Select Option",
                "row": [
                    {
                        "id": "add_family_friends",
                        "title": "Add Family & Friends",
                        "description": "How can I add Family and Friends on my line?"
                    },
                    {
                        "id": "tariff_plan",
                        "title": "Tariff plan",
                        "description": "How do I know my tariff Plan ?"
                    },
                    {
                        "id": "free_data",
                        "title": "Free DATA",
                        "description": "How can I get free data on my line?"
                    },
                    {
                        "id": "check_bonus",
                        "title": "Check Bonus",
                        "description": "How do I check my available bonuses?"
                    },
                    {
                        "id": "cheap_calls",
                        "title": "All Networks",
                        "description": "How do I make cheap calls to all networks in Nigeria?"
                    },
                    {
                        "id": "smart_talk",
                        "title": "Smart Talk",
                        "description": "What is the condition to make cheap calls on smarttalk?"
                    },
                    {
                        "id": "smart_connect",
                        "title": "Smart Connect",
                        "description": "How do I enjoy 8x bonus on Smart Connect?"
                    },
                    {
                        "id": "more options",
                        "title": "More Options",
                        "description": "Click here to view more options"
                    }
                ]
            }]
            },
            "products_page_2": {
                'text_message': 'Products Page 2',
                'body_message': 'Please select an option.',
                'data': [{
                "section_title": "Select Option",
                "row": [
                    {
                        "id": "ovajara",
                        "title": "Ovajara",
                        "description": "How do I get Ovajara? "
                    },
                    {
                        "id": "voice_bonus",
                        "title": "Voice Bonus",
                        "description": "How do I enjoy My voice Bonus?"
                    },
                    {
                        "id": "night_browsing",
                        "title": "Night Browsing",
                        "description": "How do I enjoy discounted night browsing?"
                    },
                    {
                        "id": "10_times_reward",
                        "title": "10 Times Reward",
                        "description": "How do I get 10 Times what I recharge on my line?"
                    },
                    {
                        "id": "talk_more",
                        "title": "Talk More",
                        "description": "How can I buy the talk more bundle?"
                    },
                    {
                        "id": "premier_connect",
                        "title": "Premier connect",
                        "description": "How can I buy the  Premier connect bundle?"
                    },
                    {
                        "id": "main menu",
                        "title": "Main Menu",
                        "description": "Click here to go to Main menu"
                    }
                ]
            }]
            },
            "data": {
                'text_message': 'Data',
                'body_message': 'Please select an option.',
                'data': [{
                "section_title": "Select Option",
                "row": [
                    {
                        "id": "subscribe",
                        "title": "Subscribe",
                        "description": "How can I subscribe for a data bundle?"
                    },
                    {
                        "id": "check_balance",
                        "title": "Check Data Balance",
                        "description": "How can I check my data balance?"
                    },
                    {
                        "id": "transfer_data",
                        "title": "Transfer Data",
                        "description": "How can I transfer data from my line to another line?"
                    },
                    {
                        "id": "configure",
                        "title": "Configure",
                        "description": "How can I configure my line for data?"
                    },
                    {
                        "id": "deactivate",
                        "title": "Deactivate",
                        "description": "How do I deactivate my data Bundle?"
                    },
                    {
                        "id": "social_bundle",
                        "title": "Social Bundle",
                        "description": "Can I Use my social bundle to Surf the Internet?"
                    },
                    {
                        "id": "main menu",
                        "title": "Main Menu",
                        "description": "Click here to go to Main menu"
                    }
                ]
            }]
            },
            "acknowledge_exit": {
                'body_message': "",
                'text_message': ' ',
                'data': [
                    {
                        "id": "main_menu",
                        "title": "Main Menu"
                    }
                ]
            },
        }

        data = payload_data.get(keyword,'')
        return data

    def send_image(tracker, url):
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': WHATSAPP_TOKEN
            }
            body = {
                    "phone": "+"+tracker.sender_id,
                    "media": {
                    "type": "image",
                    "url": url,
                    "caption":"Heyya!👋\nWelcome to *Airtel*."
                    },
                }
            response_data = requests.post(
                url = RML_WHATSAPP_API,
                data = json.dumps(body),
                headers=headers,
                timeout=5
            )
            # HelperServices.save_chat_api(tracker.sender_id, body)
            print(response_data.content)
        except Exception as e:
            print(e)

    # def save_chat_api(phone_number, body):
    #     """
    #     use this method to save chat bot conversations.
    #     """
    #     try:
    #         payload = {
    #             "customer_identifier" : str(phone_number),
    #             "vendor" :  VENDOR_NAME,
    #             "chatbot_response": [body],
    #             "user_input":"",
    #             "service_type": "whatsapp",
    #         }
    #         auth_header = { 'Content-Type': 'application/json'}
    #         response_data = requests.post(url = RML_LIVE_AGENT_SAVE_CHAT_API,headers=auth_header,data = json.dumps(payload),timeout=20)

    #         print("response_data ",response_data)
    #     except Exception as ex:
    #         print('Exception occured while saving conversation')

