
ampy -p %1 put main.py
ampy -p %1 put umqttsimple.py
ampy -p %1 put mqtt_dht.py
ampy -p %1 put mqtt_sens.py
ampy -p %1 put mqtt_status.py
ampy -p %1 put mqtt_switch.py
ampy -p %1 put WDT.py
ampy -p %1 put bme280.py
ampy -p %1 put mqtt_bme280.py
ampy -p %1 put gc9a01.py
ampy -p %1 put gc9a01c.py
ampy -p %1 put test_display.py

if %1 neq "" sed -e 's/IDENT/%2/g' wifi.txt > wifi.dat

ampy -p %1 put wifi.dat
