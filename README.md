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
- couchdb >= 1.2 ; On Linux and Mac, it will be automatically installed,
on windows, you have to pass by 'Install missing module' section.

### Install manually from zip file in QGIS
You can import the zip package directly through Qgis plugin manager.
1. In QGIS, navigate to menu **Plugins** > **Manage and Install Plugins...** > **Install from ZIP**, then select the downloaded zip file.
2. Switch to tab **Installed**, make sure the plugin `Couchdb importer` is enabled.
3. Activate the plugin (with the checkbox).  
4. You can see the Couchdb Importer icon at the QGIS action bar, if plugin is activated.

## Install missing module
###### Windows only
1. Open 'OSGeo4W shell' (packed with QGIS in the start menu) as Administrator (Right-click on, select 'Run as Administrator')
2. Run command `py3_env`
3. Run command `python -m pip install couchdb`
