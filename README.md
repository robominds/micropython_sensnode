# micropython_sensnode

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MicroPython](https://img.shields.io/badge/MicroPython-1.19+-blue.svg)](https://micropython.org/)
[![Platform](https://img.shields.io/badge/Platform-ESP32%20%7C%20ESP8266-green.svg)](https://www.espressif.com/)

Sensor node firmware, examples, and tooling for MicroPython-based sensor nodes (ESP32 / ESP8266).

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Supported Hardware](#supported-hardware)
- [Repository Layout](#repository-layout)
- [Quick Start](#quick-start)
- [Example Usage](#example-usage)
- [Tested Sensors](#tested-sensors)
- [Troubleshooting](#troubleshooting)
- [Power Management](#power-management)
- [Security](#security)
- [Development](#development)
- [Contributing](#contributing)
- [Useful Links](#useful-links)
- [License](#license)
- [Maintainers](#maintainers)

## Overview

This repository contains MicroPython code and documentation for small sensor nodes that collect environmental data and publish it (e.g. via MQTT). It includes example firmware, configuration patterns, and tooling to flash and interact with devices.

## Features

- Minimal MicroPython firmware examples for ESP32 and ESP8266
- Example sensor drivers and data publishing to MQTT
- Simple configuration via secrets.py or config.py
- Flashing and REPL usage notes

## Supported Hardware

- ESP32 (recommended)
- ESP8266 (limited support)

## Repository Layout

- **main.py** - Main application entry point with MQTT client and sensor reading loop
- **bme280.py** - BME280 temperature/humidity/pressure sensor driver
- **mqtt_bme280.py** - MQTT wrapper for BME280 sensor
- **mqtt_dht.py** - MQTT wrapper for DHT22 temperature/humidity sensor
- **mqtt_sens.py** - Sensor list parser and manager
- **mqtt_status.py** - MQTT status reporting module
- **mqtt_switch.py** - MQTT switch control module
- **mqtt_uptime.py** - MQTT uptime reporting module
- **umqttsimple.py** - Simple MQTT client implementation
- **WDT.py** - Watchdog timer implementation
- **rfswitch.py** - RF switch control module
- **wifi.txt** - WiFi and MQTT configuration file template
- **upload.bat** - Windows batch script for uploading files

## Quick Start

### 1. Prerequisites

Install required tools:
```bash
pip install esptool mpremote
```

Requirements:
- Python 3.8+
- esptool.py and mpremote for flashing and file management
- MicroPython firmware for your board (download from [micropython.org](https://micropython.org/download/))

### 2. Flash MicroPython

Using esptool.py:

**For Linux:**
```bash
# Erase flash
esptool.py --port /dev/ttyUSB0 erase_flash

# Write firmware (ESP32)
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-micropython-v1.19.1.bin
```

**For Windows:**
```bash
# Erase flash
esptool.py --port COM3 erase_flash

# Write firmware (ESP32)
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 esp32-micropython-v1.19.1.bin
```

**Expected output:**
```
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: xx:xx:xx:xx:xx:xx
Uploading stub...
Running stub...
Stub running...
Configuring flash size...
Flash will be erased from 0x00001000 to 0x00xxxxxx...
Compressed xxxxx bytes to xxxxx...
Wrote xxxxx bytes (xxxxx compressed) at 0x00001000 in x.x seconds (effective xxxx.x kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```

Or use mpremote to sync files after installing MicroPython.

### 3. Configure

Create a file named `wifi.dat` on the device with your Wi-Fi and MQTT settings:

```
your-ssid
your-password
mqtt.example.com
node1
60
BME:22:21
```

Format:
- Line 1: WiFi SSID
- Line 2: WiFi password
- Line 3: MQTT broker address
- Line 4: Node name
- Line 5: Message interval (seconds)
- Line 6+: Sensor definitions (e.g., `BME:SCL_PIN:SDA_PIN` or `DHT:PIN`)

### 4. Deploy Example

Copy files to the device using mpremote:
```bash
mpremote connect /dev/ttyUSB0 cp main.py umqttsimple.py mqtt_bme280.py bme280.py mqtt_sens.py WDT.py :
mpremote connect /dev/ttyUSB0 cp wifi.dat :
mpremote connect /dev/ttyUSB0 reset
```

main.py will connect to WiFi and publish sensor readings to the configured MQTT broker.

## Example Usage

Example of reading BME280 sensor and publishing to MQTT:

```python
import bme280
from machine import Pin, I2C
from umqttsimple import MQTTClient

# Initialize I2C for BME280
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
bme = bme280.BME280(i2c=i2c)

# Read sensor data
temperature = bme.temperature
humidity = bme.humidity
pressure = bme.pressure

# Connect to MQTT and publish
client = MQTTClient("sensor-node-1", "mqtt.example.com")
client.connect()
client.publish("sensors/node1/temperature", str(temperature))
client.publish("sensors/node1/humidity", str(humidity))
client.publish("sensors/node1/pressure", str(pressure))
client.disconnect()
```

## Tested Sensors

The following sensors have been tested and verified to work with this firmware:

- **BME280** - Temperature, humidity, and pressure sensor (I2C)
  - Driver: `bme280.py`, MQTT wrapper: `mqtt_bme280.py`
  - Interface: I2C
  - Typical pins: SCL=22, SDA=21 (ESP32)

- **DHT22 (AM2302)** - Temperature and humidity sensor (1-Wire)
  - MQTT wrapper: `mqtt_dht.py`
  - Interface: Digital 1-Wire
  - Any GPIO pin can be used

## Troubleshooting

### Connection Issues

**Problem:** Device not connecting to WiFi
- **Solution:** Check your SSID and password in `wifi.dat`. Ensure your WiFi network is 2.4GHz (ESP8266/ESP32 don't support 5GHz).
- **Solution:** Try moving the device closer to the router to rule out signal strength issues.

**Problem:** Cannot find serial port
- **Solution (Linux):** Ensure you have permissions to access the serial port. Add your user to the `dialout` group: `sudo usermod -a -G dialout $USER` (logout and login required).
- **Solution (Windows):** Check Device Manager to find the correct COM port. Install USB-to-Serial drivers if needed (CP2102/CH340).

### Flash Failures

**Problem:** Flash verification failed
- **Solution:** Try reducing the baud rate: `esptool.py --baud 115200 ...` (default is 460800).
- **Solution:** Use a higher quality USB cable with data lines (not just power).
- **Solution:** Power the board from external 5V source during flashing if USB power is insufficient.

**Problem:** Device keeps rebooting
- **Solution:** Check the watchdog timer configuration in your code. Comment out WDT initialization during debugging.
- **Solution:** Add debug print statements to identify where the crash occurs.

### MQTT Issues

**Problem:** Cannot connect to MQTT broker
- **Solution:** Verify the broker address and port in `wifi.dat`. Test connectivity using `ping` from another device.
- **Solution:** Check if the broker requires authentication. Update the code to include username/password in MQTTClient initialization.
- **Solution:** Ensure your firewall allows outbound connections on port 1883 (or 8883 for TLS).

## Power Management

For battery-operated sensor nodes, consider using deep sleep to extend battery life:

```python
import machine
import time

# Read sensor and publish to MQTT
# ... your code here ...

# Enter deep sleep for 10 minutes (600 seconds)
print('Entering deep sleep for 600 seconds...')
machine.deepsleep(600000)  # Time in milliseconds
```

**Notes:**
- During deep sleep, the device consumes only 10-150 µA (depending on the ESP32/ESP8266 model).
- Connect GPIO16 (D0) to RST pin to wake from deep sleep automatically.
- All code execution stops during deep sleep. The device will restart from `main.py` after waking.
- RAM contents are lost during deep sleep. Use RTC memory for persistent data between sleep cycles.

## Security

### MQTT Security Recommendations

**Use TLS/SSL for MQTT connections:**
```python
# Example of secure MQTT connection
client = MQTTClient("sensor-node-1", "mqtt.example.com", port=8883, ssl=True)
```

**Additional security practices:**
- Use strong, unique passwords for WiFi and MQTT broker authentication
- Change default credentials in example configurations before deployment
- Consider using certificate-based authentication for production deployments
- Regularly update MicroPython firmware to get security patches
- Isolate IoT devices on a separate VLAN if possible
- Use MQTT username/password authentication at minimum
- Never commit `wifi.dat` or `secrets.py` with real credentials to version control

## Development

- Add drivers under the main directory following the provided examples (e.g., `mqtt_bme280.py`, `mqtt_dht.py`).
- Keep hardware-specific code isolated so it can be reused across nodes.
- Use the `mqtt_sens.py` module to register and manage multiple sensors in a unified way.

## Contributing

Contributions are welcome! Please follow these guidelines:

### Code Style
- Follow [PEP 8](https://pep8.org/) style guidelines for Python code where applicable
- Use 4 spaces for indentation (not tabs)
- Keep functions focused and single-purpose
- Add docstrings for non-trivial functions
- Use meaningful variable names

### Testing
- Test your changes on actual ESP32/ESP8266 hardware before submitting
- Verify that existing functionality is not broken
- Include example usage in your PR description

### Pull Request Process
1. Fork the repository and create a feature branch from `main`
2. Use descriptive branch names (e.g., `feature/add-bmp180-driver` or `fix/wifi-reconnect-issue`)
3. Make focused commits with clear commit messages
4. Open a pull request with a clear description of changes
5. Reference any related issues in your PR description

### Reporting Issues
- Use the issue tracker for bugs and feature requests
- Provide detailed information: hardware model, MicroPython version, error messages
- Include code snippets or configuration files that reproduce the issue

## Useful Links

### MicroPython Resources
- [Official MicroPython Documentation](https://docs.micropython.org/)
- [MicroPython Downloads](https://micropython.org/download/)
- [MicroPython Forum](https://forum.micropython.org/)

### MQTT Brokers
- [Mosquitto](https://mosquitto.org/) - Popular open-source MQTT broker
- [HiveMQ](https://www.hivemq.com/) - Enterprise MQTT broker with free tier
- [EMQX](https://www.emqx.io/) - Scalable MQTT broker for IoT

### Hardware Documentation
- [ESP32 Technical Reference](https://www.espressif.com/en/support/documents/technical-documents)
- [ESP8266 Technical Reference](https://www.espressif.com/en/support/documents/technical-documents)

## License

MIT License

## Maintainers

- robominds
