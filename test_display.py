#!/usr/bin/env python3
"""
Test script for GC9A01C display with DHT sensor
This can be used to test the display functionality without the full MQTT setup
"""

import machine
import dht
import time
from machine import SPI, Pin
from gc9a01c import GC9A01C

# Pin configuration - adjust these to match your wiring
DHT_PIN = 4       # GPIO pin connected to DHT sensor
SPI_SCK = 18      # SPI Clock
SPI_MOSI = 23     # SPI MOSI (Master Out Slave In)
SPI_CS = 15       # Chip Select
SPI_DC = 5        # Data/Command
SPI_RST = 0       # Reset
SPI_BL = 2        # Backlight (optional)

def test_display():
    print("Initializing SPI and display...")
    
    # Initialize SPI
    spi = SPI(1, baudrate=40000000, polarity=1, phase=1, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    
    # Initialize display
    display = GC9A01C(spi, cs=SPI_CS, dc=SPI_DC, rst=SPI_RST, bl=SPI_BL)
    display.set_backlight(1)
    
    print("Display initialized successfully")
    
    # Initialize DHT sensor
    sensor = dht.DHT22(Pin(DHT_PIN))  # Use DHT22 or DHT11 as appropriate
    
    print("Starting sensor readings...")
    
    try:
        while True:
            try:
                # Read sensor
                sensor.measure()
                temp = sensor.temperature()
                hum = sensor.humidity()
                
                print(f"Temperature: {temp}°C, Humidity: {hum}%")
                
                # Update display
                display.display_sensor_data(temp, hum)
                
                time.sleep(2)  # Update every 2 seconds
                
            except OSError as e:
                print(f"Sensor read error: {e}")
                # Display error message
                display.clear()
                display.text("Sensor Error", 50, 100, 0xF800)  # Red text
                display.show()
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("Test stopped by user")
        display.clear()
        display.text("Test Stopped", 50, 100, 0xFFFF)
        display.show()

if __name__ == "__main__":
    test_display()
