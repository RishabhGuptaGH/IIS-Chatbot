import normalizer
import json
from voice import *
import pdf
import DBsetup
import translator

def load_symptoms_data(file_path):
    with open(file_path) as file:
        return json.load(file)

def extract_symptoms(content):
    all_symptoms = []
    for group in content["dermatology_symptoms"]:
        all_symptoms.append([group["category"]])
        all_symptoms.extend(group["symptoms"])
    return all_symptoms

def verify_symptoms(possibleSymptoms, all_symptoms):
    verifiedSymptoms = []
    currentCategory = all_symptoms[0][0]
    
    for symptom in all_symptoms:
        if isinstance(symptom, list):
            currentCategory = symptom
        if symptom in possibleSymptoms:
            verifiedSymptoms.append([currentCategory, symptom])
    return verifiedSymptoms

def ask_followup_questions(engine, verifiedSymptoms, content, mode, target_lang):
    replies = [
        "Thank you for sharing this detail. It helps me understand your situation better.",
        "Got it! This information is valuable for assessing your symptoms.",
        "Thanks for letting me know. It's important to track these things carefully."
    ]
    
    for symptomStorage in verifiedSymptoms:
        category = symptomStorage[0][0]
        questionDict = {}
        response_prompt = translator.translate(f"Please answer the following regarding {symptomStorage[1]}", target_lang)
        if mode == "voice":
            speak(engine, response_prompt)
        else:
            print(response_prompt)
        
        for categories in content["dermatology_symptoms"]:
            if categories["category"] == category:
                for i, question in enumerate(categories["followup_questions"]):
                    translated_question = translator.translate(question, target_lang)
                    if mode == "voice":
                        speak(engine, translated_question)
                        MyText = listen()
                    else:
                        MyText = input(translated_question + " ")
                    
                    if i == 0 and MyText:
                        response = translator.translate(f"We're sorry to hear that you have been experiencing it for {MyText}. Please know that you’re not alone.", target_lang)
                    elif MyText:
                        response = translator.translate(replies[i % len(replies)], target_lang)
                    else:
                        response = translator.translate("Thank you for your response. If you'd like to elaborate further, let me know.", target_lang)
                    
                    if mode == "voice":
                        speak(engine, response)
                    else:
                        print(response)
                    
                    questionDict[question] = MyText
                symptomStorage.append(questionDict)
    return verifiedSymptoms

def get_user_details(engine, mode, target_lang):
    user_details = {}

    prompts = [
        ("How old are you?", "Age"),
        ("What is your gender?", "Gender"),
        ("Lastly, can you please provide your phone number?", "Phone_number")
    ]
    
    while True:
        if mode == "voice":
            speak(engine, translator.translate("May I know your name?", target_lang))
            response = listen()
        else:
            response = input(translator.translate("May I know your name?", target_lang) + " ")
        
        if response.strip():
            user_details["Name"] = response.title()
            break
        else:
            if mode == "voice":
                speak(engine, translator.translate("I didn't catch that. Could you please repeat your name?", target_lang))
            else:
                print(translator.translate("Name is mandatory. Please enter your name.", target_lang))
    
    for prompt, key in prompts:
        if mode == "voice":
            speak(engine, translator.translate(prompt, target_lang))
            response = listen()
        else:
            response = input(translator.translate(prompt, target_lang) + " ")
        user_details[key] = response.title() if key == "Name" else response
        print(f"{key} detected as: {user_details[key]}")
    
    return user_details

def main():
    engine = initialize_engine()
    print("Welcome to the dermatological healthcare chatbot!")
    
    mode = input("Would you like to communicate via text or voice? (Enter 'text' or 'voice'): ").strip().lower()
    while mode not in ["text", "voice"]:
        mode = input("Invalid input. Please enter 'text' or 'voice': ").strip().lower()

    user_lang = input("Enter the language in which you want chatbot to be used: ")
    if user_lang not in translator.languages:
        print("Unsupported language. Defaulting to English.")
        user_lang = "English"
    target_lang = user_lang

    welcome_message = translator.translate("Welcome to the dermatological healthcare chatbot!", target_lang)
    if mode == "voice":
        speak(engine, welcome_message)
    else:
        print(welcome_message)
    
    user_details = get_user_details(engine, mode, target_lang)
    
    assistance_prompt = translator.translate("Now, how may I assist you with your dermatological concerns today?", target_lang)
    if mode == "voice":
        speak(engine, assistance_prompt)
        user_input = listen()
    else:
        user_input = input(assistance_prompt + " ")
    
    if not user_input:
        error_message = translator.translate("No input detected. Please try again.", target_lang)
        if mode == "voice":
            speak(engine, error_message)
        else:
            print(error_message)
        return
    
    possibleSymptoms = normalizer.text_normalizer(user_input)
    content = load_symptoms_data("_newSymptoms.json")
    all_symptoms = extract_symptoms(content)
    verifiedSymptoms = verify_symptoms(possibleSymptoms, all_symptoms)
    
    if not verifiedSymptoms:
        print(translator.translate("No symptoms detected. Please try rephrasing your input or providing more details.", target_lang))
        return
    
    print(translator.translate("The identified symptoms are:", target_lang))
    for observedSymptoms in verifiedSymptoms:
        print(translator.translate(observedSymptoms[1], target_lang))
    
    verifiedSymptoms = ask_followup_questions(engine, verifiedSymptoms, content, mode, target_lang)
    
    closing_message = translator.translate("Your information has been recorded and a PDF has been generated. Have a great day!", target_lang)
    print(closing_message)
    
    pdf.final_report(user_details, verifiedSymptoms)
    DBsetup.setup_database(user_details, verifiedSymptoms)
    
if __name__ == "__main__":
    main()
