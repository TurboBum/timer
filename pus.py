from notifypy import Notify

def push_message(title, message, icon=None):
    notification = Notify()
    notification.title = title
    notification.message = message
    notification.icon = icon
    notification.send()