// DOM Elements
const controlHelp = document.getElementById("control-help");
const imageOverlay = document.getElementById("image-overlay");
const controlIds = document.getElementById("control-ids");
const controlInvalid = document.getElementById("control-invalid");
const controlSubmit = document.getElementById("control-submit");
const resultsCard = document.getElementById("results-card");
const resultsContainer = document.getElementById("results-container");
const recommendedVersion = document.getElementById("recommended-version");
const preloader = document.getElementById("preloader");

// Event Listener
controlSubmit.addEventListener("click", handleSubmit);

controlHelp.addEventListener("click", () => {
  imageOverlay.style.display = "block";
});

imageOverlay.addEventListener("click", () => {
  imageOverlay.style.display = "none";
});

// Main submit handler
async function handleSubmit(e) {
	const ids = parseIds(controlIds.value);

	if (ids.length === 0) return;

	if (!validateIds(ids)) {
		showValidationError();
		return;
	}

	hideValidationError();
	preloader.style.display = 'flex';

	try {
		const uniqueIds = [...new Set(ids)];
		const response = await fetch("/api", {
			method: "POST",
			body: JSON.stringify(uniqueIds),
			headers: {
				"Content-Type": "application/json"
			}
		});

		if (!response.ok) {
			console.error("API returned an error");
			return;
		}

		const data = await response.json();
		displayResults(data.mods, data.recommended_version, data.incompatible_mods);
		console.log(data);

	} catch (err) {
		console.error("Error during fetch:", err);
	} finally {
		preloader.style.display = 'none';
	}
}

// Parse IDs from textarea input
function parseIds(rawInput) {
	return rawInput
		.replace(/\r\n/g, "\n")
		.split("\n")
		.map(id => id.trim())
		.filter(id => id.length > 0);
}

// Validate that all IDs are digits
function validateIds(ids) {
	return ids.every(id => /^[0-9]+$/.test(id));
}

// Show/Hide validation error
function showValidationError() {
	controlIds.style.borderColor = "red";
	controlInvalid.style.display = "block";
}
function hideValidationError() {
	controlIds.style.borderColor = "initial";
	controlInvalid.style.display = "none";
}

function displayResults(mods, recommendedVersionText, incompatibleMods = []) {
	resultsContainer.innerHTML = '';

	// Render mod list
	for (const modId in mods) {
		if (mods.hasOwnProperty(modId)) {
			const mod = mods[modId];

			const modBlock = document.createElement("div");
			modBlock.classList.add("mod-block");

			const modName = document.createElement("h2");
			modName.textContent = mod.name;

			const versionList = document.createElement("ul");
			versionList.classList.add("version-list");

			mod.versions.forEach(version => {
				const li = document.createElement("li");
				li.textContent = version;
				versionList.appendChild(li);
			});

			modBlock.appendChild(modName);
			modBlock.appendChild(versionList);
			resultsContainer.appendChild(modBlock);
		}
	}

	// Recommended version
	recommendedVersion.textContent = recommendedVersionText || 'N/A';

	// Handle incompatible mods
	const incompatibleSection = document.getElementById("incompatible-section");
	const incompatibleList = document.getElementById("incompatible-list");

	if (incompatibleMods && incompatibleMods.length > 0) {
		incompatibleList.innerHTML = '';
		incompatibleMods.forEach(name => {
			const li = document.createElement("li");
			li.textContent = name;
			incompatibleList.appendChild(li);
		});
		incompatibleSection.style.display = "block";
	} else {
		incompatibleSection.style.display = "none";
	}

	resultsCard.style.display = "block";
}
