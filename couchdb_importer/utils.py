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
from functools import lru_cache
from time import strptime
from qgis.core import QgsGeometry, QgsProject, QgsPoint
from qgis.PyQt.QtCore import Qt
from couchdb_importer.message_utils import simple_message


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
    def get_label(positionable):
        if 'libelle' in positionable:
            return positionable['libelle']
        return ''

    @staticmethod
    def get_designation(positionable):
        if 'designation' in positionable:
            return positionable['designation']
        return ''

    @staticmethod
    def get_label_reference(positionable):
        if 'libelle' in positionable:
            return positionable['libelle']
        # FDSIRTMA23-33 : display name for authors
        elif 'login' in positionable:
            return positionable['login']
        elif 'nom' in positionable:# Anomalie#8060
            return positionable['nom']
        elif 'designation' in positionable:
            return positionable['designation']
        elif '_id' in positionable:
            return positionable['_id']
        else:
            return "Aucune donnée"

    @staticmethod
    def get_label_and_designation_reference(positionable):
        if 'libelle' in positionable and 'designation' in positionable:
            return positionable['libelle'] + ' ||| ' + positionable['designation']
        elif '_id' in positionable:
            if 'libelle' in positionable and 'designation' not in positionable:
                return positionable['libelle'] + ' ||| ' + positionable['_id']
            elif 'libelle' not in positionable and 'designation' in positionable:
                return positionable['_id'] + ' ||| ' + positionable['designation']
            else:
                return positionable['_id'] + ' ||| ' + positionable['_id']
        else:
            if 'libelle' in positionable and 'designation' not in positionable:
                return positionable['libelle'] + ' ||| no data'
            elif 'libelle' not in positionable and 'designation' in positionable:
                return 'no data ||| ' + positionable['designation']
            else:
                return 'no data ||| no data'

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
        if layer.type() != 0 or layer.fields().indexFromName("_id (ne pas modifier/supprimer)") == -1:
            return []
        features = layer.getFeatures()
        return [f["_id (ne pas modifier/supprimer)"] for f in features]

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
    def filter_layers_by_name_and_geometry_type(name, geom_type):
        filtered = filter(lambda layer: Utils.match_type(layer, geom_type), QgsProject.instance().mapLayersByName(name))
        return next(filtered, None)

    @staticmethod
    def match_type(layer, geom_type):
        return layer is not None and layer.wkbType() == geom_type

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
    def build_query_one_id_with_class(className, id):
        mango = {
            "selector": {
                "@class": "fr.sirs.core.model." + className,
                "_id": id
            }
        }
        return mango

    @staticmethod
    def create_specific_view():
        doc = {
            "_id": "_design/SpecQgis",
            "views": {
                "byClass": {
                    "map": "function(doc) {if(doc['@class']) {emit(doc['@class'], doc)}}"
                },
                "byId": {
                    "map": "function(doc) {if(doc['_id']) {emit(doc['_id'], doc)}}"
                },
                "byClassAndId": {
                    "map": "function(doc) {if(doc['@class'] && doc['_id']) {emit([doc['@class'], doc['_id']], doc)}}"
                }
            }
        }
        return doc

    @staticmethod
    def is_all_selected_in_model(model):
        for i in range(model.rowCount()):
            item = model.itemFromIndex(model.index(i, 0))
            if item.checkState() == Qt.Unchecked:
                return False
        return True

    @staticmethod
    def filter_last_n_elements(elements, n):
        if len(elements) in range(n + 1):
            return elements
        else:
            return elements[-n:]

    @staticmethod
    def filter_positionable_list_attribute(target, iface):
        """
        Replace all attribute of type list by a single value;
        for example all observations of a 'Desordre' are replace by the most recent observation.
        """
        for elem in target:
            for attr in elem:
                if type(elem[attr]) == list and len(elem[attr]) != 0:
                    if attr == 'prestationIds':
                        elem[attr] = Utils.filter_last_n_elements(elem[attr], 3)
                    else:
                        if len(elem[attr]) > 1:
                            elem[attr] = [try_extract_most_recent(elem[attr], iface)]
                        else:
                            elem[attr] = [elem[attr][0]]

    @staticmethod
    def filter_object_by_attributes(obj, attributes):
        target = obj.copy()

        linear_id = None

        for attr in target:
            if attr not in attributes:
                del obj[attr]
            else:
                if attr == "linearId":
                    linear_id = obj[attr]
        return linear_id


# @staticmethod
def try_extract_most_recent(list_attribute: list, iface, date_attribute_name: str = "date",
                            date_format: str = "%Y-%m-%d"):
    """
    Try to return most recent object from the input list
    :param iface: iface in order to be able to display messages in qgis
    :param date_attribute_name: key to retrieve date in the list's elements; default value 'date'
    :param date_format: expected format of the date attribute; default value '%Y-%m-%d' for yyyy-mm-dd format
    :param list_attribute: List to reduce
    :return: None if empty list ; last element if objects of the list doesn't have a date attribute with format
            yyyy-MM-dd; else the last object of the list according to the 'date' attribute
    """
    if len(list_attribute) == 0:
        return None
    most_recent = list_attribute[-1]
    most_recent_date = None

    try:
        for obj in list_attribute:
            if date_attribute_name in obj:
                try:
                    current_date = strptime(obj[date_attribute_name], date_format)
                    if most_recent_date is None or most_recent_date < current_date:
                        most_recent = obj
                        most_recent_date = current_date
                except Exception as e:
                    simple_message(iface, "error on date parsing : " + str(e))
        return most_recent
    except Exception as e:
        #     simple_message(iface, "e") # debug purpose
        return most_recent
