import spidev
import time

# spi.open(0,0)	                ffnet den SPI-Bus 0 mit CS0
# spi.open(0,1)	                ffnet den SPI-Bus 0 mit CS1
# spi.close()	                Schliesst den SPI-Bus
# spi.readbytes(len)	        Liest len Bytes vom SPI-Slave
# spi.writebytes([array of bytes])	Sendet ein Byte-Array zum SPI-Slave
# spi.xfer([array of bytes])	Sendet ein Byte-Array, CEx wird vor jedem Byte aktiv und dann wieder inaktiv
# spi.xfer2([array of bytes])	Sendet ein Byte-Array, dabei bleibt CEx dauerhaft aktiv

# SPI transfer: 1 byte instruction + 3 bytes address + n bytes write or read

READ_INSTRUCTION          = 0x03
HI_SPEED_READ_INSTRUCTION = 0x0B
ERASE_4KB_INSTRUCTION     = 0x20
ERASE_32KB_INSTRUCTION    = 0x52
ERASE_64KB_INSTRUCTION    = 0xD8
ERASE_CHIP_INSTRUCTION    = 0x60
BYTE_PROGRAM_INSTRUCTION  = 0x02
AAI_WORD_PROG_INSTRUCTION = 0xAD
RDSR_INSTRUCTION          = 0x05
EWSR_INSTRUCTION          = 0x50
WRSR_INSTRUCTION          = 0x01
WREN_INSTRUCTION          = 0x06
WRDI_INSTRUCTION          = 0x04
RDID_INSTRUCTION          = 0x90
JEDEC_ID_INSTRUCTION      = 0x9F
EBSY_INSTRUCTION          = 0x70
DBSY_INSTRUCTION          = 0x80



def read_status(spi):
    to_send = [RDSR_INSTRUCTION, 0x00]
    to_receive = spi.xfer2(to_send)
    return to_receive[1]

def chip_erase(spi):
    spi.xfer([WREN_INSTRUCTION])
    to_send = [ERASE_CHIP_INSTRUCTION]
    spi.xfer(to_send)
    print("Chip erase started: " + str(time.localtime()))
    status = read_status(spi)
    while (status & 0x01) == 0x01:
        status = read_status(spi)
    spi.xfer([WRDI_INSTRUCTION])
    print("Chip erase finished: " + str(time.localtime()))

def enable_write(spi):
    to_send = [EWSR_INSTRUCTION]
    to_receive = spi.xfer2(to_send)
    to_send = [WRSR_INSTRUCTION, 0x00]
    spi.xfer2(to_send)
    to_send = [RDSR_INSTRUCTION, 0x00]
    spi.xfer2(to_send)
    print(str(to_receive))

def write_sst25(spi, address, data):
    length = len(data)
    if (length % 2) == 1:
        data = data + [255] 
    i = 0
    spi.xfer([WREN_INSTRUCTION])
    while i < length:
        add = [((address + i) >> 16), (((address + i) >> 8) & 0x000000FF), ((address+ i) & 0x000000FF)]
        to_receive = spi.xfer2([AAI_WORD_PROG_INSTRUCTION] + add + data[i:i+2])
        print(str([AAI_WORD_PROG_INSTRUCTION] + add + data[i:i+2]))
        i = i + 2
        status = read_status(spi)
        while (status & 0x01) == 0x01:
            status = read_status(spi)
    print("Status: " + str(read_status(spi)))
    spi.xfer([WRDI_INSTRUCTION])
    return to_receive

def read_sst25(spi, address, len):
    data = [READ_INSTRUCTION] + address
    for i in range(len):
        data = data + [0x00]
    to_receive = spi.xfer2(data)
    return to_receive[4::]

spi = spidev.SpiDev()
spi.open(0, 0)
print("Status: " + str(read_status(spi)))
#chip_erase(spi)

enable_write(spi)
time.sleep(0.5)
to_send = [0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18]
address = 0x00
write_sst25(spi, address, to_send)
time.sleep(0.5)
to_read = read_sst25(spi, [0x00, 0x00, 0x00], 8)
print(str(to_read))
print("Status: " + str(read_status(spi)))
spi.close()
