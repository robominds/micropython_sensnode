import machine
import framebuf
import time

class GC9A01:
    """
    Lightweight driver for the GC9A01 round 240x240 LCD.
    Designed for MicroPython on ESP32/ESP8266 using SPI.
    """

    def __init__(self, spi, cs, dc, rst, bl=None, width=240, height=240):
        self.spi = spi
        self.cs = machine.Pin(cs, machine.Pin.OUT)
        self.dc = machine.Pin(dc, machine.Pin.OUT)
        self.rst = machine.Pin(rst, machine.Pin.OUT)
        self.bl = machine.Pin(bl, machine.Pin.OUT) if bl is not None else None
        self.width = width
        self.height = height

        # Framebuffer in RGB565
        self.buffer = bytearray(self.width * self.height * 2)
        self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)

        self.reset()
        self.init_display()
        self.fill(0)
        self.show()
        if self.bl:
            self.set_backlight(1)

    # --- Low level helpers ---
    def _write_cmd(self, cmd):
        self.cs.off()
        self.dc.off()
        self.spi.write(bytearray([cmd]))
        self.cs.on()

    def _write_data(self, data):
        self.cs.off()
        self.dc.on()
        self.spi.write(data if isinstance(data, (bytes, bytearray)) else bytearray([data]))
        self.cs.on()

    def reset(self):
        self.rst.off()
        time.sleep_ms(50)
        self.rst.on()
        time.sleep_ms(50)

    # --- Display setup ---
    def init_display(self):
        # Init sequence adapted from GC9A01 datasheet and common display modules
        cmds = [
            (0xEF, None),
            (0xEB, b"\x14"),
            (0xFE, None),
            (0xEF, None),
            (0xEB, b"\x14"),
            (0x84, b"\x40"),
            (0x85, b"\xFF"),
            (0x86, b"\xFF"),
            (0x87, b"\xFF"),
            (0x88, b"\x0A"),
            (0x89, b"\x21"),
            (0x8A, b"\x00"),
            (0x8B, b"\x80"),
            (0x8C, b"\x01"),
            (0x8D, b"\x01"),
            (0x8E, b"\xFF"),
            (0x8F, b"\xFF"),
            (0xB6, b"\x00\x00"),
            (0x36, b"\x18"),  # Memory access control: RGB, refresh direction
            (0x3A, b"\x05"),  # 16-bit color
            (0x90, b"\x08\x08\x08\x08"),
            (0xBD, b"\x06"),
            (0xBC, b"\x00"),
            (0xFF, b"\x60\x01\x04"),
            (0xC3, b"\x13"),
            (0xC4, b"\x13"),
            (0xC9, b"\x22"),
            (0xBE, b"\x11"),
            (0xE1, b"\x10\x0E"),
            (0xDF, b"\x21\x0C\x02"),
            (0xF0, b"\x45\x09\x08\x08\x26\x2A"),
            (0xF1, b"\x43\x70\x72\x36\x37\x6F"),
            (0xF2, b"\x45\x09\x08\x08\x26\x2A"),
            (0xF3, b"\x43\x70\x72\x36\x37\x6F"),
            (0xED, b"\x1B\x0B"),
            (0xAE, b"\x77"),
            (0xCD, b"\x63"),
            (0x70, b"\x07\x07\x04\x0E\x0F\x09\x07\x08\x03"),
            (0xE8, b"\x34"),
            (0x62, b"\x18\x0D\x71\xED\x70\x70\x18\x0F\x71\xEF\x70\x70"),
            (0x63, b"\x18\x11\x71\xF1\x70\x70\x18\x13\x71\xF3\x70\x70"),
            (0x64, b"\x28\x29\xF1\x01\xF1\x00\x07"),
            (0x66, b"\x3C\x00\xCD\x67\x45\x45\x10\x00\x00\x00"),
            (0x67, b"\x00\x3C\x00\x00\x00\x01\x54\x10\x32\x98"),
            (0x74, b"\x10\x85\x80\x00\x00\x4E\x00"),
            (0x98, b"\x3E\x07"),
            (0x35, None),    # Tearing effect line on
            (0x21, None),    # Inversion on
            (0x11, None),    # Sleep out
            (0x29, None),    # Display on
        ]
        for cmd, data in cmds:
            self._write_cmd(cmd)
            if data:
                self._write_data(data)
            if cmd in (0x11, 0x29):
                time.sleep_ms(120)

    # --- Drawing primitives ---
    def fill(self, color):
        self.fb.fill(color)

    def pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.fb.pixel(x, y, color)

    def text(self, string, x, y, color=0xFFFF):
        self.fb.text(string, x, y, color)

    def set_backlight(self, value):
        if self.bl:
            self.bl.value(1 if value else 0)

    # --- Transfer framebuffer to display ---
    def show(self):
        self._set_window(0, 0, self.width - 1, self.height - 1)
        self._write_cmd(0x2C)
        self.cs.off()
        self.dc.on()
        self.spi.write(self.buffer)
        self.cs.on()

    def _set_window(self, x0, y0, x1, y1):
        self._write_cmd(0x2A)
        self._write_data(bytearray([0x00, x0, 0x00, x1]))
        self._write_cmd(0x2B)
        self._write_data(bytearray([0x00, y0, 0x00, y1]))

    # --- Convenience helpers ---
    def clear(self, color=0):
        self.fill(color)
        self.show()

    def draw_sensor_readout(self, temp_c=None, hum=None, y_start=20):
        self.fill(0)
        if temp_c is not None:
            self.text("Temp: {:.1f}C".format(temp_c), 30, y_start, 0xF800)
        if hum is not None:
            self.text("Hum:  {:.1f}%".format(hum), 30, y_start + 20, 0x07E0)
        self.show()
