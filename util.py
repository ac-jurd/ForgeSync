import os
from collections import Counter

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


def find_best_minecraft_version_and_incompatibles(results):
    version_counts = Counter()
    for mod_data in results.values():
        unique_versions = set(mod_data.get("versions", []))
        version_counts.update(unique_versions)

    if not version_counts:
        return None, 0, []

    best_version, max_count = version_counts.most_common(1)[0]

    # Find mods that do NOT support best_version
    incompatible_mods = [
        mod_data["name"]
        for mod_data in results.values()
        if best_version not in mod_data.get("versions", [])
    ]

    return best_version, max_count, incompatible_mods
