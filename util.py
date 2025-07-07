import os

def parse_env(path: str = '.env') -> dict[str, str]:
    if not os.path.exists(path):
        return {}

    d = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue  # Skip malformed lines
            key, val = line.split('=', 1)
            d[key.strip()] = val.strip()
    return d
