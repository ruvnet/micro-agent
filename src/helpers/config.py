import configparser
import os
from typing import Any, Dict, Tuple
import sys

config = configparser.ConfigParser()
config_path = os.path.join(os.path.expanduser('~'), '.micro-agent')

def read_config_file() -> Dict[str, Any]:
    config.read(config_path)
    return {s: dict(config.items(s)) for s in config.sections()}

def has_own(object: Dict[str, Any], key: str) -> bool:
    return key in object

def get_config(cli_config: Dict[str, Any] = None) -> Dict[str, Any]:
    file_config = read_config_file()
    combined_config = {**file_config, **(cli_config or {}), **os.environ}
    return combined_config

def set_configs(key_values: Tuple[str, str]) -> None:
    if not config.has_section('DEFAULT'):
        config.add_section('DEFAULT')
    for key, value in key_values:
        config.set('DEFAULT', key, value)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def show_config_ui() -> None:
    try:
        config = get_config()
        # Placeholder for UI logic
        print("Configuration UI not implemented.")
    except Exception as e:
        print(f"\n{str(e)}", file=sys.stderr)
        sys.exit(1)
