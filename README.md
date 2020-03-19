# Setup
## Install 'Plugin builder 3' plugin
Open QGIS.
Click on 'Plugins' tab then 'Manage and Install Plugins...'.
Search 'Plugin builder 3' in search bar then install it.
Close QGIS.

## Add the project to QGIS sources
`cp -r ./couchdb_importer/ /PathToQgisDirectory/QGIS/QGIS3/profiles/default/python/plugins/`

## Install the python module 'couchdb'
`pip install couchdb -t /PathToPythonLibrary/` : Pay attention to the python library used by your QGIS.

## Install 'couchdb_importer' plugin
Open QGIS.
Click on 'Plugins' tab then 'Manage and Install Plugins...'.
Search 'couchdb_importer' in search bar then install it.
