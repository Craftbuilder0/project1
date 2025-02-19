from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import speech_recognition as sr
from threading import Thread
import time
import smtplib
from email.mime.text import MIMEText

# ✅ Function to Send Email
def send_email(to, subject, message):
    sender_email = "foroption1@gmail.com"
    sender_password = "xuyvlkxyaatpfsjj"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# ✅ Kivy App Class
class ShadowCallApp(App):
    def build(self):
        self.keywords = ""
        self.contact = ""
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.keyword_input = TextInput(hint_text="Enter Keyworded Sentences", multiline=False)
        self.contact_input = TextInput(hint_text="Enter Email Address", multiline=False)
        self.status_label = Label(text="Status: Waiting...")

        start_btn = Button(text="Start Listening", on_press=self.start_listening)

        layout.add_widget(self.keyword_input)
        layout.add_widget(self.contact_input)
        layout.add_widget(start_btn)
        layout.add_widget(self.status_label)

        return layout
    
    # ✅ Function to Update UI Safely
    def update_status(self, message):
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', message), 0)

    # ✅ Start Listening Thread
    def start_listening(self, instance):
        self.keywords = self.keyword_input.text.lower()
        self.contact = self.contact_input.text

        if not self.keywords or not self.contact:
            self.update_status("Please enter both keyword and email!")
            return

        self.update_status("Listening for keyword...")
        Thread(target=self.listen_continuously, daemon=True).start()

    # ✅ Continuous Voice Recognition
    def listen_continuously(self):
        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as mic:  # Ensure proper microphone handling
                recognizer.adjust_for_ambient_noise(mic)
                print("Listening started...")

                while True:
                    try:
                        print("Listening...")
                        audio = recognizer.listen(mic)
                        detected_text = recognizer.recognize_google(audio).lower()
                        print(f"Detected: {detected_text}")

                        if self.keywords == detected_text:
                            self.update_status("Alert! Keyword detected! Sending Email...")
                            print("Voice matched!")
                            send_email(self.contact, 'Emergency', f"Emergency! Detected: {detected_text}")
                            print("Email Sent")
                            time.sleep(5)  # Prevent spamming
                        else:
                            self.update_status("Listening for keyword...")
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                    except sr.RequestError:
                        print("Could not request results; check internet connection")
                    except Exception as e:
                        print(f"Error: {e}")
                        self.update_status(f"Error: {e}")
                        time.sleep(2)
        except Exception as e:
            print(f"Microphone error: {e}")
            self.update_status(f"Microphone error: {e}")

# ✅ Run the App
if __name__ == "__main__":
    ShadowCallApp().run()
