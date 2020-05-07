# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CouchdbImporter
                                 A QGIS plugin
 This plugin allows importing vector data from the couchdb database.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-01-30
        git sha              : $Format:%H$
        copyright            : (C) 2020 by MaximeGavens/Geomatys
        email                : contact@geomatys.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.core import QgsGeometry, QgsProject, QgsPoint
from qgis.PyQt.QtCore import Qt


class Utils:

    @staticmethod
    def build_list_from_selection(obj):
        result = []
        for item in obj:
            if obj[item]:
                result.append(item)
        return result

    @staticmethod
    def parse_url(url):
        split_url = url.split("://")
        if len(split_url) == 2:
            http = split_url[0]
            addr = split_url[1]
            if http == "http" or http == "https":
                return [http, addr]
            else:
                return None
        else:
            return None

    @staticmethod
    def collect_ids_from_layers_filtered_by_positionable_class(positionable):
        result = []
        layers = QgsProject.instance().mapLayers()
        for l in layers:
            if layers[l].name() in positionable:
                ids = Utils.collect_ids_from_layer(layers[l])
                result.extend(ids)
        return result

    @staticmethod
    def debut_fin_to_wkt_linestring(wktdebut, wktfin):
        coordDebut = wktdebut.split('(')[1]
        coordFin = wktfin.split('(')[1]
        coordDebut = coordDebut.split(')')[0]
        coordFin = coordFin.split(')')[0]

        return "LINESTRING (" + coordDebut + ", " + coordFin + ")"

    @staticmethod
    def build_row_name_positionable(positionable):
        className = positionable["@class"].split("fr.sirs.core.model.")[1]
        label = Utils.get_label(positionable)
        id = positionable["_id"]
        name = className + " - " + label + " - " + id
        return name

    @staticmethod
    def get_label(positionable):
        if 'designation' in positionable:
            return positionable['designation']
        elif 'libelle' in positionable:
            return positionable['libelle']
        elif 'login' in positionable:
            return positionable['login']
        elif '_id' in positionable:
            return positionable['_id']
        else:
            return 'no data'

    @staticmethod
    def get_label_reference(positionable):
        if 'libelle' in positionable:
            return positionable['libelle']
        elif 'designation' in positionable:
            return positionable['designation']
        elif '_id' in positionable:
            return positionable['_id']
        else:
            return 'no data'

    @staticmethod
    def collect_ids_from_layers():
        result = []
        layers = QgsProject.instance().mapLayers()
        for l in layers:
            ids = Utils.collect_ids_from_layer(layers[l])
            result.extend(ids)
        return result

    @staticmethod
    def collect_ids_from_layer(layer):
        if layer.type() != 0 or layer.fields().indexFromName("_id") == -1:
            return []
        features = layer.getFeatures()
        return [f["_id"] for f in features]

    @staticmethod
    def build_geometry(wkt, param):
        geom = QgsGeometry.fromWkt(wkt)
        multi_geom = QgsGeometry()
        temp_geom = []
        if geom.type() == 0:
            return geom
        elif geom.type() == 1:
            if geom.isMultipart():
                multi_geom = geom.asMultiPolyline()
                for i in multi_geom:
                    temp_geom.extend(i)
            else:
                temp_geom = geom.asPolyline()
            if Utils.is_point(temp_geom, param):
                # te be more rigorous, I should take the barycenter from the list
                return QgsPoint(temp_geom[0])
            else:
                return geom
        elif geom.type() == 2:
            # to find the maximum length inside geometry, I apply the convexhull to recover only pertinent point,
            # before apply empirical research
            hull = geom.convexHull()
            if hull.isMultipart():
                multi_geom = hull.asMultiPolygon()
                for i in multi_geom:
                    for j in i:
                        temp_geom.extend(j)
            else:
                multi_geom = hull.asPolygon()
                for i in multi_geom:
                    temp_geom.extend(i)
            if Utils.is_point(temp_geom, param):
                # to be more rigorous, I should take the barycenter from the list
                return QgsPoint(temp_geom[0])
            else:
                return geom
        else:
            return None

    @staticmethod
    def is_point(listPoint, param):
        for p1 in listPoint:
            for p2 in listPoint:
                if p1.distance(p2) > param:
                    return False
        return True

    @staticmethod
    def filter_layers_by_name_and_geometry_type(name, type):
        layers = QgsProject.instance().mapLayers()
        for l in layers:
            if layers[l].name() == name and layers[l].wkbType() == type:
                return layers[l]
        return None

    @staticmethod
    def is_str_start_by_underscore(var):
        if type(var) is str:
            return var.find('_') == 0
        return False

    @staticmethod
    def build_query(className, attributes=None, ids=None):
        if ids is not None and type(ids) == list:
            orList = []
            for id in ids:
                orList.append({
                    "@class": "fr.sirs.core.model." + className,
                    "_id": id
                })
            mango = {
                "selector": {
                    "$or": orList
                },
                "limit": 50000
            }
            if attributes is not None:
                mango["fields"] = attributes
        else:
            mango = {
                "selector": {
                    "@class": "fr.sirs.core.model." + className
                },
                "limit": 50000
            }
            if attributes is not None:
                mango["fields"] = attributes
        return mango

    @staticmethod
    def build_query_only_id(ids):
        orList = []
        for id in ids:
            orList.append({
                "_id": id
            })
        mango = {
            "selector": {
                "$or": orList
            },
            "limit": 50000
        }
        return mango

    @staticmethod
    def build_query_one_id(id):
        mango = {
            "selector": {
                "_id": id
            }
        }
        return mango

    @staticmethod
    def is_all_selected_in_model(model):
        for i in range(model.rowCount()):
            item = model.itemFromIndex(model.index(i, 0))
            if item.checkState() == Qt.Unchecked:
                return False
        return True
