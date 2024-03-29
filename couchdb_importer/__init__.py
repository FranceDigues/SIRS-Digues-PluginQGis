# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CouchdbImporter
                                 A QGIS plugin
 This plugin allows importing vector data from the couchdb database.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-01-30
        copyright            : (C) 2020 by MaximeGavens/Geomatys
        email                : contact@geomatys.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CouchdbImporter class from file CouchdbImporter.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .couchdb_importer import CouchdbImporter
    return CouchdbImporter(iface)
