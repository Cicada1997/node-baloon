import board
import busio
import digitalio
import time
import adafruit_rfm69

# -------------------------
# ESP32-C6-Zero pin mapping
# -------------------------
SCK  = board.IO3
MOSI = board.IO1
MISO = board.IO2

CS    = digitalio.DigitalInOut(board.IO0)
RESET = digitalio.DigitalInOut(board.IO4)
DIO0  = digitalio.DigitalInOut(board.IO5)

# -------------------------
# Manual reset (required)
# -------------------------
RESET.direction = digitalio.Direction.OUTPUT
RESET.value = False
time.sleep(0.1)
RESET.value = True
time.sleep(0.1)

# -------------------------
# SPI setup
# -------------------------
spi = busio.SPI(SCK, MOSI=MOSI, MISO=MISO)

# wait for SPI ready
while not spi.try_lock():
    pass
spi.configure(baudrate=1000000, phase=0, polarity=0)
spi.unlock()

# -------------------------
# Initialize RFM69
# -------------------------
FREQ_MHZ = 868.0      

rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, FREQ_MHZ)
rfm69.encryption_key = b"1234567890ABCDEF"  # MUST match on both nodes
rfm69.tx_power = 20  # High-power HCW module

NODE_ID = 1
DEST_ID = 2

rfm69.node = NODE_ID
rfm69.destination = DEST_ID



print("Node 1 ready.")

counter = 0
last_send = time.monotonic()

while True:
    # ---- RECEIVE ----
    packet = rfm69.receive(with_header=True)
    if packet is not None:
        header = [hex(x) for x in packet[0:4]]
        payload = packet[4:].decode()
        print(f"[Node 1] Received: {payload}, Header: {header}, RSSI: {rfm69.last_rssi}")

    # ---- SEND EVERY 2 SEC ----
    now = time.monotonic()
    if now - last_send > 2:
        counter += 1
        msg = f"Hello from Node 1 / msg {counter}"
        rfm69.send(msg.encode("utf-8"), keep_listening=True)
        print("[Node 1] Sent:", msg)
        last_send = now
