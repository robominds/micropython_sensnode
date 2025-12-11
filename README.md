# micropython_sensnode

Sensor node firmware, examples, and tooling for MicroPython-based sensor nodes (ESP32 / ESP8266).

Overview

This repository contains MicroPython code and documentation for small sensor nodes that collect environmental data and publish it (e.g. via MQTT). It includes example firmware, configuration patterns, and tooling to flash and interact with devices.

Features

- Minimal MicroPython firmware examples for ESP32 and ESP8266
- Example sensor drivers and data publishing to MQTT
- Simple configuration via secrets.py or config.py
- Flashing and REPL usage notes

Supported hardware

- ESP32 (recommended)
- ESP8266 (limited support)

Repository layout

- main.py / boot.py - example application entry points
- drivers/ - sensor driver examples (I2C, SPI, 1-Wire)
- tools/ - helper scripts for flashing and serial interactions
- docs/ - additional documentation and schematics

Quick start

1. Prerequisites
   - Python 3.8+
   - esptool.py / mpremote or ampy for flashing
   - MicroPython firmware for your board (download from micropython.org)

2. Flash MicroPython

   Using esptool.py:
   - erase flash: esptool.py --port <PORT> erase_flash
   - write firmware: esptool.py --chip esp32 --port <PORT> write_flash -z 0x1000 <firmware>.bin

   Or use mpremote to sync files after installing MicroPython.

3. Configure

   - Create a file named secrets.py or config.py on the device with your Wi-Fi and MQTT settings. Example secrets.py:

   ```python
   WIFI_SSID = "your-ssid"
   WIFI_PASSWORD = "your-password"
   MQTT_BROKER = "mqtt.example.com"
   MQTT_PORT = 1883
   MQTT_TOPIC = "sensors/node1"
   ```

4. Deploy example

   - Copy files to the device using mpremote or rshell, then reboot.
   - main.py will connect and publish sensor readings to the configured MQTT_TOPIC.

Development

- Add drivers under drivers/ following the provided examples.
- Keep hardware-specific code isolated so it can be reused across nodes.

Contributing

Contributions are welcome. Please open issues for bugs or feature requests and submit pull requests for changes.

License

MIT License

Maintainers

- robominds
