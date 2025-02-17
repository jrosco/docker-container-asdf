import json

# Define the .env file path
env_file = "config/environment"

# Read and parse the .env file
versions = {}
with open(env_file, "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            versions[key] = value.strip('"')

# Construct version strings
golang_version = versions.get("GOLANG_VERSION", "unknown")
alpine_version = f'{versions.get("ALPINE_MAJOR_VERSION", "0")}.{versions.get(
    "ALPINE_MINOR_VERSION", "0")}.{versions.get("ALPINE_PATCH_VERSION", "0")}'
debian_version = f'{versions.get("DEBIAN_MAJOR_VERSION", "0")}.{
    versions.get("DEBIAN_MINOR_VERSION", "0")}'
asdf_version = f'{versions.get("ASDF_MAJOR_VERSION", "0")}.{versions.get(
    "ASDF_MINOR_VERSION", "0")}.{versions.get("ASDF_PATCH_VERSION", "0")}'

# Define badge properties (color only)
badges = {
    "golang": {
        "label": "Go",
        "message": golang_version,
        "color": "blue",
        "logo": "goland",
        "style": "for-the-badge"
    },
    "alpine": {
        "label": "Alpine",
        "message": alpine_version,
        "color": "0095D5",
        "logo": "alpinelinux",
        "style": "for-the-badge"
    },
    "debian": {
        "label": "Debian",
        "message": debian_version,
        "color": "A81D33",
        "logo": "debian",
        "style": "for-the-badge"
    },
    "asdf": {
        "label": "ASDF",
        "message": asdf_version,
        "color": "ff69b4",
        "logo": "gnubash",
        "style": "for-the-badge"
    }
}

# Generate JSON files for each badge
for key, data in badges.items():
    badge_json = {
        "schemaVersion": 1,
        "label": data["label"],
        "message": data["message"],
        "color": data["color"],
        "style": data["style"]

    }
    with open(f"docs/badges/{key}.json", "w") as f:
        json.dump(badge_json, f, indent=4)

print("✅ Update: Badges JSON generated")
