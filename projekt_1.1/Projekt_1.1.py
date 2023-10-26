import time
import machine
import onewire
import ds18x20
import ujson

with open("config.json", "r") as f:
    config = ujson.load(f)

dat_pin_number = config.get("pin", 16)
sleep_time = config.get("interval", 9)

dat = machine.Pin(dat_pin_number)
ds = ds18x20.DS18X20(onewire.OneWire(dat))

roms = ds.scan()
print("found devices:", roms)

id = ""
for b in machine.unique_id():
    id += "{:02x}".format(b)

while True:
    ds.convert_temp()
    time.sleep_ms(750) 

    for rom in roms:
        sensor_id = hex(int.from_bytes(rom, "little"))[2:]
        temperature = ds.read_temp(rom)

        print("Sensor ID:", sensor_id)
        print("Device ID:", id)
        print("Temperature:", temperature)

    time.sleep(sleep_time)

