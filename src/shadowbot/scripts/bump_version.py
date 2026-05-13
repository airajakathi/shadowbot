#!/usr/bin/env python3
"""
Version bump script for ShadowBot package.

This script updates the version number in all required locations:
- shadowbot/version.py (single source of truth for Python package)
- shadowbot/deploy.py (Dockerfile template)
- ../../docker/Dockerfile, Dockerfile.chat, Dockerfile.dev, Dockerfile.ui
- shadowbot.rb (Homebrew formula)

Usage:
    python src/shadowbot/scripts/bump_version.py 2.2.96
    
Or with optional shadowbotagents version:
    python src/shadowbot/scripts/bump_version.py 2.2.96 --agents 0.0.167
"""

import re
import sys
import argparse
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory (shadowbot-package)."""
    # scripts/ -> src/shadowbot/ -> src/ -> shadowbot-package/
    return Path(__file__).parent.parent.parent.parent


def update_file(filepath: Path, patterns: list[tuple[str, str]]) -> bool:
    """Update a file with the given regex patterns and replacements."""
    if not filepath.exists():
        print(f"  ⚠️  File not found: {filepath}")
        return False
    
    content = filepath.read_text()
    original = content
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        filepath.write_text(content)
        print(f"  ✅ Updated: {filepath.relative_to(get_project_root())}")
        return True
    else:
        print(f"  ⏭️  No changes: {filepath.relative_to(get_project_root())}")
        return False


def bump_version(new_version: str, agents_version: str | None = None):
    """Bump version in all required files."""
    root = get_project_root()
    
    print(f"\n🚀 Bumping ShadowBot version to {new_version}\n")
    
    shadowbot_dir = root / "src/shadowbot"
    
    # 1. Update version.py (single source of truth)
    print("📦 Python Package:")
    update_file(
        shadowbot_dir / "shadowbot/version.py",
        [(r'__version__ = "[^"]+"', f'__version__ = "{new_version}"')]
    )
    
    # 2. Update deploy.py (Dockerfile template)
    print("\n🐳 Deploy Script:")
    update_file(
        shadowbot_dir / "shadowbot/deploy.py",
        [(r'shadowbot==[0-9.]+', f'shadowbot=={new_version}')]
    )
    
    # 3. Update Dockerfiles
    print("\n🐳 Dockerfiles:")
    dockerfiles = [
        "docker/Dockerfile",
        "docker/Dockerfile.chat",
        "docker/Dockerfile.dev",
        "docker/Dockerfile.ui",
    ]
    for dockerfile in dockerfiles:
        update_file(
            root / dockerfile,
            [(r'"shadowbot>=[0-9.]+"', f'"shadowbot>={new_version}"')]
        )
    
    # 4. Update Homebrew formula
    print("\n🍺 Homebrew Formula:")
    update_file(
        shadowbot_dir / "shadowbot.rb",
        [(r'v[0-9]+\.[0-9]+\.[0-9]+', f'v{new_version}')]
    )
    
    # 5. Update shadowbotagents dependency if specified
    if agents_version:
        print(f"\n📦 Updating shadowbotagents dependency to {agents_version}:")
        update_file(
            shadowbot_dir / "pyproject.toml",
            [(r'shadowbotagents>=[0-9.]+', f'shadowbotagents>={agents_version}')]
        )
    
    print("\n✨ Version bump complete!")
    print("\nNext steps:")
    print("  1. Run: cd src/shadowbot && uv lock")
    print("  2. Run: cd src/shadowbot && uv build")
    print(f"  3. Commit changes: git add -A && git commit -m 'Bump version to {new_version}'")
    print(f"  4. Tag release: git tag v{new_version}")
    print("  5. Publish: cd src/shadowbot && uv publish")


def main():
    parser = argparse.ArgumentParser(
        description="Bump ShadowBot version in all required files"
    )
    parser.add_argument(
        "version",
        help="New version number (e.g., 2.2.96)"
    )
    parser.add_argument(
        "--agents", "-a",
        help="Optional: Update shadowbotagents dependency version (e.g., 0.0.167)",
        default=None
    )
    
    args = parser.parse_args()
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', args.version):
        print(f"❌ Invalid version format: {args.version}")
        print("   Expected format: X.Y.Z (e.g., 2.2.96)")
        sys.exit(1)
    
    if args.agents and not re.match(r'^\d+\.\d+\.\d+$', args.agents):
        print(f"❌ Invalid agents version format: {args.agents}")
        print("   Expected format: X.Y.Z (e.g., 0.0.167)")
        sys.exit(1)
    
    bump_version(args.version, args.agents)


if __name__ == "__main__":
    main()
