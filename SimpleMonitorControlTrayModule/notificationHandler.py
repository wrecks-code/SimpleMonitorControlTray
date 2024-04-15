import threading

from win10toast import ToastNotifier


# TODO: add Logic
def sendError(text):
    toaster = ToastNotifier()
    toaster.show_toast("Error", text, duration=7)


def sendNotification(text, duration):
    def show_notification():
        toaster = ToastNotifier()
        toaster.show_toast("It's your first startup!", text, duration=duration)

    notification_thread = threading.Thread(target=show_notification)
    notification_thread.start()
