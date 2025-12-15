import machine
import framebuf
import time

class GC9A01C:
    def __init__(self, spi, cs, dc, rst, bl=None):
        self.spi = spi
        self.cs = machine.Pin(cs, machine.Pin.OUT)
        self.dc = machine.Pin(dc, machine.Pin.OUT)
        self.rst = machine.Pin(rst, machine.Pin.OUT)
        self.bl = machine.Pin(bl, machine.Pin.OUT) if bl else None

        self.width = 240
        self.height = 240
        
        # Initialize display buffer
        self.buffer = bytearray(self.width * self.height * 2)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)
        
        self.init_display()

    def init_display(self):
        self.reset()
        
        # GC9A01C initialization sequence
        init_commands = [
            (0xEF, None),
            (0xEB, [0x14]),
            (0xFE, None),
            (0xEF, None),
            (0xEB, [0x14]),
            (0x84, [0x40]),
            (0x85, [0xFF]),
            (0x86, [0xFF]),
            (0x87, [0xFF]),
            (0x88, [0x0A]),
            (0x89, [0x21]),
            (0x8A, [0x00]),
            (0x8B, [0x80]),
            (0x8C, [0x01]),
            (0x8D, [0x01]),
            (0x8E, [0xFF]),
            (0x8F, [0xFF]),
            (0xB6, [0x00, 0x00]),
            (0x36, [0x18]),
            (0x3A, [0x05]),
            (0x90, [0x08, 0x08, 0x08, 0x08]),
            (0xBD, [0x06]),
            (0xBC, [0x00]),
            (0xFF, [0x60, 0x01, 0x04]),
            (0xC3, [0x13]),
            (0xC4, [0x13]),
            (0xC9, [0x22]),
            (0xBE, [0x11]),
            (0xE1, [0x10, 0x0E]),
            (0xDF, [0x21, 0x0C, 0x02]),
            (0xF0, [0x45, 0x09, 0x08, 0x08, 0x26, 0x2A]),
            (0xF1, [0x43, 0x70, 0x72, 0x36, 0x37, 0x6F]),
            (0xF2, [0x45, 0x09, 0x08, 0x08, 0x26, 0x2A]),
            (0xF3, [0x43, 0x70, 0x72, 0x36, 0x37, 0x6F]),
            (0xED, [0x1B, 0x0B]),
            (0xAE, [0x77]),
            (0xCD, [0x63]),
            (0x70, [0x07, 0x07, 0x04, 0x0E, 0x0F, 0x09, 0x07, 0x08, 0x03]),
            (0xE8, [0x34]),
            (0x62, [0x18, 0x0D, 0x71, 0xED, 0x70, 0x70, 0x18, 0x0F, 0x71, 0xEF, 0x70, 0x70]),
            (0x63, [0x18, 0x11, 0x71, 0xF1, 0x70, 0x70, 0x18, 0x13, 0x71, 0xF3, 0x70, 0x70]),
            (0x64, [0x28, 0x29, 0xF1, 0x01, 0xF1, 0x00, 0x07]),
            (0x66, [0x3C, 0x00, 0xCD, 0x67, 0x45, 0x45, 0x10, 0x00, 0x00, 0x00]),
            (0x67, [0x00, 0x3C, 0x00, 0x00, 0x00, 0x01, 0x54, 0x10, 0x32, 0x98]),
            (0x74, [0x10, 0x85, 0x80, 0x00, 0x00, 0x4E, 0x00]),
            (0x98, [0x3E, 0x07]),
            (0x35, None),
            (0x21, None),
            (0x11, None),
            (0x29, None),
        ]
        
        for cmd, data in init_commands:
            self.write_cmd(cmd)
            if data:
                for byte in data:
                    self.write_data(byte)
            if cmd in [0x11, 0x29]:  # Sleep out and display on
                time.sleep_ms(120)

    def write_cmd(self, cmd):
        self.cs.off()
        self.dc.off()
        self.spi.write(bytearray([cmd]))
        self.cs.on()

    def write_data(self, data):
        self.cs.off()
        self.dc.on()
        if isinstance(data, int):
            self.spi.write(bytearray([data]))
        else:
            self.spi.write(data)
        self.cs.on()

    def reset(self):
        self.rst.on()
        time.sleep_ms(100)
        self.rst.off()
        time.sleep_ms(100)
        self.rst.on()
        time.sleep_ms(100)

    def set_backlight(self, value):
        if self.bl:
            self.bl.value(value)
    
    def clear(self, color=0x0000):
        self.framebuf.fill(color)
    
    def pixel(self, x, y, color):
        self.framebuf.pixel(x, y, color)
    
    def text(self, text, x, y, color=0xFFFF):
        self.framebuf.text(text, x, y, color)
    
    def show(self):
        # Set address window to full screen
        self.write_cmd(0x2A)  # Column address set
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)  # 239
        
        self.write_cmd(0x2B)  # Row address set  
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)  # 239
        
        self.write_cmd(0x2C)  # Memory write
        self.write_data(self.buffer)
    
    def display_sensor_data(self, temp, hum):
        self.clear()
        self.text("Temperature:", 10, 50, 0xFFFF)
        self.text("{:.1f}C".format(temp), 10, 70, 0xF800)  # Red
        self.text("Humidity:", 10, 110, 0xFFFF)
        self.text("{:.1f}%".format(hum), 10, 130, 0x07E0)  # Green
        self.show()

