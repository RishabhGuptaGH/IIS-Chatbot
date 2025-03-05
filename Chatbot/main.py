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

def ask_followup_questions(engine, verifiedSymptoms, content, mode):
    replies = [
        "Thank you for sharing this detail. It helps me understand your situation better.",
        "Got it! This information is valuable for assessing your symptoms.",
        "Thanks for letting me know. It's important to track these things carefully."
    ]
    
    for symptomStorage in verifiedSymptoms:
        category = symptomStorage[0][0]
        questionDict = {}
        response_prompt = f"Please answer the following regarding {symptomStorage[1]}"
        if mode == "voice":
            speak(engine, response_prompt)
        else:
            print(response_prompt)
        
        for categories in content["dermatology_symptoms"]:
            if categories["category"] == category:
                for i, question in enumerate(categories["followup_questions"]):
                    if mode == "voice":
                        speak(engine, question)
                        MyText = listen()
                    else:
                        MyText = input(question + " ")
                    
                    if i == 0 and MyText:
                        response = f"We're sorry to hear that you have been experiencing it for {MyText}. Please know that you’re not alone."
                    elif MyText:
                        response = replies[i % len(replies)]
                    else:
                        response = "Thank you for your response. If you'd like to elaborate further, let me know."
                    
                    if mode == "voice":
                        speak(engine, response)
                    else:
                        print(response)
                    
                    questionDict[question] = MyText
                symptomStorage.append(questionDict)
    return verifiedSymptoms

def get_user_details(engine, mode):
    user_details = {}

    prompts = [
        ("May I know your name?", "Name"),
        ("How old are you?", "Age"),
        ("What is your gender?", "Gender"),
        ("Lastly, can you please provide your phone number?", "Phone_number")
    ]
    
    for prompt, key in prompts:
        if mode == "voice":
            speak(engine, prompt)
            response = listen()
        else:
            response = input(prompt + " ")
        user_details[key] = response.title() if key == "Name" else response
        print(f"{key} detected as: {user_details[key]}")
    
    return user_details

def main():
    engine = initialize_engine()
    print("Welcome to the dermatological healthcare chatbot!")
    
    mode = input("Would you like to communicate via text or voice? (Enter 'text' or 'voice'): ").strip().lower()
    while mode not in ["text", "voice"]:
        mode = input("Invalid input. Please enter 'text' or 'voice': ").strip().lower()
    
    if mode == "voice":
        speak(engine, "Hello! I am a Dermatological Healthcare chatbot. Before we proceed, I need to collect some basic details.")
    else:
        print("Hello! I am a Dermatological Healthcare chatbot. Before we proceed, I need to collect some basic details.")
    
    user_details = get_user_details(engine, mode)
    
    if mode == "voice":
        speak(engine, "Now, how may I assist you with your dermatological concerns today?")
        user_input = listen()
    else:
        user_input = input("Now, how may I assist you with your dermatological concerns today? ")
    
    if not user_input:
        if mode == "voice":
            speak(engine, "No input detected. Please try again.")
        else:
            print("No input detected. Please try again.")
        return
    
    possibleSymptoms = normalizer.text_normalizer(user_input)
    content = load_symptoms_data("_newSymptoms.json")
    all_symptoms = extract_symptoms(content)
    verifiedSymptoms = verify_symptoms(possibleSymptoms, all_symptoms)
    
    if not verifiedSymptoms:
        if mode == "voice":
            speak(engine, "No symptoms detected. Please try rephrasing your input or providing more details.")
        else:
            print("No symptoms detected. Please try rephrasing your input or providing more details.")
        return
    
    if mode == "voice":
        speak(engine, "The identified symptoms are:")
    else:
        print("The identified symptoms are:")
    
    for observedSymptoms in verifiedSymptoms:
        if mode == "voice":
            speak(engine, observedSymptoms[1])
        else:
            print(observedSymptoms[1])
    
    verifiedSymptoms = ask_followup_questions(engine, verifiedSymptoms, content, mode)
    
    if mode == "voice":
        speak(engine, "Your information has been recorded and a PDF has been generated. Have a great day!")
    else:
        print("Your information has been recorded and a PDF has been generated. Have a great day!")
    
    pdf.final_report(user_details, verifiedSymptoms)
    
if __name__ == "__main__":
    main()
