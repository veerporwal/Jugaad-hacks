import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr

class AutoNoteTakingApp:
    def _init_(self, master):
        self.master = master
        master.title("Auto Note Taking App")

        self.transcribed_text = ""

        self.label = tk.Label(master, text="Auto Note Taking App")
        self.label.pack()

        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.transcribed_text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.transcribed_text_area.pack()

        self.save_button = tk.Button(master, text="Save Notes", command=self.save_notes)
        self.save_button.pack()

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.transcribed_text_area.delete('1.0', tk.END)

        recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        with self.microphone as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        try:
            self.transcribed_text = recognizer.recognize_google(audio)
            print("Transcribed Text:", self.transcribed_text)
            self.transcribed_text_area.insert(tk.END, self.transcribed_text)
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    def stop_recording(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        if hasattr(self, 'microphone'):
            self.microphone._exit_(None, None, None)

    def save_notes(self):
        if self.transcribed_text:
            with open("meeting_notes.txt", "w") as file:
                file.write(self.transcribed_text)
                print("Notes saved to 'meeting_notes.txt'")

def main():
    root = tk.Tk()
    app = AutoNoteTakingApp(root)
    root.mainloop()

if _name_ == "_main_":
    main()
