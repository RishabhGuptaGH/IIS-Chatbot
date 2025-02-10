import normalizer
import json
import fpdf


def symptomDetection():
    userInput = input("Chatbot: Hello! I am a Dermatological Healthcare chatbot. How may I help you today?\nUser: ")
    possibleSymptoms = normalizer.textNormalizer(userInput)
    all_symptoms = []
    
    with open("new_symptoms.json") as file:
        content = json.load(file)
        for groups in content["dermatology_symptoms"]:
            all_symptoms.extend([[groups["category"]]])
            all_symptoms.extend(groups["symptoms"])
        
        verifiedSymptoms = []
        currentCategory = all_symptoms[0][0]

        for symptom in all_symptoms:
            if type(symptom) == list:
                currentCategory = symptom
            if symptom in possibleSymptoms:
                verifiedSymptoms.append([currentCategory, symptom])

        print("\n")
        if len(verifiedSymptoms) == 0:
            print("\nChatbot: No symptoms detected. Please try rephrasing your input or providing more details.")
            quit()

        print("Chatbot: The identified symptoms are: ", end="")
        for observedSymptoms in verifiedSymptoms:
            print(observedSymptoms[1], end="   ")
        print(end="\n\n")

        return verifiedSymptoms



def followupQuestions(verifiedSymptoms,replies):
    file = open("new_symptoms.json",'r')
    content = json.load(file) 
    for symptomStorage in verifiedSymptoms:
        category= symptomStorage[0][0]
        questionDict= {}
        print(f"Chatbot: Please answer the following regarding {symptomStorage[1]}:", end="\n\n")
        for categories in content["dermatology_symptoms"]:
            if categories["category"]== category:
                for i, question in enumerate(categories["followup_questions"]):
                    response = input(f"Chatbot: {question}\nUser: ").strip()

                    if i==0 and response: 
                        print(f"Chatbot: We're sorry to hear that you have been experiencing it for {response}. Please know that you’re not alone.")
                    elif response:  
                        reply= replies[i%len(replies)]
                        print(f"Chatbot: {reply}")
                    else: 
                        print("Chatbot: Thank you for your response. If you'd like to elaborate further, let me know.")

                    questionDict[question] = response
                symptomStorage.append(questionDict)
                print("\n")



def textConfirmation(verifiedSymptoms):
    print("\nChatbot: Thank you for your responses! Here's what I've gathered:\n")
    for symptom in verifiedSymptoms:
        print(f"- Symptom: {symptom[1]}")
        print("  Follow-up Responses:")
        for question, answer in symptom[2].items(): 
            print(f"    {question}: {answer}")
        
    print("\nChatbot: Your information has been recorded. Have a great day!")



def chatbot():

    replies = [
        "Thank you for sharing this detail. It helps me understand your situation better.",
        "Got it! This information is valuable for assessing your symptoms.",
        "Thanks for letting me know. It’s important to track these things carefully."
    ] 

    verifiedSymptoms = symptomDetection()
    
    followupQuestions(verifiedSymptoms,replies)    

    textConfirmation(verifiedSymptoms)

    print(verifiedSymptoms)

if __name__ == "__main__":
    chatbot()