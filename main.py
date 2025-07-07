from flask import Flask, render_template, request, jsonify
from util import parse_env, find_best_minecraft_version_and_incompatibles
from api import Api

MAX_CONTENT_LENGTH = 1024 * 1024

env = parse_env()
api = Api(env['CF_API_KEY'])
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api_handler():
    if request.content_length and request.content_length > MAX_CONTENT_LENGTH:
        return 'Request entity too large', 413

    try:
        data = request.get_json(force=True)
    except Exception as e:
        print('JSON parsing error:', e)
        return 'Invalid JSON', 400

    if not isinstance(data, list) or len(data) == 0:
        return 'Expected non-empty list of IDs', 400

    ids = []
    for d in data:
        try:
            i = int(d)
            ids.append(i)
        except (ValueError, TypeError):
            return 'Data contains invalid ID', 400

    print('Loading...')

    results = {}
    for mod_id in ids:
        mc_versions, _ = api.get_mod_versions_and_loaders(mod_id)
        mc_name = api.get_mod_name(mod_id)

        if not mc_name or not mc_versions:
            # Skip invalid mod data but keep going
            continue

        results[str(mod_id)] = {
            "name": mc_name,
            "versions": mc_versions
        }

    if not results:
        return "No valid mod data found", 500

    best_version, compatible_mod_count, incompatible_mod_names = find_best_minecraft_version_and_incompatibles(results)

    response = {
        "mods": results,
        "recommended_version": best_version,
        "compatible_mod_count": compatible_mod_count,
        "incompatible_mods": incompatible_mod_names
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
