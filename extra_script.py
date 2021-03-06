Import("env")

# Get avrdude.conf path
import os
platform = env.PioPlatform()
avrdude_dir = platform.get_package_dir("tool-avrdude")
avrdude_conf = os.path.join(avrdude_dir, "avrdude.conf")

# Fetch values from platformio.ini
target = str(env.GetProjectOption("board"))                         # ATmega328P for instance
uploader = str(env.GetProjectOption("upload_protocol"))							# Avrdude supported programmer
uploader_flags = str("".join(env.GetProjectOption("upload_flags"))) # Extra Avrdude flags
baud_rate = str(env.GetProjectOption("board_upload.speed"))         # Bootloader upload baud rate

# Default values if not specified in platformio.ini
f_cpu = "8000000L"
oscillator = "internal"
bod = "2.7v"
eesave = "yes"
uart = "uart0"



def get_lfuse():
    # Return manually defined low fuse if present in platformio.ini
    if(str(env.GetProjectOption("board_fuses.lfuse")) != "None"):
        return int(env.GetProjectOption("board_fuses.lfuse"), 0)

    if(target == "ATmega2561" or target == "ATmega2560"  or target == "ATmega1284"  or target == "ATmega1284P" or \
       target == "ATmega1281" or target == "ATmega1280"  or target == "ATmega644A"  or target == "ATmega644P"  or \
       target == "ATmega640"  or target == "ATmega328"   or target == "ATmega328P"  or target == "ATmega324A"  or \
       target == "ATmega324P" or target == "ATmega324PA" or target == "ATmega168"   or target == "ATmega168P"  or \
       target == "ATmega164A" or target == "ATmega164P"  or target == "ATmega88"    or target == "ATmega88P"   or \
       target == "ATmega48"   or target == "ATmega48P"):
        if(oscillator == "external"):
            return 0xf7
        else:
            if(f_cpu == "8000000L"):
                return 0xe2
            else:
                return 0x62
    
    elif(target == "ATmega328PB" or target == "ATmega324PB" or target == "ATmega168PB" or target == "ATmega162" or \
         target == "ATmega88PB"  or target == "ATmega48PB"  or target == "AT90CAN128"  or target == "AT90CAN64" or \
         target == "AT90CAN32"):
        if(oscillator == "external"):
            return 0xff
        else:
            if(f_cpu == "8000000L"):
                return 0xe2
            else:
                return 0x62

    elif(target == "ATmega8535" or target == "ATmega8515" or target == "ATmega32" or target == "ATmega16" or  \
         target == "ATmega8"):
        if(bod == "4.0v"):
            bod_bits = 0b11
        elif(bod == "2.7v"):
            bod_bits = 0b01
        else:
            bod_bits = 0b00

        if(oscillator == "external"):
            return 0xff & ~(bod_bits << 6)
        else:
            if(f_cpu == "8000000L"):
                return 0xe4 & ~(bod_bits << 6)
            else:
                return 0xe1 & ~(bod_bits << 6)

    elif(target == "ATtiny13" or target == "ATtiny13A"):
        # Get eesave value
        if(eesave == "yes"):
            eesave_bit = 1
        else:
            eesave_bit = 0
        if(oscillator == "external"):
            return 0x78 & ~(eesave_bit << 6)
        else:
            if(f_cpu == "9600000L" or f_cpu == "8000000L"):
                return 0x7a & ~(eesave_bit << 6) # Defaults to 9.6 MHz
            elif(f_cpu == "4800000L"):
                return 0x79 & ~(eesave_bit << 6)
            elif(f_cpu == "1200000L"):
                return 0x6a & ~(eesave_bit << 6)
            elif(f_cpu == "600000L"):
                return 0x69 & ~(eesave_bit << 6)
            elif(f_cpu == "128000L"):
                return 0x7b & ~(eesave_bit << 6)
            elif(f_cpu == "16000L"):
                return 0x6b & ~(eesave_bit << 6)

    else:
        # Return negative value if low fuse could not be calculated
        return -1


def get_hfuse():
    # Return manually defined hfuse if present in platformio.ini
    if(str(env.GetProjectOption("board_fuses.hfuse")) != "None"):
        return int(env.GetProjectOption("board_fuses.hfuse"), 0)
    
    # Get eesave value
    if(eesave == "yes"):
        eesave_bit = 1
    else:
        eesave_bit = 0

    # Get ckopt for targets that uses this
    if(oscillator == "external"):
        ckopt_bit = 1
    else:
        ckopt_bit = 0

    if(target == "ATmega2561" or target == "ATmega2560" or target == "ATmega1284"  or target == "ATmega1284P" or \
       target == "ATmega1281" or target == "ATmega1280" or target == "ATmega644A"  or target == "ATmega644P"  or \
       target == "ATmega640"  or target == "ATmega328"  or target == "ATmega328P"  or target == "ATmega328PB" or \
       target == "ATmega324A" or target == "ATmega324P" or target == "ATmega324PA" or target == "ATmega324PB" or \
       target == "AT90CAN128" or target == "AT90CAN64"  or target == "AT90CAN32"):
        if(uart == "no_bootloader"):
            return 0xdf & ~(eesave_bit << 3)
        else:
            return 0xde & ~(eesave_bit << 3)

    elif(target == "ATmega164A"  or target == "ATmega164P" or target == "ATmega162"):
        if(uart == "no_bootloader"):
            return 0xdd & ~(eesave_bit << 3)
        else:
            return 0xdc & ~(eesave_bit << 3)
    
    elif(target == "ATmega168" or target == "ATmega168P" or target == "ATmega168PB" or target == "ATmega88"  or \
         target == "ATmega88P" or target == "ATmega88PB" or target == "ATmega48"    or target == "ATmega48P" or \
         target == "ATmega48PB"):
        if(bod == "4.3v"):
            return 0xdc & ~(eesave_bit << 3)
        elif(bod == "2.7v"):
            return 0xdd & ~(eesave_bit << 3)
        elif(bod == "1.8v"):
            return 0xde & ~(eesave_bit << 3)
        else:
            return 0xdf & ~(eesave_bit << 3)

    elif(target == "ATmega128" or target == "ATmega64" or target == "ATmega32"):
        if(uart == "no_bootloader"):
            return 0xdf & ~(ckopt_bit << 4) & ~(eesave_bit << 3)
        else:
            return 0xde & ~(ckopt_bit << 4) & ~(eesave_bit << 3)
    
    elif(target == "ATmega8535" or target == "ATmega8515" or target == "ATmega16" or target == "ATmega8"):
        if(uart == "no_bootloader"):
            return 0xdd & ~(ckopt_bit << 4) & ~(eesave_bit << 3)
        else:
            return 0xdc & ~(ckopt_bit << 4) & ~(eesave_bit << 3)

    elif(target == "ATtiny13" or target == "ATtiny13A"):
        if(bod == "4.3v"):
            return 0x9
        elif(bod == "2.7v"):
            return 0xfb
        elif(bod == "1.8v"):
            return 0xfd
        else:
            return 0xff

    else:
        return -1

def get_efuse():
    # Return manually defined efuse if present in platformio.ini
    if(str(env.GetProjectOption("board_fuses.efuse")) != "None"):
        return int(env.GetProjectOption("board_fuses.efuse"), 0)

    if(target == "ATmega2561" or target == "ATmega2560"  or target == "ATmega1284" or target == "ATmega1284P" or \
       target == "ATmega1281" or target == "ATmega1280"  or target == "ATmega644A" or target == "ATmega644P"  or \
       target == "ATmega640"  or target == "ATmega328"   or target == "ATmega328P" or target == "ATmega324A"  or \
       target == "ATmega324P" or target == "ATmega324PA" or target == "ATmega164A" or target == "ATmega164P"):
        if(bod == "4.3v"):
            return 0xfc
        elif(bod == "2.7v"):
            return 0xfd
        elif(bod == "1.8v"):
            return 0xfe
        else:
            return 0xff

    elif(target == "ATmega328PB" or target == "ATmega324PB"):
        if(bod == "4.3v"):
            return 0xf4
        elif(bod == "2.7v"):
            return 0xf5
        elif(bod == "1.8v"):
            return 0xf6
        else:
            return 0xf7

    elif(target == "ATmega168" or target == "ATmega168P" or target == "ATmega168PB" or target == "ATmega88" or \
         target == "ATmega88P" or target == "ATmega88PB"):
        if(uart == "no_bootloader"):
            return 0xfd
        else:
            return 0xfc

    elif(target == "ATmega128" or target == "ATmega64" or target == "ATmega48" or target == "ATmega48P"):
        return 0xff
    
    elif(target == "AT90CAN128" or target == "AT90CAN64" or target == "AT90CAN32"):
        if(bod == "4.1v"):
            return 0xfd
        elif(bod == "4.0v"):
            return 0xfb
        elif(bod == "3.9v"):
            return 0xf9
        elif(bod == "3.8v"):
            return 0xf7
        elif(bod == "2.7v"):
            return 0xf5
        elif(bod == "2.6v"):
            return 0xf3
        elif(bod == "2.5v"):
            return 0xf1
        else:
            return 0xff

    else:
        return -1



def get_lock_fuse():
    if(str(env.GetProjectOption("board_fuses.lock")) != "None"):
        return int(env.GetProjectOption("board_fuses.lock"), 0)
    else:
        return 0x0f



def fuses(*args, **kwargs):
    global f_cpu
    global uart
    global oscillator
    global bod
    global eesave
    global avrdude_conf
    global uploader
    global uploader_flags

    # Define F_CPU
    if(str(env.GetProjectOption("board_build.f_cpu")) != "None"):
        f_cpu = str(env.GetProjectOption("board_build.f_cpu")).upper()
        print("\n\nClock speed specified\t\tUsing board_build.f_cpu = %s" % f_cpu)
    else:
        print("\n\nClock speed not specified\tUsing board_build.f_cpu = %s" % f_cpu)

    # Define UART port
    if(str(env.GetProjectOption("hardware.uart")).lower() == "uart0" or str(env.GetProjectOption("hardware.uart")).lower() == "uart1" or str(env.GetProjectOption("hardware.uart")).lower() == "uart2" or str(env.GetProjectOption("hardware.uart")).lower() == "uart3"):
        uart = str(env.GetProjectOption("hardware.uart")).lower()
        print("UART port specified\t\tUsing hardware.uart = %s" % uart)
    elif(str(env.GetProjectOption("hardware.uart")) != "None"):
        uart = "no_bootloader"
        print("UART not specified\t\tNo bootloader will be installed")
    else:
        print("UART port not specified\t\tDefault is hardware.uart = %s" % uart)
    
    # Define internal or external oscillator
    if(str(env.GetProjectOption("hardware.oscillator")).lower() == "internal" or str(env.GetProjectOption("hardware.oscillator")).lower() == "external"):
        oscillator = str(env.GetProjectOption("hardware.oscillator")).lower()
        print("Oscillator specified\t\tUsing hardware.oscillator = %s" % oscillator)
    else:
        print("Oscillator not specified\tUsing hardware.oscillator = %s" % oscillator)

    # Define BOD level
    if(str(env.GetProjectOption("hardware.bod")) != "None"):
        bod = str(env.GetProjectOption("hardware.bod")).lower()
        print("BOD level specified\t\tUsing hardware.bod = %s" % bod)
    else:
        print("BOD level not specified\t\tUsing hardware.bod = %s" % bod)

    # Define EE save
    if(str(env.GetProjectOption("hardware.eesave")).lower() == "true" or str(env.GetProjectOption("hardware.eesave")).lower() == "yes" or str(env.GetProjectOption("hardware.eesave")) == "enabled"):
        eesave = "yes"
        print("EESAVE specified\t\tEEPROM will be retained")
    elif(str(env.GetProjectOption("hardware.eesave")).lower() == "false" or str(env.GetProjectOption("hardware.eesave")).lower() == "no" or str(env.GetProjectOption("hardware.eesave")) == "disabled"):
        eesave = "no"
        print("EESAVE specified\t\tEEPROM will not be retained")
    else:
        eesave = "yes"
        print("EESAVE not specified\t\tEEPROM will be retained")

    # Store and format fuses
    low_fuse = str("{0:#0{1}x}".format(get_lfuse(),4))
    high_fuse = str("{0:#0{1}x}".format(get_hfuse(),4))
    ext_fuse = str("{0:#0{1}x}".format(get_efuse(),4))

    # Prevent unsupported targets to execute Avrdude
    if(low_fuse == "-0x1" or high_fuse == "-0x1"):
        print("Target %s not supported, Aborting..." % target)
        return -1
    else:
        print("\nCalculated lfuse: %s" % low_fuse)
        print("Calculated hfuse: %s" % high_fuse)
        print("Calculated efuse: %s\n" % ext_fuse)

        # Generate fuses command and run Avrdude
        fuses_cmd = "avrdude -C%s -p%s -c%s %s -v -Ulock:w:0x3f:m -Ulfuse:w:%s:m -Uhfuse:w:%s:m %s" % (avrdude_conf, target.lower(), uploader, uploader_flags, low_fuse, high_fuse, ("-Uefuse:w:%s:m" % ext_fuse if ext_fuse != "-0x1" else ""))
        return env.Execute(fuses_cmd)



def bootloader(*args, **kwargs):
    global target
    global f_cpu
    global uart
    global baud_rate
    global avrdude_conf
    global uploader
    global uploader_flags

    # Do not burn bootloader for targets that doesn't support it
    if(target == "ATmega48" or target == "ATmega48P" or target == "ATtiny13"):
        print("\n\nError target %s doesn't support bootloader" % target)
        return -1

    # Define F_CPU
    if(str(env.GetProjectOption("board_build.f_cpu")) != "None"):
        f_cpu = str(env.GetProjectOption("board_build.f_cpu")).upper()
        print("\n\nClock speed specified\t\tUsing board_build.f_cpu = %s" % f_cpu)
    else:
        print("\n\nClock speed not specified\tUsing board_build.f_cpu = %s" % f_cpu)

    # Define UART port
    if(str(env.GetProjectOption("hardware.uart")).lower() == "uart0" or str(env.GetProjectOption("hardware.uart")).lower() == "uart1" or str(env.GetProjectOption("hardware.uart")).lower() == "uart2" or str(env.GetProjectOption("hardware.uart")).lower() == "uart3"):
        uart = str(env.GetProjectOption("hardware.uart")).lower()
        print("UART port specified\t\tUsing hardware.uart = %s" % uart)
    elif(str(env.GetProjectOption("hardware.uart")) != "None"):
        uart = "no_bootloader"
        print("UART not specified\t\tNo bootloader will be installed")
    else:
        print("UART port not specified\t\tDefault is hardware.uart = %s" % uart)

    # Baud rate guard
    if(baud_rate != "None"):
        print("Baud rate specified\t\tUsing board_upload.speed = %s\n" % baud_rate)
    else:
        print("Baud rate not specified.\tPlease specify board_upload.speed in platformio.ini\n")
        return -1
    
    lock_fuse = str("{0:#0{1}x}".format(get_lock_fuse(),4))
    print("Calculated lock fuse: %s\n" % lock_fuse)

    # Does the target have a BIGBOOT bootloader?
    if(target == "ATmega2561" or target == "ATmega2560" or target == "ATmega1284" or target == "ATmega1284P" or \
       target == "ATmega1281" or target == "ATmega1280" or target == "ATmega644A" or target == "ATmega644P"  or \
       target == "ATmega640"  or target == "ATmega128"  or target == "ATmega64"   or target == "AT90CAN128"  or \
       target == "AT90CAN64"  or target == "AT90CAN32"):
        bigboot = "_BIGBOOT"
    else:
        bigboot = ""

    # Generate bootloader command and run Avrdude
    bootloader_file = str(platform.get_package_dir("framework-arduinoavr")) + "/optiboot_flash/bootloaders/%s/%s/optiboot_flash_%s_%s_%s_%s%s.hex" % (target.lower(), f_cpu, target.lower(), uart.upper(), baud_rate, f_cpu, bigboot)
    bootloader_cmd = "avrdude -C%s -p%s -c%s %s -v -Uflash:w:%s:i -Ulock:w:%s:m" % (avrdude_conf, target.lower(), uploader, uploader_flags, bootloader_file, lock_fuse)
    return env.Execute(bootloader_cmd)



env.AlwaysBuild(env.Alias("fuses", None, fuses))
env.AlwaysBuild(env.Alias("bootloader", None, bootloader))
