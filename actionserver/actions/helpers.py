"""
this file is used to trigger analytics and enquiry api
"""
import requests
import json

base_url = "https://apis.rmlconnect.net/rml-live-agent-central-system/chatbot/"

def trigger_analytics_api(vendor_name, type_of_activity, display_title, chart_type="line_chart"):
    """
    use this method to trigger save dynamic analytics api
    """
    try:
        request_body = {
            "vendor_username": vendor_name,
            "type_of_activity": type_of_activity,
            "chart_type": chart_type,
            "display_title": display_title
        }
        url = base_url + "dynamic-analytics/"

        headers = {'Content-Type': 'application/json'}

        requests.request("POST", url, headers=headers, data=json.dumps(request_body))
    except Exception as ex:
        print('Exception ocured while triggering analytics api, ', ex)


def trigger_enquiries_api(
    name, phone_number, chatbot_data, vendor_name,
    request_about, request_type, address="", rating="", check_status="", feedback=""):
    """
    use this method to trigger save enquiries api
    """
    try:
        request_body = {
                "customer_name": name,
                "phone_number": phone_number,
                "address": address,
                "request_about": request_about,
                "rating": rating,
                "check_status": check_status,
                "chatbot_data": chatbot_data,
                "request_type": request_type,
                "vendor_username": vendor_name,
                "feedback": feedback
            }
        url = base_url + "save-enquiries/"

        headers = {'Content-Type': 'application/json'}

        requests.request("POST", url, headers=headers, data=json.dumps(request_body))
    except Exception as ex:
        print('Exception ocured while triggering enquiry api, ', ex)
