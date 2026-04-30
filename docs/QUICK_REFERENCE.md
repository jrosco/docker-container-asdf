# Multi-Platform Docker Build Quick Reference

## Quick Start

### 1. Build for Current Platform (Default)
```bash
make build
```

### 2. Setup Multi-Platform Support
```bash
make setup-buildx
```

### 3. Build for All Platforms Locally
```bash
source ./config/environment
make build-multiplatform
```

### 4. Push to Registry
```bash
source ./config/environment
make push-multiplatform
```

## Common Tasks

### Build Alpine for ARM64 Only
```bash
docker buildx build \
  --platform linux/arm64 \
  --file base-images/Dockerfile.alpine \
  --build-arg asdf_version=0.14.0 \
  --build-arg alpine_image=alpine:3.19 \
  --build-arg go_build_version=golang:1.21-alpine3.19 \
  -t ghcr.io/jrosco/asdf-vm:alpine-arm64 \
  --load \
  .
```

### Push Alpine for Multiple Platforms
```bash
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --file base-images/Dockerfile.alpine \
  --build-arg asdf_version=0.14.0 \
  --build-arg alpine_image=alpine:3.19 \
  --build-arg go_build_version=golang:1.21-alpine3.19 \
  -t ghcr.io/jrosco/asdf-vm:alpine \
  --push \
  .
```

### Check Available Builders
```bash
docker buildx ls
```

### Switch to Multi-Platform Builder
```bash
docker buildx use asdf-builder
```

### Inspect Build Output
```bash
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --file base-images/Dockerfile.alpine \
  --build-arg asdf_version=0.14.0 \
  --build-arg alpine_image=alpine:3.19 \
  --build-arg go_build_version=golang:1.21-alpine3.19 \
  .
```

## Supported Platforms

| Image | Platforms |
|-------|-----------|
| Alpine | linux/amd64, linux/arm64, linux/arm/v7 |
| Debian | linux/amd64, linux/arm64, linux/arm/v7 |
| RedHat | linux/amd64, linux/arm64 |

## Environment Variables

All build commands use environment variables from `config/environment`:

```bash
source ./config/environment
echo "Building ASDF ${ASDF_VERSION} on Alpine ${ALPINE_VERSION}"
```
