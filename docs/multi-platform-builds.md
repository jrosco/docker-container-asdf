# Multi-Platform Docker Builds

This document describes how to build and push Docker images for multiple platforms (architectures) in the `asdf-vm` repository.

## Overview

The repository is configured to build Docker images for the following platforms:

- **linux/amd64**: x86_64 (standard Intel/AMD processors)
- **linux/arm64**: ARM 64-bit (Apple Silicon, AWS Graviton, newer ARM servers)
- **linux/arm/v7**: 32-bit ARM (Raspberry Pi, older ARM devices)

RedHat images currently support:
- **linux/amd64**: x86_64
- **linux/arm64**: ARM 64-bit

## Prerequisites

### For Local Development

To build multi-platform images locally, you need:

1. **Docker Desktop** (v20.10+) with BuildKit enabled
2. **QEMU** (for ARM emulation) - Usually included with Docker Desktop
3. Docker Buildx (included with Docker Desktop 20.10+)

Verify your setup:

```bash
docker buildx version
docker buildx ls
```

### For CI/CD (GitHub Actions)

The GitHub workflows automatically handle multi-platform builds using:
- `docker/setup-qemu-action@v3`: Provides QEMU for cross-platform emulation
- `docker/setup-buildx-action@v3`: Sets up Docker Buildx
- `docker/build-push-action@v5`: Builds and pushes multi-platform images

## Building Locally

### Option 1: Using Docker Buildx (Recommended)

Build for multiple platforms:

```bash
# Build Alpine image for all platforms
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --file base-images/Dockerfile.alpine \
  --build-arg asdf_version=0.14.0 \
  --build-arg alpine_image=alpine:3.19 \
  --build-arg go_build_version=golang:1.21-alpine3.19 \
  -t myregistry/asdf:alpine-0.14.0 \
  .
```

Build for a specific platform:

```bash
# Build for ARM64 only
docker buildx build \
  --platform linux/arm64 \
  --file base-images/Dockerfile.alpine \
  --build-arg asdf_version=0.14.0 \
  --build-arg alpine_image=alpine:3.19 \
  --build-arg go_build_version=golang:1.21-alpine3.19 \
  --load \
  -t myregistry/asdf:alpine-arm64 \
  .
```

**Note**: The `--load` flag only works with single platform builds.

### Option 2: Using Docker Compose with BuildKit

Enable BuildKit:

```bash
export DOCKER_BUILDKIT=1
```

Then build using docker-compose:

```bash
docker compose build alpine
```

This will respect the `platforms` section in `docker-compose.yaml`.

### Option 3: Using the Makefile

```bash
# Build and load for current platform
make build

# Push to registry (requires multi-platform builder setup)
make push
```

## Pushing to Registry

### Pushing Multi-Platform Images

To push multi-platform images to a registry, use buildx:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --file base-images/Dockerfile.alpine \
  --build-arg asdf_version=0.14.0 \
  --build-arg alpine_image=alpine:3.19 \
  --build-arg go_build_version=golang:1.21-alpine3.19 \
  --push \
  -t ghcr.io/jrosco/asdf-vm:alpine-0.14.0 \
  .
```

**Note**: The `--push` flag is required when building for multiple platforms (since Docker cannot load multiple architectures locally).

### Registry Authentication

Ensure you're logged into the registry:

```bash
# GitHub Container Registry
docker login ghcr.io

# Docker Hub
docker login docker.io
```

## Supported Build Arguments

All Dockerfiles support the following build arguments:

### Alpine (`base-images/Dockerfile.alpine`)

- `asdf_version`: Version of ASDF to install (e.g., `0.14.0`)
- `alpine_image`: Base Alpine image (e.g., `alpine:3.19`)
- `go_build_version`: Go builder image (e.g., `golang:1.21-alpine3.19`)

### Debian (`base-images/Dockerfile.debian`)

- `asdf_version`: Version of ASDF to install
- `debian_image`: Base Debian image (e.g., `debian:12`)
- `go_build_version`: Go builder image (e.g., `golang:1.21-bookworm`)

### RedHat (`base-images/Dockerfile.redhat`)

- `asdf_version`: Version of ASDF to install
- `redhat_image`: Base RedHat image (e.g., `registry.access.redhat.com/hi/go:1.21`)
- `go_build_version`: Go builder image
- `redhat_build_tools`: RedHat build tools image

## Environment Variables

Configuration is managed via `config/environment`:

```bash
ASDF_VERSION=0.14.0
ALPINE_VERSION=3.19
ALPINE_VERSION_SHORTHAND=19
DEBIAN_VERSION=12
DEBIAN_VERSION_CODENAME=bookworm
GOLANG_VERSION=1.21
ASDF_REGISTRY_BASE=ghcr.io/jrosco/asdf-vm
```

Load these into the environment:

```bash
source ./config/environment
export BUILD_NUMBER=1
```

## CI/CD Pipeline

### GitHub Actions Workflows

#### docker-push.yaml (Production)

Triggered on push to `main` (merge with semantic versioning):

1. Creates a semantic version tag
2. Builds base images for multiple platforms:
   - Alpine: `linux/amd64,linux/arm64,linux/arm/v7`
   - Debian: `linux/amd64,linux/arm64,linux/arm/v7`
   - RedHat: `linux/amd64,linux/arm64`
3. Pushes to GHCR and Docker Hub with proper tags

#### docker-build.yaml (Pull Request Testing)

Triggered on pull requests:

1. Tests base image builds
2. Builds and pushes dev images for multiple platforms
3. Checks semantic version bump

### Monitoring Builds

Check workflow results:

```bash
# View recent builds
gh run list --workflow docker-push.yaml

# View specific run
gh run view <run-id>

# View logs
gh run view <run-id> --log
```

## Troubleshooting

### Issue: `docker buildx build` not found

**Solution**: Ensure Docker Desktop 20.10+ is installed. Upgrade if needed.

### Issue: QEMU not available

**Solution**: Reinstall Docker Desktop or manually install QEMU:

```bash
# macOS with Homebrew
brew install qemu

# Linux (Ubuntu/Debian)
sudo apt-get install qemu-user-static

# Linux (RHEL/Fedora)
sudo dnf install qemu-user-static
```

### Issue: Build hangs when emulating ARM

**Solution**: QEMU emulation can be slow. This is normal for ARM builds on x86_64. Consider:

1. Building on an ARM machine natively (faster)
2. Using GitHub Actions (typically faster)
3. Increasing timeout values in builds

### Issue: Registry push fails

**Solution**: Ensure you're authenticated:

```bash
docker logout
docker login <registry>
```

### Issue: Platform mismatch in manifest

**Solution**: Ensure all platforms build successfully before pushing. Check logs:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -f base-images/Dockerfile.alpine \
  --push \
  -t myimage:tag \
  .
```

## Performance Optimization

### Caching

The workflows use GitHub Actions Cache with buildx for faster builds:

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

To enable caching locally:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-to type=local,dest=/tmp/buildx-cache \
  --cache-from type=local,src=/tmp/buildx-cache \
  -t myimage:tag \
  .
```

### Parallel Building

The CI/CD workflows use parallel job execution to build multiple services concurrently, reducing total CI/CD time.

## Best Practices

1. **Test on all platforms**: Use CI/CD to validate multi-platform builds before production
2. **Use specific base image versions**: Avoid `latest` tags in production builds
3. **Leverage caching**: Store cache between builds to speed up development
4. **Document platform-specific issues**: Note any platform-specific workarounds
5. **Monitor build times**: Track and optimize slow builds
6. **Use native builds when possible**: Building on the target architecture is faster

## Reference

- [Docker Buildx Documentation](https://docs.docker.com/build/architecture/)
- [Docker Build Documentation](https://docs.docker.com/build/)
- [QEMU Documentation](https://www.qemu.org/)
- [Open Container Initiative Image Spec](https://github.com/opencontainers/image-spec)
