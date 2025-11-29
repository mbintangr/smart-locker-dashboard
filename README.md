# GuaLock - Smart Locker Dashboard

GuaLock is an innovative smart locker system that provides secure, convenient, and modern storage solutions using QR code authentication technology. Built with Streamlit and designed for IoT integration, GuaLock offers a seamless user experience for managing personal storage lockers.

## 🚀 Features

### Core Functionality
- **QR Code Authentication**: Secure access using unique QR codes
- **Real-time Scanning**: Live webcam QR code scanning with instant validation
- **User Management**: Complete authentication system with login, registration, and role-based access
- **Locker Management**: Dynamic locker assignment and availability tracking
- **IoT Integration**: Hardware integration with Raspberry Pi for physical locker control
- **Distance Sensing**: Ultrasonic sensors for detecting locker occupancy
- **Servo Control**: Automated locker opening/closing mechanisms

### User Experience
- **Intuitive Interface**: Clean, modern web interface built with Streamlit
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Updates**: Live status updates and notifications
- **Multi-language Support**: Indonesian language interface with English documentation

## 🏗️ Architecture

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Dashboard │    │   Backend API   │    │   Hardware IoT  │
│   (Streamlit)   │◄──►│   (n8n Webhook) │◄──►│   (Raspberry Pi)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Computer Vision**: OpenCV, pyzbar (QR code detection)
- **Hardware Integration**: 
  - Raspberry Pi GPIO
  - Ultrasonic Sensors (HC-SR04)
  - Servo Motors (SG90)
- **Communication**: HTTP/HTTPS REST API
- **Containerization**: Docker & Docker Compose

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- Docker and Docker Compose (for containerized deployment)
- Raspberry Pi with GPIO access (for hardware integration)
- Webcam (for QR code scanning)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-locker-dashboard
   ```

2. **Install Python dependencies**
   ```bash
   cd dashboard
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit.py
   ```

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Open your browser and navigate to `http://localhost:9003`

### Hardware Setup (Raspberry Pi)

1. **Connect hardware components**
   - Ultrasonic sensors: Trigger and Echo pins
   - Servo motors: Control pins for each locker
   - Webcam: USB or CSI interface

2. **Enable GPIO access**
   ```bash
   sudo pigpiod
   ```

3. **Test hardware functionality**
   - Verify sensor readings
   - Test servo motor movements
   - Check webcam capture

## 🔧 Configuration

### Environment Variables
The application uses external API endpoints that can be configured in the respective Python files:

- **API_BASE_URL**: Base URL for backend services
- **WEBCOOK_LOGIN_URL**: Authentication endpoint
- **WEBCOOK_CHECKOUT_URL**: QR code validation endpoint
- **WEBCOOK_CHECKIN_URL**: Locker registration endpoint

### Hardware Configuration
Edit the GPIO pin mappings in [`dashboard/pages/main.py`](dashboard/pages/main.py:27-73):

```python
# Ultrasonic sensor pins
if locker_id == '1':
    TRIG = 16
    ECHO = 12
elif locker_id == '2':
    TRIG = 19
    ECHO = 6

# Servo motor pins
if locker_id == '1':
    servo_pin = 18
elif locker_id == '2':
    servo_pin = 23
```

## 📖 User Guide

### For Users

1. **Registration**
   - Navigate to the registration page
   - Fill in your email, username, and password
   - Submit the form to create your account

2. **Login**
   - Use your credentials to access the system
   - You will be redirected based on your user role (user/admin)

3. **Using Lockers**
   - **As a User**: Generate QR codes for accessing assigned lockers
   - **As an Admin**: Register lockers to users and manage the system

4. **QR Code Scanning**
   - Allow webcam access when prompted
   - Present your QR code to the camera
   - The system will validate and automatically open your locker

### For Administrators

1. **Locker Management**
   - Monitor locker availability
   - Assign lockers to registered users
   - Track locker usage and status

2. **User Management**
   - View registered users
   - Manage user permissions
   - Handle user accounts

3. **System Monitoring**
   - Check hardware status
   - Monitor API connectivity
   - Review system logs

## 🔒 Security Features

- **QR Code Authentication**: Unique, time-based access codes
- **Session Management**: Secure user sessions with timeout
- **Input Validation**: Form validation and sanitization
- **HTTPS Communication**: Encrypted data transmission
- **Role-Based Access**: Different permissions for users and administrators

## 🐛 Troubleshooting

### Common Issues

1. **Camera Not Detected**
   - Check webcam connections
   - Verify camera permissions in your browser
   - Test camera with other applications

2. **GPIO Access Errors**
   - Ensure pigpio daemon is running: `sudo pigpiod`
   - Check pin configurations in the code
   - Verify hardware connections

3. **API Connection Issues**
   - Check network connectivity
   - Verify API endpoint URLs
   - Test API connectivity separately

4. **Servo Motor Problems**
   - Check power supply to servos
   - Verify pin connections
   - Test servo movement with simple scripts

### Debug Mode
Enable debug logging by setting environment variables:
```bash
export DEBUG=True
streamlit run streamlit.py
```

## 🤝 Contributing

We welcome contributions to improve GuaLock! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Python PEP 8 coding standards
- Add comments for complex logic
- Include tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web framework
- **OpenCV**: For computer vision capabilities
- **Raspberry Pi Community**: For hardware support and resources
- **n8n**: For the workflow automation platform

## 📞 Support

For support and inquiries:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the code comments for implementation details

---

**Built with ❤️ for smart storage solutions**
