# micropython_sensnode
Sensor nodes using micropython with GC9A01C display support

## Overview
This project provides a complete MicroPython-based sensor node system that can read environmental data from various sensors and publish it via MQTT. The system now includes support for the GC9A01C round LCD display to show real-time sensor readings.

## Features
- **Multi-sensor support**: DHT22, BME280, and switch sensors
- **MQTT integration**: Automatic publishing of sensor data
- **Visual display**: Real-time sensor data on GC9A01C round LCD
- **WiFi connectivity**: Automatic connection and reconnection
- **Watchdog protection**: System reliability with automatic recovery
- **Configurable**: Easy setup via configuration file

## Hardware Requirements
- ESP32 or ESP8266 microcontroller
- Sensors: DHT22, BME280, or other supported sensors
- GC9A01C round LCD display (240x240 pixels)
- WiFi network access
- MQTT broker

## GC9A01C Display Integration

### New Files Added
- **`gc9a01c.py`**: Complete display driver with SPI communication and graphics support
- **`test_display.py`**: Standalone test script for display functionality
- **`wifi.dat.example`**: Example configuration file

### Modified Files
- **`main.py`**: Integrated display initialization and sensor data visualization

### Display Features
- **Resolution**: 240x240 pixels round display
- **Color support**: 16-bit RGB565 color format
- **Real-time updates**: Temperature and humidity displayed with color coding
- **Error handling**: Graceful fallback when display updates fail
- **SPI interface**: High-speed communication (40MHz baudrate)

### Pin Configuration
Default pin assignments (configurable in code):
```
SPI CS:    GPIO 15
SPI DC:    GPIO 5
SPI RST:   GPIO 0
SPI BL:    GPIO 2 (backlight)
DHT Sensor: GPIO 4
```

### Display Output
The display shows:
- Temperature readings in red text
- Humidity readings in green text
- Clear, easy-to-read format
- Automatic updates with sensor readings

## Configuration
Create a `wifi.dat` file with the following format:
```
your_wifi_ssid
your_wifi_password
your_mqtt_server_ip
your_node_name
30
dht22 4
```

## Usage

### Full System
1. Configure your `wifi.dat` file
2. Upload all files to your ESP32/ESP8266
3. Connect sensors and display according to pin configuration
4. Run `main.py` for complete sensor node with MQTT and display

### Display Testing
1. Run `test_display.py` to test display functionality independently
2. Verify sensor readings and display output
3. Adjust pin configurations as needed

## Sensor Support
- **DHT22**: Temperature and humidity sensor
- **BME280**: Temperature, humidity, and pressure sensor
- **Switch sensors**: Digital input monitoring

## Dependencies
- MicroPython firmware
- Built-in libraries: `machine`, `network`, `time`, `framebuf`
- Custom modules: `umqttsimple`, `bme280`, sensor-specific modules



Perfect! I've updated the upload.bat script to include the new GC9A01C display files. The script now includes:

Added Files:
•  gc9a01c.py: The main display driver
•  test_display.py: Standalone test script for display functionality

Current Upload Script Functionality:
The upload.bat script now uploads all necessary files to the ESP32/ESP8266:

1. Core system files: main.py, umqttsimple.py, WDT.py
2. Sensor modules: mqtt_dht.py, mqtt_sens.py, mqtt_status.py, mqtt_switch.py, bme280.py, mqtt_bme280.py
3. Display files: gc9a01c.py, test_display.py
4. Configuration: wifi.dat (generated from wifi.txt with identifier substitution)

Usage:
The script can be run with:
batch
Where:
•  COM3 is your ESP32/ESP8266 serial port
•  your_node_identifier will replace the IDENT placeholder in wifi.txt to create wifi.dat

The script now ensures that all files needed for the complete sensor node system with GC9A01C display support are uploaded to the microcontroller in a single operation.
