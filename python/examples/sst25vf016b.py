import spidev

# spi.open(0,0)	                ffnet den SPI-Bus 0 mit CS0
# spi.open(0,1)	                ffnet den SPI-Bus 0 mit CS1
# spi.close()	                Schliesst den SPI-Bus
# spi.readbytes(len)	        Liest len Bytes vom SPI-Slave
# spi.writebytes([array of bytes])	Sendet ein Byte-Array zum SPI-Slave
# spi.xfer([array of bytes])	Sendet ein Byte-Array, CEx wird vor jedem Byte aktiv und dann wieder inaktiv
# spi.xfer2([array of bytes])	Sendet ein Byte-Array, dabei bleibt CEx dauerhaft aktiv

# SPI transfer: 1 byte instruction + 3 bytes address + n bytes write or read

READ_INSTRUCTION          = 0x03
WRITE_INSTRUCTION         = 0x0B
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


spi = spidev.SpiDev()
spi.open(0,0)
#to_send = [0x03, 0x00, 0x00, 0x00, 0x00]
to_send = [RDID_INSTRUCTION, 0x00, 0x00, 0x00]
to_receive = spi.xfer(to_send)
print(str(to_receive))
spi.close()
