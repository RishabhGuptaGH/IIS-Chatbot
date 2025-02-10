import normalizer
import json
from voice import *
import pdf

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

def ask_followup_questions(engine, verifiedSymptoms, content):
    replies = [
        "Thank you for sharing this detail. It helps me understand your situation better.",
        "Got it! This information is valuable for assessing your symptoms.",
        "Thanks for letting me know. It's important to track these things carefully."
    ]
    
    for symptomStorage in verifiedSymptoms:
        category = symptomStorage[0][0]
        questionDict = {}
        speak(engine, f"Please answer the following regarding {symptomStorage[1]}")
        
        for categories in content["dermatology_symptoms"]:
            if categories["category"] == category:
                for i, question in enumerate(categories["followup_questions"]):
                    speak(engine, question)
                    MyText = listen()
                    
                    if i == 0 and MyText:
                        speak(engine, f"We're sorry to hear that you have been experiencing it for {MyText}. Please know that you’re not alone.")
                    elif MyText:
                        speak(engine, replies[i % len(replies)])
                    else:
                        speak(engine, "Thank you for your response. If you'd like to elaborate further, let me know.")
                    
                    questionDict[question] = MyText
                symptomStorage.append(questionDict)
    return verifiedSymptoms

def get_user_details(engine):
    user_details = {}

    speak(engine, "May I know your name?")
    user_details["Name"] = listen().title()
    print(f"Name detected as: {user_details["Name"]}")

    speak(engine, "How old are you?")
    user_details["Age"] = listen()
    print(f"Age detected as: {user_details["Age"]}")

    speak(engine, "What is your gender?")
    user_details["Gender"] = listen()
    print(f"Gender detected as: {user_details["Gender"]}")

    speak(engine, "Lastly, can you please provide your phone number?")
    user_details["Phone_number"] = listen()
    print(f"Phone Number detected as: {user_details["Phone_number"]}")

    return user_details

def main():
    engine = initialize_engine()
    print("Welcome to voice-based chatbot")
    speak(engine, "Hello! I am a Dermatological Healthcare chatbot. Before we proceed, I need to collect some basic details.")

    user_details = get_user_details(engine)

    speak(engine, "Now, how may I assist you with your dermatological concerns today?")
    
    user_input = listen()
    if not user_input:
        speak(engine, "No input detected. Please try again.")
        return
    
    possibleSymptoms = normalizer.text_normalizer(user_input)
    content = load_symptoms_data("_newSymptoms.json")
    all_symptoms = extract_symptoms(content)
    verifiedSymptoms = verify_symptoms(possibleSymptoms, all_symptoms)
    
    if not verifiedSymptoms:
        speak(engine, "No symptoms detected. Please try rephrasing your input or providing more details.")
        return
    
    speak(engine, "The identified symptoms are")
    for observedSymptoms in verifiedSymptoms:
        speak(engine, observedSymptoms[1])
    
    verifiedSymptoms = ask_followup_questions(engine, verifiedSymptoms, content)
    
    speak(engine, "Your information has been recorded and PDF has been generated. Have a great day!")

    pdf.final_report(user_details,verifiedSymptoms)
    
if __name__ == "__main__":
    main()
