import threading
import webbrowser
from app import run_flask
from mouse_control import run_gesture

# Open website automatically
webbrowser.open("http://127.0.0.1:5000")

# Create threads
t1 = threading.Thread(target=run_flask)
t2 = threading.Thread(target=run_gesture)

# Start both
t1.start()
t2.start()

# Keep running
t1.join()
t2.join()