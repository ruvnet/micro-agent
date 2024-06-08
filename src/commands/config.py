import configparser
import sys
from pathlib import Path

def show_config_ui():
    # Placeholder for UI-based configuration management
    pass

def get_config():
    config = configparser.ConfigParser()
    config.read(Path.home() / '.micro-agent')
    return config

def set_config(key, value):
    config = get_config()
    if 'DEFAULT' not in config:
        config['DEFAULT'] = {}
    config['DEFAULT'][key] = value
    with open(Path.home() / '.micro-agent', 'w') as configfile:
        config.write(configfile)

def config_command(argv):
    try:
        if len(argv) < 2 or argv[1] in ['--help', '-h']:
            print("Usage: config [get|set|ui] [key=value...]")
            sys.exit(1)

        mode = argv[1]
        key_values = argv[2:]

        if mode == 'ui':
            show_config_ui()
        elif mode == 'get':
            config = get_config()
            for key in key_values:
                if key in config['DEFAULT']:
                    print(f"{key}={config['DEFAULT'][key]}")
                else:
                    print(f"Error: Key {key} not found", file=sys.stderr)
                    sys.exit(1)
        elif mode == 'set':
            for key_value in key_values:
                key, value = key_value.split('=')
                set_config(key, value)
            print("Config updated ✅")
        else:
            print(f"Invalid mode: {mode}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    config_command(sys.argv)
