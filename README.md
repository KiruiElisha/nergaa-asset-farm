# Nergaa asset farm

Builds Frappe apps' frontends (JS/CSS) on GitHub Actions for [Nergaa Cloud](https://cloud.nergaa.cloud), so its
bench builds extract them instead of compiling on the build server: faster builds, and no build killed for memory.

When Nergaa Cloud's Press sees a new commit of an app, it starts `.github/workflows/prebuild-assets.yml` here
(`repository_dispatch: prebuild-assets`). Each job:

1. checks out Frappe and the app at the exact commits the bench deploys, with the bench's Python and Node versions;
2. builds the app with `bench build --app <app> --production`, as the build server would;
3. packs `apps/<app>/<app>/public` in the format Press's asset store keeps (`tools/pack_assets.py`);
4. asks Press for a one-time signed upload link and stores the file.

Nothing secret is in this repository. Jobs get no storage keys and no upload link in their inputs: they ask Press
for one with the `NERGAA_ASSET_FARM_SECRET` repository secret, and Press signs only for commits it asked for.

The Press side, setup and troubleshooting: `docs/BUILDS.md` in nergaa-cloud.
