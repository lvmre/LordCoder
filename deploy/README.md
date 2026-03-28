# Deploy Scaffolding

These files are templates for later packaging and service-management phases.

Current phase:

- validates cross-platform developer installs
- keeps `pip install .` as the release target
- does not yet ship native installers or service automation

Included scaffolding:

- `systemd` service template
- `launchd` plist template
- Windows service-install notes/template

Deferred:

- MSI / winget
- signed DMG / notarization
- deb/rpm/AppImage
- multi-arch OCI publishing
