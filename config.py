question_and_information = ""  # todo fix variable, I need to be able to change it, and update it of web instantly on the web (using http request)
number_response = 0
# number_response = config.number_response
# question_and_information = config.question_and_information
def update_config(new_question_and_information, new_number_response):
    global question_and_information, number_response
    question_and_information = new_question_and_information
    number_response = new_number_response
    print("using update_config")