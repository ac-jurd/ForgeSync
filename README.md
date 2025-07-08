# 🧱 ForgeSync

**ForgeSync** is a lightweight web tool built with Flask that helps Minecraft modpack creators determine the most compatible Minecraft version for a list of mods from [CurseForge](https://www.curseforge.com/minecraft/mc-mods). 

Simply input a list of mod IDs, and the tool fetches their supported versions via the CurseForge API, analyzes the data, and recommends the version with the highest compatibility.

---

## 🚀 Features

- 🧩 Determine the best Minecraft version for a list of mods
- 📦 Check which mods are incompatible with the suggested version
- 🔄 Caches mod data locally to reduce API calls
- 🌐 Simple web interface with Bootstrap styling
- ⚡ API endpoint for programmatic access

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **API**: CurseForge API
- **Utilities**: Requests, caching with `OrderedDict`, `.env` parsing

---

## 📸 Demo

1. Paste CurseForge mod IDs into the input box (one per line).
2. Click **Submit**.
3. View:
   - All supported versions for each mod
   - Recommended Minecraft version
   - List of mods that don't support the recommended version

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/ac-jurd/ForgeSync.git
cd ForgeSync
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your CurseForge API key

Create a `.env` file in the root directory with the following contents:

```bash
CF_API_KEY=<your_curseforge_api_key>
```

### 🧪 Running the App

```bash
python main.py
```

Then open your browser to `http://localhost:5000`.

> **Note:** The built-in Flask server is intended for development and testing purposes only.  
> For deploying this app in a production environment, it is recommended to use a production-ready WSGI server such as **Gunicorn** or **uWSGI**, typically behind a reverse proxy like **Nginx**. This ensures better performance, security, and stability.

### 📡 API Endpoint

### `POST /api`

**Request Body**: JSON array of CurseForge mod IDs  
**Example**:

```json
[238222, 268560, 314904]
```

**Response**:

```json
{
  "mods": {
    "238222": {
      "name": "JEI",
      "versions": ["1.18.2", "1.19.2", "1.20.1"]
    },
    ...
  },
  "recommended_version": "1.18.2",
  "compatible_mod_count": 3,
  "incompatible_mods": ["Mod X", "Mod Y"]
}
```

### 📁 Project Structure

```graphql
.
├── main.py                # Main Flask application
├── api.py                # Handles CurseForge API interaction
├── util.py               # Utilities: env parsing, version analysis
├── templates/
│   └── index.html        # Frontend page template
├── static/
│   ├── main.js           # Frontend JS logic
│   ├── style.css         # CSS
│   └── favicon.ico       # Favicon
├── .env                  # Contains your CurseForge API key
└── requirements.txt      # Python dependencies
```

### 🔒 Notes on Usage

- This tool respects CurseForge API rate limits with polite delays.

- Caching helps reduce repeated API calls within a 10-minute window.

- The frontend includes guidance on how to find mod IDs.

### 🙌 Acknowledgements

- [CurseForge API](https://docs.curseforge.com/)

- [Bootstrap 5](https://getbootstrap.com/)
