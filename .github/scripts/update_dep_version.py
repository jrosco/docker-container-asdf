import requests
import re
import os
import sys

if len(sys.argv) == 1:
    print("provide Product name")
    exit(1)
else:
    product = sys.argv[1]
    # Gets the first entry, increase to go back to eariler versions
    go_back = sys.argv[2] if len(sys.argv) > 2 else 0
    url = f"https://endoflife.date/api/{product.lower()}.json"

# Read the .env file while preserving comments and structure
env_file = "config/environment"
env_lines = []

if os.path.exists(env_file):
    with open(env_file, "r") as f:
        # Keep all lines, including comments and formatting
        env_lines = f.readlines()
else:
    print(f"⚠️ Environment file {env_file} does not exist.")
    env_lines = []


# Fetch the latest version
def get_latest_version():
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        releases = response.json()
        latest_release = releases[go_back]["latest"]
        return latest_release
    except Exception as e:
        print(f"Error fetching version: {e}")
        return None


# Get latest version
latest_version = get_latest_version()

if latest_version:
    # Extract major, minor, and patch versions
    full_match = re.match(r"(\d+)\.(\d+)\.(\d+)", latest_version)
    floating_match = re.match(r"(\d+)\.(\d+)", latest_version)

    if full_match:
        major, minor, patch = full_match.groups()
    if floating_match:
        major, minor = floating_match.groups()

    if full_match or floating_match:
        # Track if updates are needed
        updated_lines = []
        changed = False

        for line in env_lines:
            # Check if line is a variable assignment
            if line.startswith(f"{product.upper()}_MAJOR_VERSION="):
                current_major = line.split("=")[1].strip().strip('"')
                if current_major != major:
                    line = f'{product.upper()}_MAJOR_VERSION="{major}"\n'
                    changed = True

            elif line.startswith(f"{product.upper()}_MINOR_VERSION="):
                current_minor = line.split("=")[1].strip().strip('"')
                if current_minor != minor:
                    line = f'{product.upper()}_MINOR_VERSION="{minor}"\n'
                    changed = True

            elif line.startswith(f"{product.upper()}_PATCH_VERSION="):
                current_patch = line.split("=")[1].strip().strip('"')
                if current_patch != patch:
                    line = f'{product.upper()}_PATCH_VERSION="{patch}"\n'
                    changed = True

            updated_lines.append(line)  # Keep the line as-is unless modified

        # Write back to the file only if changes were made
        if changed:
            with open(env_file, "w") as f:
                f.writelines(updated_lines)
            print(f"✅ Updated .env to {product.capitalize()} {latest_version}")
        else:
            print(f"👍 {product.capitalize()} versions already up to date.")
    else:
        print(f"⚠️ Unable to parse {
              product.capitalize()} version: {latest_version}")
else:
    print(f"⚠️ Could not retrieve the latest {product.capitalize()} version.")
