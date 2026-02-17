import logging
from flask import Flask, render_template, request, jsonify
import pywemo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Global cache for device objects
device_cache = {}


def discover_wemo_devices():
    """
    Discover all Wemo devices on the network.
    
    Returns:
        List of device dictionaries with name, type, and state information
    """
    global device_cache
    try:
        devices = pywemo.discover_devices()
        device_list = []
        device_cache.clear()  # Clear old cache
        
        for device in devices:
            device_info = {
                'name': device.name,
                'type': type(device).__name__,
                'state': device.get_state(),
                'state_text': 'On' if device.get_state() == 1 else 'Off'
            }
            device_list.append(device_info)
            # Cache the device object for later control
            device_cache[device.name] = device
        
        return device_list
    except Exception as e:
        logger.exception("Error discovering devices:")
        return []


@app.route('/')
def index():
    """Homepage that displays all available Wemo devices."""
    logger.info("Scanning for Wemo devices...")
    devices = discover_wemo_devices()
    return render_template('index.html', devices=devices)


@app.route('/toggle', methods=['POST'])
def toggle_device():
    """Toggle a Wemo device on or off."""
    try:
        data = request.get_json()
        device_name = data.get('device_name')
        new_state = data.get('state')  # 1 for on, 0 for off
        
        if not device_name or new_state is None:
            return jsonify({'success': False, 'error': 'Missing device_name or state'}), 400
        
        # Get device from cache
        device = device_cache.get(device_name)
        if not device:
            # Try to rediscover devices
            discover_wemo_devices()
            device = device_cache.get(device_name)
            
        if not device:
            return jsonify({'success': False, 'error': 'Device not found'}), 404
        
        # Toggle the device
        if new_state == 1:
            device.on()
            logger.info(f"Turned ON device: {device_name}")
        else:
            device.off()
            logger.info(f"Turned OFF device: {device_name}")
        
        # Verify the state change
        actual_state = device.get_state()
        
        return jsonify({
            'success': True,
            'device_name': device_name,
            'state': actual_state,
            'state_text': 'On' if actual_state == 1 else 'Off'
        })
        
    except Exception as e:
        logger.exception("Error toggling device:")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == "__main__":
    # Run Flask app on a free port (5000 by default)
    print("Starting Wemo Web Controller...")
    print("Access the application at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
