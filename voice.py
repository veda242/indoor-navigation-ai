import pyttsx3

engine = pyttsx3.init()

last_label = ""
last_suggestion = ""


def speak(label, suggestion, distance):
    global last_label, last_suggestion

    if (label != last_label or suggestion != last_suggestion) and distance != "FAR":
        message = f"{label} ahead, {suggestion}"
        engine.say(message)
        engine.runAndWait()

        last_label = label
        last_suggestion = suggestion