# Joity-AI-Powered-Assistive-System-for-Visually-Impaired-Individuals
AI-powered assistive system for visually impaired individuals integrating autonomous navigation, AI-based currency recognition, GPS tracking, and safety features.

# Funding Acknowledgement
This project was developed as part of a government-funded research and innovation initiative, selected through a competitive funding process under the ICT Division, Government of the People’s Republic of Bangladesh.
The project received financial and institutional support from the ICT Division to facilitate the research, development, and prototyping of an assistive technology system aimed at improving the independence, safety, and mobility of visually impaired individuals.
We gratefully acknowledge the ICT Division, Government of the People’s Republic of Bangladesh, for its valuable support and funding, which enabled the successful development and implementation of this socially impactful project.

# Project Features
Joity is an integrated assistive technology system developed to support the independent mobility, financial management, safety, and remote monitoring of visually impaired individuals. The project combines autonomous vehicle technology, computer vision, machine learning, GPS/GSM communication, and multiple safety mechanisms into a unified prototype. Its autonomous car uses Raspberry Pi-based image processing for lane detection and navigation, while YOLOv8 enables real-time stop-sign and obstacle detection. The system also incorporates an AI-based currency counter that evolved from a color-sensor-based approach to Haar Cascade, and finally YOLOv11-based currency recognition, enabling multiple Bangladeshi currency notes to be detected from a single frame with improved accuracy. For remote monitoring, GPS and GSM technologies provide real-time location information through SMS, calls, and the Traccar tracking platform, allowing family members or caregivers to monitor the user's location. In addition, automated door locking, fire detection, and anti-theft mechanisms are integrated to enhance the overall safety and security of the user. Together, these features provide a comprehensive assistive platform aimed at improving independence, accessibility, and confidence in the daily activities of visually impaired individuals.
# The key features of the project are listed below:
# Autonomous Navigation System
•	Lane detection using image processing and OpenCV
•	Bird's-eye view transformation for road analysis
•	Real-time steering control
•	Automatic U-turn functionality
•	Stop sign detection using YOLOv8
•	Obstacle detection and avoidance
•	Raspberry Pi-based autonomous driving prototype
# AI-Based Currency Recognition
# Three-stage evolution of the currency recognition system:
# Stage 1: Arduino + Color Sensor
•	Taka note recognition using TCS3200 sensor
•	Wallet balance management
•	Audio feedback for users
# Stage 2: Machine Learning Approach
•	Haar Cascade Classifier implementation
•	Raspberry Pi-based image processing
# Stage 3: Deep Learning Enhancement
•	Currency detection using YOLOv11
•	Multiple note recognition in a single frame
•	Detection accuracy: 87.3% – 99.5%
•	Dataset annotation using Label Studio
•	Model training using Google Colab
# GPS Tracking and Monitoring
•	Real-time location tracking
•	GPS-based coordinate acquisition
•	GSM communication module
•	SMS location sharing
•	Google Maps integration
•	Remote monitoring using Traccar
# Safety Features
•	Automatic door lock system
•	Fire detection and alarm
•	Anti-theft protection
•	User presence detection
•	Servo-controlled access mechanism
________________________________________
# System Architecture
The Joity system is designed as a modular assistive technology platform consisting of four major subsystems: autonomous navigation, currency recognition, GPS-based tracking, and user safety. These subsystems operate through a combination of Raspberry Pi and Arduino-based processing units, cameras, sensors, communication modules, and machine learning models. The autonomous navigation subsystem processes camera input for lane detection and uses YOLOv8 for stop-sign and obstacle detection, while the currency subsystem provides progressively improved Bangladeshi currency recognition through color sensing, Haar Cascade, and YOLOv11. The GPS tracking subsystem combines GPS and GSM technologies with the Traccar platform for location monitoring, while additional safety mechanisms provide protection through automated door locking, fire detection, and anti-theft functionality. The overall system architecture is shown in the picture segment.

# Hardware Components
The prototype integrates multiple hardware components to implement its navigation, recognition, tracking, and safety functions. Raspberry Pi 5 serves as the primary processing platform for the autonomous car, while Raspberry Pi 3B+ is used for the currency recognition subsystem. Arduino Uno is utilized for the tracking subsystem and supporting control operations. Cameras provide visual input for computer vision tasks, while the motor driver, GPS, GSM, sensors, servo motors, LCD, and other peripheral modules enable physical movement, communication, monitoring, and safety functions.
# The major hardware components used in the project are listed below:
•	Raspberry Pi 5
•	Raspberry Pi 3B+
•	Arduino Uno
•	Raspberry Pi Camera Modules
•	L298N Motor Driver
•	GPS Module
•	GSM Module
•	Ultrasonic Sensors
•	Infrared Sensors
•	Servo Motors
•	LCD Display
•	Flame Sensor
•	Speaker Module

# Software & AI Technologies
The project combines conventional image processing with machine learning and deep learning techniques to implement intelligent assistive functions. Python and OpenCV are used for image acquisition and processing, particularly for lane detection and autonomous vehicle control. YOLOv8 is employed for stop-sign and obstacle detection, while YOLOv11 is used for advanced currency recognition and multiple-note detection. A Haar Cascade Classifier was also implemented as an intermediate machine learning approach for currency detection. Dataset annotation and model development were supported using Label Studio and Google Colab, while Traccar provides the remote location tracking interface.
# The software, AI models, and development tools used in the project are listed below:
•	Python
•	OpenCV
•	YOLOv8
•	YOLOv11
•	Haar Cascade Classifier
•	Google Colab
•	Label Studio
•	Traccar Platform
# Research Contributions
•	Development of an integrated assistive technology platform for visually impaired individuals.
•	Application of computer vision and deep learning for autonomous navigation.
•	AI-based Bangladeshi currency recognition system.
•	GPS and GSM-enabled real-time monitoring.
•	Multi-functional prototype combining mobility, finance, and safety support.
# Future Work
•	Real-world autonomous mobility implementation
•	PID-based closed-loop speed control
•	Integration with digital maps and navigation services
•	Improved obstacle avoidance
•	Mobile application development
•	Cloud-based monitoring and analytics
_______________________________________
# Contact
For collaborations, research discussions, or project inquiries:
Md. Mahfuzul Haque
Email: mahfuzul@jstu.ac.bd
Rabeya Khan
Email: rabeyakhan592@gmail.com 
Nadira Farjana
Email: nadirafarjanaiva@gmail.com
# If you find this project useful, please consider giving the repository a star.

