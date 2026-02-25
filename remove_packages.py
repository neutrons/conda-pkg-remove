#!/usr/bin/env python3
"""Remove old labeled packages from anaconda.org, keeping the N most recent versions."""

import os
import sys

from binstar_client.utils import get_server_api


def main():
    token = os.environ["ANACONDA_TOKEN"]
    org = os.environ["ORGANIZATION"]
    pkg = os.environ["PACKAGE_NAME"]
    label = os.environ["LABEL"]
    keep = int(os.environ.get("KEEP", "5"))
    dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"

    if dry_run:
        print("Dry run mode - no files will be deleted")

    api = get_server_api(token=token)

    # Get all files for the package
    try:
        files = api.package_files(org, pkg)
    except Exception as e:
        print(f"Error fetching package files for {org}/{pkg}: {e}", file=sys.stderr)
        sys.exit(1)

    # Filter by label
    labeled_files = [f for f in files if label in f.get("labels", [])]
    print(f"Found {len(labeled_files)} file(s) with label '{label}'")

    if not labeled_files:
        print("Nothing to do.")
        return

    # Sort by upload date (most recent first)
    labeled_files.sort(key=lambda x: x.get("upload_time", ""), reverse=True)

    # Get unique versions maintaining order (most recent first)
    seen_versions = []
    for f in labeled_files:
        v = f["version"]
        if v not in seen_versions:
            seen_versions.append(v)

    print(f"Found {len(seen_versions)} unique version(s) with label '{label}'")
    print(f"Keeping the {keep} most recent version(s)")

    versions_to_keep = set(seen_versions[:keep])
    print(f"Versions to keep: {sorted(versions_to_keep)}")

    # Files to delete (those whose versions are not in the keep set)
    to_delete = [f for f in labeled_files if f["version"] not in versions_to_keep]

    if not to_delete:
        print("Nothing to delete.")
        return

    print(f"\nDeleting {len(to_delete)} file(s):")
    for f in to_delete:
        basename = f["basename"]
        version = f["version"]
        print(f"  {org}/{pkg}/{version}/{basename}")
        if not dry_run:
            api.remove_dist(org, pkg, version, basename)

    if dry_run:
        print("\nDry run complete - no files were deleted")
    else:
        print(f"\nDeleted {len(to_delete)} file(s)")


if __name__ == "__main__":
    main()
