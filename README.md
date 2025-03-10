# Couchdb Importer

Couchdb Importer is a QGIS plugin that allows users to build Vector layers
from Couchdb data.

Features:
  - Connecting to Couchdb database.
  - Add new features.
  - Update current features.
  - Support Point, LineString and Polygon geometry types.
  - Object properties are imported into attribute table of layers.

Usage:
  - Hit connection button to view all your database
  - Choose database
  - Choose class object
  - Choose attribute of class object
  - Choose one by one object
  - Choose projection type
  - Hit Add layer button to create QGIS layers
  - Hit Update layer button to update the current layers data.

# Installation
## Requirements
- QGIS version 3.4 or later

## Install manually from zip file in QGIS
You can import the zip package directly through Qgis plugin manager.
1. In QGIS, navigate to menu **Plugins** > **Manage and Install Plugins...** > **Install from ZIP**, then select the downloaded zip file.
2. Switch to tab **Installed**, make sure the plugin `Couchdb importer` is enabled.
3. Activate the plugin (with the checkbox).
4. You can see the Couchdb Importer icon at the QGIS action bar, if plugin is activated.

# Development notes

Main python class and method are implemented in `couchdb_importer/couchdb_importer.py`

UI interface is developed using QGIS .ui files :
`couchdb_importer/couchdb_importer_dialog_base.ui` and
`couchdb_importer/couchdb_summary_dialog_base.ui`

Mapping between interface components (like buttons) and implemented python method is done in le method :
`couchdb_importer#run()`

Connection to couchdb service is done with ` couchdb_connector.py` file.

Debug : use of First Aid qgis' plugin. Install it from qgis' base extensions; open it in parallele of your plugin in qgis; place your breakpoints in the first-aid's interface; crush your finger ;)

# Release

In order to release a new version :
- Edit to match the version to release in `couchdb_importer/metadata.txt`
- Run the manual step `release` of the Gitlab pipeline
A new tag should be created, matching the version specified
