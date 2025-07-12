#!/bin/bash
set -e

INCREMENT_TYPE=${1:-patch}
git fetch --tags

# Get latest version tag (or default to v0.0.0 if no tags)
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
VERSION=${LATEST_TAG#v}

IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

case "$INCREMENT_TYPE" in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
  *)
    echo "❌ Invalid version bump type: $INCREMENT_TYPE"
    exit 1
    ;;
esac

NEW_VERSION="v${MAJOR}.${MINOR}.${PATCH}"
RELEASE_BRANCH="release/$NEW_VERSION"

# Configure Git (already done in workflow, but safe here too)
git config user.name "github-actions"
git config user.email "github-actions@github.com"

# Create tag and push
git tag "$NEW_VERSION"
git push origin "$NEW_VERSION"

# Create release branch and push
git checkout -b "$RELEASE_BRANCH"
git push origin "$RELEASE_BRANCH"

# Export version for workflow
echo "NEW_VERSION=$NEW_VERSION" >> "$GITHUB_ENV"
echo "new_version=$NEW_VERSION" >> "$GITHUB_OUTPUT"
echo "$NEW_VERSION" > VERSION

echo "✅ Created tag $NEW_VERSION and branch $RELEASE_BRANCH"
