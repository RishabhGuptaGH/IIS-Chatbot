import speech_recognition as sr
import pyttsx3

r= sr.Recognizer()
engine = pyttsx3.init()

def speak(command):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id) 
    engine.setProperty('rate', 150)   
    engine.setProperty('volume', 1.0)
    engine.say(command)
    engine.runAndWait()

def voice():
    print("Welcome to voice based chatbot")
    speak("Hello! I am a Dermatological Healthcare chatbot. How may I help you today?")
    try:
        with sr.Microphone() as source:
            print("Listening...")
                
            r.adjust_for_ambient_noise(source, duration=0.5)
                
            audio = r.listen(source)
                
            MyText = r.recognize_google(audio)
            MyText = MyText.lower()

    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.UnknownValueError:
        print("Sorry, I did not catch that. Please try again.")

    possibleSymptoms = normalizer.textNormalizer(MyText)
    all_symptoms = []

    with open("symptoms.json") as file:
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

        if len(verifiedSymptoms) == 0:
            speak("No symptoms detected. Please try rephrasing your input or providing more details.")
            quit()

        speak("The identified symptoms are")
        for observedSymptoms in verifiedSymptoms:
            speak(observedSymptoms[1])

        replies = [
            "Thank you for sharing this detail. It helps me understand your situation better.",
            "Got it! This information is valuable for assessing your symptoms.",
            "Thanks for letting me know. It’s important to track these things carefully."
        ]

        for symptomStorage in verifiedSymptoms:
            category= symptomStorage[0][0]
            questionDict= {}
            speak("Please answer the following regarding")
            speak(symptomStorage[1])
            for categories in content["dermatology_symptoms"]:
                if categories["category"]== category:
                    for i, question in enumerate(categories["followup_questions"]):
                        speak(question)   
                        try:
                            with sr.Microphone() as source:
                                print("Listening...")
                                    
                                r.adjust_for_ambient_noise(source, duration=0.5)
                                    
                                audio = r.listen(source)
                                    
                                MyText = r.recognize_google(audio)
                                MyText = MyText.lower()

                        except sr.RequestError as e:
                            print(f"Could not request results; {e}")
                        except sr.UnknownValueError:
                            print("Sorry, I did not catch that. Please try again.")

                        if i==0 and MyText: 
                            speak(f"We're sorry to hear that you have been experiencing it for {MyText}. Please know that you’re not alone.")
                        elif MyText:  
                            reply= replies[i%len(replies)]
                            speak(reply)
                        else: 
                            speak("Thank you for your response. If you'd like to elaborate further, let me know.")

                        questionDict[question] = MyText
                    symptomStorage.append(questionDict)
                    print("\n")

        print("\nChatbot: Thank you for your responses! Here's what I've gathered:\n")
        for symptom in verifiedSymptoms:
            print(f"- Symptom: {symptom[1]}")
            print("  Follow-up Responses:")
            for question, answer in symptom[2].items(): 
                print(f"    {question}: {answer}")

        speak("Your information has been recorded. Have a great day!")

        dataStorageList = verifiedSymptoms

  voice()
