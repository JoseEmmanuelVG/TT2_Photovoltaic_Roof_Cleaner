# TT2_Photovoltaic_Roof_Cleaner

# Implementation Project of Communication and Control with Raspberry Pi 5

## Main Objective
To develop and implement a communication and control system on a Raspberry Pi 5, utilizing the WiFi module, for the remote operation of a mobile robot designed for cleaning photovoltaic solar rooftops.

## Functionalities

### Implementation of Modules 
**Raspberry Pi 5 and Essential Accessories**: Necessary elements such as a case, power adapter, micro HDMI-HDMI cable, and an SD card with Raspberry Pi OS were acquired and configured.

**Verification*: 
- **Desktop Interface**: Functionality tests of the basic interface of the Raspberry Pi 5.
- **Communication Module**: Validation of the WiFi module and configuration of the VNC protocol for remote control.
- **Control and Processing Module**: Evaluation of GPIO outputs through a Python program.

### Implementation of Module Web aplication
**Web User Interface**: A web application was developed using the Dash framework to control and monitor the robotic system.

#### Project Structure
- **Assets Folder**: CSS style sheets and local storage.
- **Callback and Function Files**: Handling interaction logic.
- **User Interface Definition Files**: Visual structure of the web pages.

**Framework and Libraries**: Integration of Dash, Flask, React.js, and dash_bootstrap_components.

**Server and Security Configuration**: Configuration of authentication and encryption with flask_login and bcrypt.

### Functionality Verification
**Navigation Tests**: Confirmation of correct URL generation and redirection between views (autonomous control, remote control, login).

**Usability, Responsive Design, and Accessibility Tests**:
- **Usability**: Intuitive interactions and clearly labeled buttons.
- **Responsive Design**: Interface adaptation to different screen sizes.
- **Accessibility**: Compliance with web accessibility guidelines.

**User Interface (UI) Functionality Tests**:
- **Network Inspection**: Monitoring network requests and responses.
- **Identified Errors**: Failed requests with status code 500 without raspberry pi Conection.

### Implementation of Callbacks and Visual Controllers
**Robot Movement Control**: Integration of interactive buttons in the UI to move the robot in various directions.

**Design and Usability Improvements**: Optimization of control layout and visual/auditory feedback.

**Image Capture Controllers**: Implementation of buttons to capture and save images from the robot’s camera.

**Serial Reception and Transmission with Arduino**:
- **Roller Activation**: Control of power, rotation inversion, and speed adjustment.
- **Sensor Data Reception**: Real-time visualization of ultrasonic, temperature, humidity sensors, and battery percentage.

**Controllers and Callbacks for Additional Sensors and Actuators**:
- **Float Sensors**: Status monitoring in the UI.
- **Water Pump Relay**: Power control.
- **H-Bridge for Electronic Actuators**: Control of elongation and retraction.

**Addition of Lateral Ultrasonic Sensors**: Improved autonomous navigation of the robot.

## Results
Functional and usability tests confirmed the correct operation of the communication and control modules, as well as the web user interface, providing precise and reliable control of the mobile robot.





<details>
  <summary>🌟 Did you find any repository useful?</summary>
  If any project has been helpful to you, consider giving it a ⭐ star in the repository and follow my GitHub account to stay tuned for future updates! 🚀

  In addition, I am always open to suggestions, recommendations or collaborations. Feel free to [get in touch](https://www.linkedin.com/in/vazquez-galan-jose-emmanuel-664968221) if you have any questions or ideas for improving this project. I'm excited for your feedback and contributions.

  Thank you for your interest and support! 😊
</details>




<p align="center">
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
</p>
