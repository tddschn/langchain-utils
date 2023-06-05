def send_notification(
    message='Prompt copied to clipboard',
    activate='com.lencx.chatgpt',
    title='langchain-utils',
    appIcon=None,
):
    """Sends a notification using the pync library."""

    try:
        import pync
    except ImportError:
        print(
            "Please install pync to use the notification feature on macOS: pip install pync"
        )
        return

    notification_args = {"title": title, "activate": activate}

    if appIcon is not None:
        notification_args["appIcon"] = appIcon

    pync.notify(message, **notification_args)
