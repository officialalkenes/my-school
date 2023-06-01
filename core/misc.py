import yaml


def coerce_yaml(value):
    if isinstance(value, str):
        return yaml.load(f"dummy: {value}", Loader=yaml.SafeLoader)["dummy"]
    return value
