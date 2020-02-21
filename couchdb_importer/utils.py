class Utils:
    @staticmethod
    def build_query(searchedClass):
        mango = {
            "selector": {
                "@class": {
                    "$eq": "fr.sirs.core.model." + searchedClass
                }
            }
        }
        return mango

    @staticmethod
    def build_tuple(item, criteria):
        list = []
        for key in criteria:
            if key in item.keys():
                list.append(item[key])
            else:
                list.append(None)
        return tuple(list)

    @staticmethod
    def find_criteria_from_class(type):
        switcher = {
            'Desordre': ['_id', \
                         '_rev', \
                         '@class', \
                         'borne_debut_aval', \
                         'borne_debut_distance', \
                         'prDebut', \
                         'valid', \
                         'designation', \
                         'longitudeMin', \
                         'longitudaMax', \
                         'latitudeMin', \
                         'latitudeMax', \
                         'editedGeoCoordinate', \
                         'borneDebutId', \
                         'borneFinId', \
                         'systemRepId', \
                         'sourceId', \
                         'typeDesordreId', \
                         'observations', \
                         'foreignParentId', \
                         'positionDebut', \
                         'positionFin', \
                         'geometry', \
                         'date_debut', \
                         'date_fin'],
            'TronconDigue': ['_id', \
                             '_rev', \
                             '@class', \
                             'libelle', \
                             'designation', \
                             'valid', \
                             'digueId', \
                             'typeRiveId', \
                             'systemeRepDefautId', \
                             'date_debut', \
                             'geometry'
                             ],
            'TronconLit': ['_id', \
                           '_rev', \
                           '@class', \
                           'libelle', \
                           'author', \
                           'valid', \
                           'systemRepDefaultId', \
                           'date_debut', \
                           'dateMaj', \
                           'geometry']
        }
        return switcher.get(type, 'Invalid class reference')

    @staticmethod
    def is_str_start_by_underscore(var):
        if type(var) is str:
            return var.find('_') == 0
        return False

    @staticmethod
    def get_geometry_index(criteria):
        i = 0
        for crit in criteria:
            if crit == "geometry":
                return i
            i = i + 1
        return 0
