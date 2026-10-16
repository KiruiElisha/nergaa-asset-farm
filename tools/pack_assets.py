#!/usr/bin/env python3
"""Pack an app's built assets the way Press's build server stores them in the asset store.

    pack_assets.py <bench> <app> <out.tar.gz>

Same layout as the agent's repack_public_folder (frappe/agent, agent/builder.py): the app's
apps/<app>/<app>/public folder, renamed to <app>/, without the node_modules link bench build adds.
A build then extracts it instead of running the app's frontend build (get_cached_app.py).
"""
from __future__ import annotations

import os
import sys
import tarfile


def pack(bench: str, app: str, out: str) -> int:
    public = os.path.join(bench, "apps", app, app, "public")
    if not os.path.isdir(public):
        raise SystemExit(f"{public} not found: was the app built?")
    node_modules = f"{app}/node_modules"
    count = 0

    def keep(info: tarfile.TarInfo) -> tarfile.TarInfo | None:
        nonlocal count
        if info.name == node_modules or info.name.startswith(node_modules + "/"):
            return None
        count += 1
        return info

    with tarfile.open(out, "w:gz") as tar:
        tar.add(public, arcname=app, recursive=True, filter=keep)
    return count


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    n = pack(*sys.argv[1:])
    print(f"packed {n} entries of {sys.argv[2]} into {sys.argv[3]} ({os.path.getsize(sys.argv[3]) // 1024} KB)")
