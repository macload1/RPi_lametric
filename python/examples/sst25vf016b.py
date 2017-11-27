import spidev

# spi.open(0,0)	                Öffnet den SPI-Bus 0 mit CS0
# spi.open(0,1)	                Öffnet den SPI-Bus 0 mit CS1
# spi.close()	                Schliesst den SPI-Bus
# spi.readbytes(len)	        Liest len Bytes vom SPI-Slave
# spi.writebytes([array of bytes])	Sendet ein Byte-Array zum SPI-Slave
# spi.xfer([array of bytes])	Sendet ein Byte-Array, CEx wird vor jedem Byte aktiv und dann wieder inaktiv
# spi.xfer2([array of bytes])	Sendet ein Byte-Array, dabei bleibt CEx dauerhaft aktiv

# SPI transfer: 1 byte instruction + 3 bytes address + n bytes write or read

spi = spidev.SpiDev()
spi.open(0,0)
to_send = [0x03, 0x00, 0x00, 0x00, 0x00]
to_receive = spi.xfer(to_send)
print(str(to_receive))
spi.close()
