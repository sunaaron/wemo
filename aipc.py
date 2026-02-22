import pywemo
import sys

AIPC_DEVICE_NAME = "AI PC"  

def turn_on_aipc():
    """
    Discover all Wemo devices and turn on any that are named 'AI PC'.
    """
    print("Scanning for Wemo devices to turn on 'AI PC'...")
    try:
        devices = pywemo.discover_devices()
        for device in devices:
            if device.name == AIPC_DEVICE_NAME and device.get_state() == 0:  # Only turn on if it's currently off
                device.on()
                print(f"Turned on device: {device.name}")
    except Exception as e:
        print(f"Error discovering or controlling devices: {e}")


def turn_off_aipc():
    """
    Discover all Wemo devices and turn off any that are named 'AI PC'.
    """
    print("Scanning for Wemo devices to turn off 'AI PC'...")
    try:
        devices = pywemo.discover_devices()
        for device in devices:
            if device.name == AIPC_DEVICE_NAME and device.get_state() == 1:  # Only turn off if it's currently on 
                device.off()
                print(f"Turned off device: {device.name}")
    except Exception as e:
        print(f"Error discovering or controlling devices: {e}")


def main():
    """
    Main function to handle command line arguments.
    Accepts 'on' or 'off' as argument and calls appropriate function.
    """
    if len(sys.argv) != 2:
        print("Usage: python aipc.py [on|off]")
        return
    
    arg = sys.argv[1].lower()
    
    if arg == "on":
        turn_on_aipc()
    elif arg == "off":
        turn_off_aipc()
    else:
        print("Invalid argument. Please use 'on' or 'off'")


if __name__ == "__main__":
    main()
