import json

filename = 'current.json'


def dict_discover(key, value, indent):
    print(f'{" " * indent}{key} (dict of {len(value)} items):')
    for k, v in value.items():
        json_discover(k, v, indent + 2)


def list_discover(key, value, indent):
    print(f'{" " * indent}{key} (list of {len(value)} items):')
    for i, item in enumerate(value):
        json_discover(f'{key}[{i}]', item, indent + 2)


def json_discover(key, value, indent=0):
    if isinstance(value, dict):
        dict_discover(key, value, indent)
    elif isinstance(value, list):
        list_discover(key, value, indent)
    else:
        print(' ' * indent + f'{key} ({type(value).__name__})')

if __name__ == '__main__':
    print('=' * 20)
    with open(filename) as in_file:
        json_discover('data', json.load(in_file))
