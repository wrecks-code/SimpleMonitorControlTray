import threading

from win10toast import ToastNotifier


def sendError(text):
    toaster = ToastNotifier()
    toaster.show_toast("Error", text, duration=7)


def sendNotification(text, duration):
    # toaster.show_toast("It's your first startup!", text, duration=duration)
    pass
