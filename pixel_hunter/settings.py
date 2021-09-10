from pathlib import Path
import yaml

__all__ = ('load_config', )


def load_config(config_file=None):
    default_file = Path(__file__).parent / 'config.yaml'
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    user_config = {}

    if config_file:
        user_config = yaml.safe_load(config_file)

    config.update(**user_config)

    return config
