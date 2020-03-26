# Couchdb Importer

Couchdb Importer is a QGIS plugin that allows users to build layers from Couchdb data.

Make sure the couchdb python extension are installed! Otherwise the plugin
will give an error message about a missing "couchdb" module.
Follow the section 'Install QGIS python extension' for more information.

Features:
  - Connecting to Couchdb database.
  - Add new features.
  - Update current features.
  - Support Point, LineString and Polygone geometry types.
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
-QGIS 3.x
-couchdb >= 1.2 (on windows, see 'Install QGIS python extension' section for help)

### Install manually from zip file in QGIS
1. In QGIS, navigate to menu **Plugins** > **Manage and Install Plugins...** > **Install from ZIP**, then select the downloaded zip file.
2. Switch to tab **Installed**, make sure the plugin `Couchdb importer` is enabled.
3. Activate the plugin (with the checkbox).  
4. You can see the Couchdb Importer icon at the QGIS action bar, if plugin is activated.

### Download from plugin repository
1. Unpack the dowloaded file 'Couchdb_importer.zip'.  
2. Place the extracted files/folder in QGIS plugins directory.  
3. Activate the plugin (with the checkbox).  
4. You can see the Couchdb Importer icon at the QGIS action bar, if plugin is activated.

# Install QGIS python extension
## Windows
1. Open OSGeo4W shell (packed with QGIS in the start menu) as Administrator (Right-click on, select 'Run as Administrator')
2. Run command `py3_env`
3. Run command `python -m pip install couchdb`
