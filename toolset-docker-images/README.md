# Toolset Docker Images

This directory contains **example toolset templates** that demonstrate how to build specialized Docker images using the base `asdf-vm` images. Each example is a complete, working toolset that you can use as-is or customize for your needs.

## What's in This Directory?

```
toolset-docker-images/
├── helm/              # Example: Kubernetes package manager + related tools
├── awscli/            # Example: AWS CLI and AWS utilities
├── terraform/         # Example: Infrastructure-as-Code tools
└── README.md          # This file
```

Each toolset directory contains:
- **Dockerfile** - Inherits from a base asdf image and specifies packages to install
- **docker-compose.yaml** - Build configuration with tags, platforms, and versions
- **.env** - Environment variables for versions, registries, and image metadata
- **README.md** - Toolset-specific documentation

## Quick Start: Using an Example Toolset

### Build Locally

Navigate to a toolset directory and build:

```bash
cd toolset-docker-images/helm
docker compose build alpine
```

### Test the Toolset

```bash
docker compose run alpine asdf current
docker compose run alpine helm version
```

### Build for a Specific Base

```bash
cd toolset-docker-images/terraform
docker compose build debian  # Build on Debian instead of Alpine
```

## The Toolset Structure

Each toolset is a directory with four key files:

### 1. Dockerfile

Minimal - just inherits from a base image:

```dockerfile
# build with: --build-arg packages="helm helm:version helm:version:set"
ARG asdf_image="ghcr.io/jrosco/asdf-vm:alpine"
FROM $asdf_image
```

The base image's `ONBUILD` hooks handle the rest automatically.

### 2. docker-compose.yaml

Defines how to build the toolset with tags, platforms, and build arguments:

```yaml
services:
  alpine:
    image: ghcr.io/your-org/helm-toolset:alpine
    build:
      context: .
      dockerfile: Dockerfile
      args:
        asdf_image: "ghcr.io/your-org/asdf-vm:alpine"
        packages: "helm:3.14.0:set helmfile:latest kustomize:latest"
      platforms:
        - "linux/amd64"
      tags:
        - "ghcr.io/your-org/helm-toolset:latest"
        - "ghcr.io/your-org/helm-toolset:alpine-3.20"
```

### 3. .env

Configures versions and registries for the build:

```bash
# Build metadata
BUILD_NUMBER="0"
ASDF_VERSION="v0.13.0"

# Base image registry
ASDF_REGISTRY_BASE="ghcr.io/your-org/asdf-vm"
ASDF_REGISTRY_TOOLSET="$ASDF_REGISTRY_BASE-toolsets"

# Platform versions
ALPINE_VERSION="3.20"
DEBIAN_VERSION="12.7"
```

Update these variables in `.env` before building.

### 4. README.md

Documents the toolset - what tools it includes and how to use it.

## Creating Your Own Toolset

### Step 1: Copy an Existing Example

```bash
cp -r toolset-docker-images/helm/ my-custom-toolset/
cd my-custom-toolset/
```

### Step 2: Update .env

Customize for your organization and tools:

```bash
# Change registry
ASDF_REGISTRY_TOOLSET="ghcr.io/my-org/my-toolsets"

# Define the packages this toolset installs
# (You'll use this in docker-compose.yaml)
MY_TOOL_PACKAGES="terraform:latest:set packer:latest aws-vault:latest"
```

### Step 3: Update docker-compose.yaml

Modify the build args to use your packages:

```yaml
services:
  alpine:
    build:
      args:
        asdf_image: "${ALPINE_IMAGE_REPO_PATH}"
        packages: ${MY_TOOL_PACKAGES}  # Reference from .env
```

### Step 4: Update Dockerfile (Optional)

If you need custom setup beyond just installing packages:

```dockerfile
ARG asdf_image="ghcr.io/my-org/asdf-vm:alpine"
FROM $asdf_image

# Optional: Add custom scripts or configuration
COPY my-script.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/my-script.sh
```

### Step 5: Build and Test

```bash
docker compose build alpine
docker compose run alpine asdf current
docker compose run alpine terraform version
```

## Understanding Package Arguments

The `packages` build argument accepts a space-separated list in this format:

```
package_name:version:modifier
```

### Modifiers:

| Format | Example | Behavior |
| --- | --- | --- |
| (no modifier) | `helm` | Add plugin only, don't install |
| `version` | `helm:3.14.0` | Install specific version |
| `:latest` | `helm:latest` | Install latest version |
| `:all` | `helm:all` | Install all versions (rarely used) |
| `:set` | `helm:3.14.0:set` | Install AND set as default |

### Example Packages String:

```bash
packages="terraform:1.8.0:set helm:3.14.0:set aws-vault:latest kubectl:1.28.0"
```

This installs:
- Terraform 1.8.0 as default
- Helm 3.14.0 as default
- Latest AWS Vault
- Kubectl 1.28.0

## Multi-Platform Builds

Build for multiple architectures in docker-compose.yaml:

```yaml
services:
  alpine:
    build:
      platforms:
        - "linux/amd64"
        - "linux/arm64"
        - "linux/arm/v7"
```

Then build with buildx:

```bash
docker buildx build --push --platform linux/amd64,linux/arm64 .
```

## Publishing Your Toolsets

### Build and Tag

```bash
docker compose build alpine
docker tag ghcr.io/my-org/my-toolset:latest ghcr.io/my-org/my-toolset:v1.0.0
```

### Push to Registry

```bash
docker push ghcr.io/my-org/my-toolset:latest
docker push ghcr.io/my-org/my-toolset:v1.0.0
```

### Share with Your Team

Users can now pull your toolset:

```bash
docker pull ghcr.io/my-org/my-toolset:latest
docker run -it ghcr.io/my-org/my-toolset:latest bash
```

## Environment Variables Reference

Common variables used in `.env` and `docker-compose.yaml`:

| Variable | Purpose | Example |
| --- | --- | --- |
| `BUILD_NUMBER` | Build iteration counter | `0`, `1`, `2` |
| `ASDF_VERSION` | asdf version to use | `v0.13.0` |
| `ASDF_REGISTRY_TOOLSET` | Docker registry for your toolsets | `ghcr.io/my-org/toolsets` |
| `ALPINE_VERSION` | Alpine base image version | `3.20` |
| `DEBIAN_VERSION` | Debian base image version | `12.7` |
| `{TOOL}_PACKAGES` | Space-separated packages for this toolset | `helm:latest kubectl:latest` |

## Tips & Best Practices

1. **Keep Toolsets Focused** - Each toolset should solve one problem (Kubernetes tools, AWS tools, Python dev tools, etc.)
2. **Pin Versions** - Use specific versions (`:3.14.0`) for production; use `:latest` for development
3. **Use .tool-versions for Locked Builds** - For critical deployments, use a `.tool-versions` file
4. **Test Before Publishing** - Always test with `docker-compose run` before pushing to registry
5. **Document Tools** - Update each toolset's README with what's included and example usage
6. **Version Your Toolsets** - Use semantic versioning (`v1.0.0`) for your toolset releases

## Examples in This Repository

### Helm Toolset ([helm/](./helm))
- **Base Image:** Alpine
- **Tools:** Helm, Helmfile, Kustomize
- **Use Case:** Kubernetes deployment and package management

### AWS Toolset ([awscli/](./awscli))
- **Base Image:** Alpine
- **Tools:** AWS CLI, AWS Vault
- **Use Case:** AWS infrastructure and secrets management

### Terraform Toolset ([terraform/](./terraform))
- **Base Image:** Alpine
- **Tools:** Terraform, Packer
- **Use Case:** Infrastructure-as-Code provisioning

## Next Steps

1. **Choose an example** that's closest to your needs
2. **Copy it** to create your own toolset
3. **Update .env** with your registry and tool versions
4. **Test locally** with `docker-compose build` and `docker-compose run`
5. **Customize** the Dockerfile if you need special setup
6. **Publish** to your registry
7. **Share** with your team

See the main [README](../README.md) for more information about base images and the asdf version manager.
