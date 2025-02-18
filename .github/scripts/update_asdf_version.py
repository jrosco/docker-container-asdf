import requests
import re

# Define the source for the latest ASDF version
ASDF_URL = "https://api.github.com/repos/asdf-vm/asdf/releases/latest"

# Read the .env file while preserving comments and structure
env_file = "config/environment"
env_lines = []

with open(env_file, "r") as f:
    # Keep all lines, including comments and formatting
    env_lines = f.readlines()


# Fetch the latest ASDF version
def get_latest_asdf_version():
    try:
        response = requests.get(ASDF_URL, timeout=10)
        response.raise_for_status()
        latest_version = response.json().get(
            "tag_name", "").lstrip("v")  # Remove 'v' prefix
        return latest_version
    except Exception as e:
        print(f"Error fetching ASDF version: {e}")
        return None


# Get latest ASDF version
latest_asdf_version = get_latest_asdf_version()

if latest_asdf_version:
    # Extract major, minor, and patch versions
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", latest_asdf_version)
    if match:
        major, minor, patch = match.groups()

        # Track if updates are needed
        updated_lines = []
        changed = False

        for line in env_lines:
            # Check if line is a variable assignment
            if line.startswith("ASDF_MAJOR_VERSION="):
                current_major = line.split("=")[1].strip().strip('"')
                if current_major != major:
                    line = f'ASDF_MAJOR_VERSION="{major}"\n'
                    changed = True

            elif line.startswith("ASDF_MINOR_VERSION="):
                current_minor = line.split("=")[1].strip().strip('"')
                if current_minor != minor:
                    line = f'ASDF_MINOR_VERSION="{minor}"\n'
                    changed = True

            elif line.startswith("ASDF_PATCH_VERSION="):
                current_patch = line.split("=")[1].strip().strip('"')
                if current_patch != patch:
                    line = f'ASDF_PATCH_VERSION="{patch}"\n'
                    changed = True

            updated_lines.append(line)  # Keep the line as-is unless modified

        # Write back to the file only if changes were made
        if changed:
            with open(env_file, "w") as f:
                f.writelines(updated_lines)

            print(f"✅ Updated .env to ASDF {latest_asdf_version}")
        else:
            print("👍 ASDF version is already up to date.")
    else:
        print(f"⚠️ Unable to parse ASDF version: {latest_asdf_version}")
else:
    print("⚠️ Could not retrieve the latest ASDF version.")
