from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from plyer import notification
import datetime
import random
from kivy.uix.widget import Widget

# Motivational quotes
quotes = [
    "Believe you can and you're halfway there.",
    "Success is no accident. It's hard work and persistence.",
    "Push yourself because no one else is going to do it for you.",
    "Dream big, work hard, stay focused, and surround yourself with good people.",
    "Your only limit is your mind.",
    "I know my kudu will give me the crown of pride.",
    "This is your last chance to prove yourself",
    "You are the only person who can make this work.",
    "Your success is the loudest slap in the face of your abusers"
]

# Custom widget for dynamic gradient background
class GradientBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rect = None
        self.update_gradient()  # Initial gradient creation

    def update_gradient(self, *args):
        # Clear previous gradient if exists
        self.canvas.clear()

        with self.canvas:
            # Create gradient background (linear gradient)
            Color(0.5, 0.2, 0.7)  # Starting color
            self.rect = Rectangle(size=self.size, pos=self.pos)
            # Update the gradient size and position to match the window's size
            self.bind(size=self.update_gradient, pos=self.update_gradient)

class NEETApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.exam_date = None  # Initialize exam date variable

    def set_date(self):
        # Get selected year, month, day
        year = int(self.ids.year_spinner.text)
        month = int(self.ids.month_spinner.text)
        day = int(self.ids.day_spinner.text)
        
        try:
            self.exam_date = datetime.date(year, month, day)
            self.update_countdown()
            Clock.schedule_interval(self.update_countdown, 0.01)  # Update every 0.01 seconds for sub-seconds
        except ValueError:
            self.ids.countdown_label.text = "Invalid Date! Please select a valid date."

    def update_countdown(self, *args):
        if self.exam_date:
            now = datetime.datetime.now()
            exam_datetime = datetime.datetime.combine(self.exam_date, datetime.datetime.min.time())
            delta = exam_datetime - now

            if delta.total_seconds() > 0:
                days = delta.days
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                microseconds = int(delta.microseconds / 1000)  # Convert to milliseconds
                self.ids.countdown_label.text = (
                    f"Countdown: {days} days, {hours} hours, {minutes} minutes, "
                    f"{seconds}.{microseconds:03d} seconds"
                )
            else:
                self.ids.countdown_label.text = "Exam Date Reached!"

    def set_reminder(self):
        notification.notify(
            title="NEET Reminder",
            message="Stay focused! Keep working hard for your NEET exam.",
            timeout=10
        )

    def get_random_quote(self):
        return random.choice(quotes)

class NEETAppMain(App):
    def build(self):
        return NEETApp()

if __name__ == '__main__':
    NEETAppMain().run()
