from notifypy import Notify

def push_message(name, title, message, icon=None):
    notification = Notify()
    notification.application_name = name
    notification.title = title
    notification.message = message
    if icon is not None:
        notification.icon = icon
    notification.send()