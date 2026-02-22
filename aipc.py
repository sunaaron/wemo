import pywemo


def turn_on_aipc():
    """
    Discover all Wemo devices and turn on any that are named 'AIPC'.
    """
    try:
        devices = pywemo.discover_devices()
        for device in devices:
            if device.name == 'AIPC' and device.get_state() == 0:  # Only turn on if it's currently off
                device.on()
                print(f"Turned on device: {device.name}")
    except Exception as e:
        print(f"Error discovering or controlling devices: {e}")


def turn_off_aipc():
    """
    Discover all Wemo devices and turn off any that are named 'AIPC'.
    """
    try:
        devices = pywemo.discover_devices()
        for device in devices:
            if device.name == 'AIPC' and device.get_state() == 1:  # Only turn off if it's currently on 
                device.off()
                print(f"Turned off device: {device.name}")
    except Exception as e:
        print(f"Error discovering or controlling devices: {e}")

