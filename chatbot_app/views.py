# chatbot_app/views.py
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Customer, Transaction
import re
import requests

# A dictionary to keep track of whether it's the user's first interaction
first_time_interactions = {}

# A dictionary to store user inputs
user_inputs = {}

def chatbot(request):
    # Set a flag indicating it's the user's first interaction when rendering the chatbot view
    customer_mobile = request.GET.get('customer_mobile', '')
    first_time_interactions[customer_mobile] = True

    return render(request, 'index.html')

def get_bot_response(question, user_message, customer_mobile):
    global first_time_interactions, user_inputs

    # Check if it's the user's first interaction or if the user entered an empty message
    if first_time_interactions.get(customer_mobile, False) or not question:
        first_time_interactions[customer_mobile] = False
        message = '<input type="hidden" id="question" value="type"/>Press "1" If You Are a New Customer <br>Press "2" If You Are an Existing Customer'
        return message
    
    if user_message.lower() == '':
        return '<input type="hidden" id="question" value=""/>Please enter valid input and try again..' 

    # Save user input
    user_inputs.setdefault(customer_mobile, []).append({question: user_message})

    # Implement logic to determine the bot's response based on user input
    # For simplicity, using a default response

    if question.lower() == 'type':
        if user_message.lower() == "1":
            return '<input type="hidden" id="question" value="name"/>Please Enter Your Name'
        elif user_message.lower() == "2":
            return '<input type="hidden" id="question" value="type_2_mobile_number"/>Provide your registered Mobile No.'

    if question.lower() == 'name':
        name = user_message.strip()  # Remove extra spaces
        if name.replace(" ", "").isalpha():  # Check if the name contains only alphabetic characters after removing spaces
            user_inputs.setdefault(customer_mobile, []).append({'name': name})
            return f'<input type="hidden" id="question" value="mobile"/> {name.capitalize()}, Please Enter Your Mobile No..'
        else:
            return "Please enter a valid name without special characters or numbers."

    if question.lower() == 'mobile':
        mobile_no = user_message.strip()  # Remove extra spaces
        if len(mobile_no) == 10 and mobile_no.isdigit():
            user_inputs['customer_mobile'] = mobile_no  # Assuming 'customer_mobile' is the key for storing the mobile number
            return '<input type="hidden" id="question" value="interested"/>Are you Interested in <br> 1.Booking ?<br> 2.Deposit ?<br>3.Loan ?'
        else:
            return "Try again and Please enter a valid 10-digit mobile number please.."

    if question.lower() == 'interested':
        interested = user_message.lower()
        user_inputs[customer_mobile].append({'interested': interested})
        if interested == "1":
            return '<input type="hidden" id="question" value="b_weight_choose"/>Add product weight in grams'
        elif interested == "2":
            return '<input type="hidden" id="question" value="d_weight_choose"/>Add your weight in grams'
        elif interested == "3":
            return f'<input type="hidden" id="question" value="l_amount_eligibility"/>Your current loan eligibility is {10000} Rs. Would you like to proceed "Yes" OR "No"?'

    if question.lower() == 'b_weight_choose':
        if re.match(r'^[0-9]+$', user_message.strip()):  # Regex to match only numeric values
            weight_grams = int(user_message.strip())
            user_inputs[customer_mobile].append({'weight_grams': weight_grams})
            return '<input type="hidden" id="question" value="b_weight_approval"/><img src="https://styles.redditmedia.com/t5_4nujh4/styles/communityIcon_02ha8dpkjs771.png?width=256&s=b0a0aa984992c84ce5b9c174160bcf4b48e2fbe7"/> <br> You would like to proceed? <br> Give Answer in Yes Or No.'
        else:
            return "Please enter a valid numeric value for weight in grams."

    if question.lower() == 'b_weight_approval':
        if user_message.lower() == "no":
            return "For any information please contact us.<br> Thank You..!"
        elif user_message.lower() == "yes":
            return "See below payment Details. <img src='https://th.bing.com/th/id/OIP.wipp_FndsGLymq0SjO8yIwAAAA?pid=ImgDet&w=279&h=279&rs=1'><br> Thank you for your booking, our executive will connect with you shortly and provide a receipt and agreement. <br> Thank You..!"
        else:
            return "Please try again and use only 'yes' or 'no'"
        
    if question.lower() == 'd_weight_choose':
        user_inputs[customer_mobile].append({'weight_grams': user_message.lower()})
        return "Thank you for your interest our execative will connect you shortly and provide further details"

    if question.lower() == 'l_amount_eligibility':
        if user_message.lower() == "no":
            return "For any information please contact us.<br> Thank You..!"
        elif user_message.lower() == "yes":
            return "Thank you for your interest our execative will connect you shortly and provide further details"
        else:
            return "Please try again and use only 'yes' or 'no'"


#########################
    if question.lower() == 'type_2_mobile_number':
        registeredMobileNumber = user_message.strip()  # Remove leading/trailing spaces
        if registeredMobileNumber.isdigit() and len(registeredMobileNumber) == 10:
            # Assuming the predefined number to match is '1234567890'
            if registeredMobileNumber == '1234567890':
                name = 'Mayur Gulhane'
                return f'<input type="hidden" id="question" value="exisitng_customer_support_type"/>Welcome {name}, Let us know how we can support you? <br>1. Information on Existing Accounts <br>2. Product Information <br>3. New Purchase'
            else:
                return f'<input type="hidden" id="question" value=""/> Given number does not exist. Please try again..'
        else:
            return 'Please enter a valid 10-digit mobile number.'
    
    if question.lower() == 'exisitng_customer_support_type':   #########
        # url = "https://milan555.pythonanywhere.com/samples/"
        # data = {}
        # response = requests.get(url)

        # if response.status_code == 200:
        #     data = response.json()  # Convert the response to JSON format
        #     for item in data:
        #         print(item['title'])
        # else:
        # # Handle the case where the request was not successful
        #     print("Failed to fetch data from the URL")
        if user_message.lower() == "1":
            return f'<input type="hidden" id="question" value="exisitng_customer_support_type_1"/> <div style="color:red"> <i> Information on Existing Accounts Please start again. Thanks..</i></div>' #this info get from api in future ###TEST Purpose Data: {data} 
        if user_message.lower() == "2":
            return f'<input type="hidden" id="question" value="exisitng_customer_support_type_2"/> Following are our products <br>1. Booking <br>2. Deposite <br>3. Loan' #this info get from api in future
        if user_message.lower() == "3":
            return f'<input type="hidden" id="question" value="exisitng_customer_support_type_3"/> New purchase.. <br>Please Choose your product <br>1. Booking <br>2. Deposite <br>3. Loan'
        else:
            return 'Please try again and enter a valid input'
                   
    if question.lower() == 'exisitng_customer_support_type_2':
        if user_message.lower() == "1":
            return f'<input type="hidden" id="question" value="product_info_1_booking"/> <p>Lorem product info is available in 43 languages and offers more than 28 million reported accommodation listings, including over 6.6 million homes, apartments, and other unique places to stay.</p><img src="static/img/apple_logo.png" target="_blank"> <br>Our Product info available on our website <br>please visit on <a href="https://www.facebook.com">www.facebook.com</a> thanks..'
        if user_message.lower() == "2":
            return f'<input type="hidden" id="question" value="product_info_2_booking"/><i>In detailed information on deposite product <br></i>Our Product info available on our website <br>please visit on <a href="https://www.google.com" target="_blank">www.google.com</a> thanks..'
        if user_message.lower() == "3":
            return f'<input type="hidden" id="question" value="product_info_3_booking"/><i>Detailed informaiton on Loans scheme <br></i>Our Product info available on our loan website <br>please visit on <a href="https://www.facebook.com" target="_blank">www.facebook.com</a> thanks..'
        else:
            return 'Please try again and enter a valid input'        

    if question.lower() == 'exisitng_customer_support_type_3':
        interested = user_message.lower()
        user_inputs[customer_mobile].append({'interested': interested})
        if interested == "1":
            return '<input type="hidden" id="question" value="b_weight_choose_type3"/>Add product weight in grams'
        elif interested == "2":
            return '<input type="hidden" id="question" value="d_weight_choose_type3"/>Add your weight in grams'
        elif interested == "3":
            return f'<input type="hidden" id="question" value="l_amount_eligibility_type3"/>Your current loan eligibility is {10000} Rs. Would you like to proceed "Yes" OR "No"?'
        else:
            return 'Please try again and enter a valid input'
        
    if question.lower() == 'b_weight_choose_type3':
        user_inputs[customer_mobile].append({'weight_grams': user_message.lower()})
        return '<input type="hidden" id="question" value="b_weight_approval_type3"/><img src="https://styles.redditmedia.com/t5_4nujh4/styles/communityIcon_02ha8dpkjs771.png?width=256&s=b0a0aa984992c84ce5b9c174160bcf4b48e2fbe7"/> <br> You would like to proceed? <br> Give Answer in Yes Or No.'

    if question.lower() == 'b_weight_approval_type3':
        if user_message.lower() == "no":
            return "For any information please contact us.<br> Thank You..!"
        elif user_message.lower() == "yes":
            return "See below payment Details. <img src='https://th.bing.com/th/id/OIP.wipp_FndsGLymq0SjO8yIwAAAA?pid=ImgDet&w=279&h=279&rs=1'><br> Thank you for your booking, our executive will connect with you shortly and provide a receipt and agreement. <br> Thank You..!"
        else:
            return "Please try again and use only 'yes' or 'no'"
        
    if question.lower() == 'd_weight_choose_type3':
        user_inputs[customer_mobile].append({'weight_grams': user_message.lower()})
        return '<input type="hidden" id="question" value=""/> <p>Thank you for your interest our execative will connect you shortly and provide further details</p>'

    if question.lower() == 'l_amount_eligibility_type3':
        if user_message.lower() == "no":
            return "For any information please contact us.<br> Thank You..!"
        elif user_message.lower() == "yes":
            return "Thank you for your interest our execative will connect you shortly and provide further details"
        else:
            return "Please try again and use only 'yes' or 'no'"

    else:
        return "Oops..!! Please try again"

def process_user_input(request):
    user_message = request.GET.get('user_message', '')
    question = request.GET.get('question', '')
    customer_mobile = request.GET.get('customer_mobile', '')

    bot_response = get_bot_response(question, user_message, customer_mobile)

    # Save the user_inputs dictionary as a JSON file (for demonstration purposes)
    with open('user_inputs.json', 'w') as json_file:
        json.dump(user_inputs, json_file)

    return JsonResponse({'bot_response': bot_response})
