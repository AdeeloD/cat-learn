from tkinter import *
from tkinter import messagebox
import math
import os
import pygame


# Constants
BLACK = "#000000"
RED = "#e7305b"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15

STUDY_TIPS = [
    "Focus on one topic at a time",
    "Take brief notes during work sessions",
    "Review your notes during breaks",
    "Stay hydrated during study sessions",
    "Use active recall techniques",
    "Try explaining concepts out loud"
]


class PomodoroLearningTimer:
    def __init__(self):
        self.window = Tk()
        self.window.title("Study with my Cat")
        self.window.config(padx=50, pady=25, bg=RED)
        self.reps = 0
        self.timer = None
        self.running = False
        self.current_tip = 0


        pygame.mixer.init()

        self.setup_ui()

    def setup_ui(self):
        # Title Label
        self.title_label = Label(
            text="Meow Learning",
            font=(FONT_NAME, 30, "bold"),
            fg=BLACK,
            bg=RED
        )
        self.title_label.grid(column=1, row=0, pady=10)

        # Cat Image
        self.canvas = Canvas(width=200, height=200, bg=RED, highlightthickness=0)
        try:
            self.catimg = PhotoImage(file="cat.png")
            self.resized_catimg = self.catimg.subsample(3, 3)  # Making it a bit smaller
            self.canvas.create_image(100, 100, image=self.resized_catimg, anchor="center")
        except TclError:
            print("Warning: Cat image not found!")
        self.canvas.grid(column=1, row=1)

        # Study Tip Label
        self.tip_label = Label(
            text="Tip: " + STUDY_TIPS[0],
            font=(FONT_NAME, 12),
            fg=BLACK,
            bg=RED,
            wraplength=300
        )
        self.tip_label.grid(column=1, row=2, pady=10)

        # Timer Frame
        timer_frame = Frame(self.window, bg=RED)
        timer_frame.grid(column=1, row=3, pady=20)

        # Timer Text
        self.timer_text = Label(
            timer_frame,
            text="00:00",
            font=(FONT_NAME, 35, "bold"),
            fg=BLACK,
            bg=RED
        )
        self.timer_text.pack()

        # Session Counter
        self.session_label = Label(
            timer_frame,
            text="Session: 0/4",
            font=(FONT_NAME, 12),
            fg=BLACK,
            bg=RED
        )
        self.session_label.pack(pady=5)

        # Buttons Frame
        button_frame = Frame(self.window, bg=RED)
        button_frame.grid(column=1, row=4, pady=10)

        # Start Button
        self.start_button = Button(
            button_frame,
            text="Start",
            command=self.start_timer,
            font=(FONT_NAME, 12, "bold"),
            width=10,
            fg=BLACK,
            bg=RED
        )
        self.start_button.pack(side=LEFT, padx=5)

        # Pause Button
        self.pause_button = Button(
            button_frame,
            text="Pause",
            command=self.pause_timer,
            font=(FONT_NAME, 12, "bold"),
            width=10,
            fg=BLACK,
            bg=RED,
            state=DISABLED
        )
        self.pause_button.pack(side=LEFT, padx=5)

        # Reset Button
        self.reset_button = Button(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            font=(FONT_NAME, 12, "bold"),
            width=10,
            fg=BLACK,
            bg=RED
        )
        self.reset_button.pack(side=LEFT, padx=5)

        # Progress Frame
        progress_frame = Frame(self.window, bg=RED)
        progress_frame.grid(column=1, row=5, pady=10)

        # Checkmarks
        self.check_marks = Label(
            progress_frame,
            text="",
            fg=BLACK,
            bg=RED,
            font=(FONT_NAME, 15, "bold")
        )
        self.check_marks.pack()

    def play_sound(self):
        try:
            pygame.mixer.music.load("alarm.mp3")
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    def show_next_tip(self):
        self.current_tip = (self.current_tip + 1) % len(STUDY_TIPS)
        self.tip_label.config(text="Tip: " + STUDY_TIPS[self.current_tip])

    def reset_timer(self):
        self.window.after_cancel(self.timer)
        self.timer_text.config(text="00:00")
        self.title_label.config(text="Meow Learning")
        self.check_marks.config(text="")
        self.session_label.config(text="Session: 0/4")
        self.reps = 0
        self.running = False
        self.start_button.config(state=NORMAL)
        self.pause_button.config(state=DISABLED)
        self.show_next_tip()

    def start_timer(self):
        self.running = True
        self.start_button.config(state=DISABLED)
        self.pause_button.config(state=NORMAL)
        self.reps += 1

        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if self.reps % 8 == 0:
            self.count_down(long_break_sec)
            self.title_label.config(text="Long Break!", fg=BLACK)
            self.notify_user("Time for a long break! Take 15 minutes to refresh.")
        elif self.reps % 2 == 0:
            self.count_down(short_break_sec)
            self.title_label.config(text="Short Break!", fg=BLACK)
            self.notify_user("Quick 5-minute break! Stand up and stretch.")
        else:
            self.count_down(work_sec)
            self.title_label.config(text="Meow Learning", fg=BLACK)
            self.notify_user("Focus time! 25 minutes of concentrated study.")
            current_session = math.ceil(self.reps / 2)
            self.session_label.config(text=f"Session: {current_session}/4")

    def pause_timer(self):
        if self.running:
            self.running = False
            self.start_button.config(state=NORMAL)
            self.pause_button.config(state=DISABLED)
            if self.timer:
                self.window.after_cancel(self.timer)

    def notify_user(self, message):
        try:
            if os.name == "posix":  # Linux/Unix
                os.system(f'notify-send "Study with Cat" "{message}"')
            elif os.name == "nt":  # Windows
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast("Study with Cat", message, duration=5)
        except Exception as e:
            print(f"Notification error: {e}")

    def count_down(self, count):
        if not self.running:
            return

        minutes = math.floor(count / 60)
        seconds = count % 60

        self.timer_text.config(text=f"{minutes:02d}:{seconds:02d}")

        if count > 0:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        else:
            self.play_sound()
            if self.reps % 2 == 0:
                completed_sessions = math.floor(self.reps / 2)
                self.check_marks.config(text="✓" * completed_sessions)
                if completed_sessions >= 4:
                    messagebox.showinfo(
                        "Congratulations!",
                        "You've completed a full Pomodoro cycle!\nTake a longer break and reflect on what you've learned."
                    )
                    self.reset_timer()
                else:
                    self.show_next_tip()
                    self.start_button.config(state=NORMAL)
                    self.pause_button.config(state=DISABLED)
            else:
                self.start_button.config(state=NORMAL)
                self.pause_button.config(state=DISABLED)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = PomodoroLearningTimer()
    app.run()
