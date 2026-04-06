# Gesture Control Virtual System

## Overview

The Gesture Control Virtual System is a Human-Computer Interaction (HCI) project that enables users to control a computer using hand gestures instead of traditional input devices such as a mouse or keyboard. The system captures real-time video through a webcam and applies computer vision techniques to detect and track hand movements. By using MediaPipe’s hand landmark detection, it identifies key points on the hand and maps them to specific system-level actions.

The main objective of this project is to provide a touchless, intuitive, and efficient method of interacting with computers. This approach reduces dependency on physical hardware and improves usability in environments where direct contact with devices is not preferred.

## Features

* Cursor movement controlled by index finger tracking
* Click functionality using pinch gesture (thumb and index finger)
* Scroll up and scroll down using predefined finger combinations
* Screenshot capture using a custom gesture
* Real-time hand tracking and gesture recognition
* Integrated frontend interface for project demonstration

## Technology Stack

* Python for backend implementation
* OpenCV for video capture and image processing
* MediaPipe for hand detection and landmark tracking
* PyAutoGUI for simulating mouse and system controls
* Flask for backend integration with frontend
* HTML and CSS for frontend interface

## Project Structure

gesture-control/
│
├── main.py
├── mouse_control.py
├── templates/
│   └── index.html
├── static/
│   └── style.css

## How It Works

The system captures live video input using a webcam. Each frame is processed using MediaPipe to detect hand landmarks. Based on the position and combination of fingers, specific gestures are recognized. These gestures are then mapped to actions such as moving the cursor, clicking, scrolling, or taking screenshots using PyAutoGUI.

## Installation and Setup

1. Clone the repository
2. Install required dependencies:
   pip install opencv-python mediapipe pyautogui flask
3. Run the main application:
   python main.py
4. Open a browser and go to:
   http://127.0.0.1:5000

## Applications

* Touchless interfaces in healthcare and public systems
* Interactive presentations and smart classrooms
* Assistive technology for accessibility
* Smart home and IoT control systems

## Limitations

* Requires proper lighting conditions for accurate detection
* Performance may vary depending on camera quality and system specifications
* Limited gesture set in the current implementation

## Future Enhancements

* Implementation of machine learning models for improved accuracy
* Custom gesture configuration by users
* Integration with voice commands
* Support for multiple hand tracking and advanced gestures
* Cross-platform optimization

## Conclusion

The Gesture Control Virtual System demonstrates how computer vision can be used to create natural and efficient interaction methods. It provides a foundation for developing advanced touchless systems and highlights the potential of gesture-based interfaces in modern computing environments.
