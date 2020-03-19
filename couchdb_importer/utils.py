class Utils:
    @staticmethod
    def parse_url(url):
        split_url = url.split("://")
        if len(split_url) == 2:
            http = split_url[0]
            addr = split_url[1]
        else:
            http = "localhost"
            addr = "5984"
        return http, addr

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
                }
            }
            if attributes is not None:
                mango["fields"]=attributes
        else:
            mango = {
                "selector": {
                    "@class": "fr.sirs.core.model." + className
                }
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
            }
        }
        return mango

    @staticmethod
    def is_str_start_by_underscore(var):
        if type(var) is str:
            return var.find('_') == 0
        return False

    @staticmethod
    def get_label(positionable):
        if 'libelle' in positionable:
            return positionable['libelle']
        elif 'designation' in positionable:
            return positionable['designation']
        else:
            return 'NULL'

    @staticmethod
    def build_row_name_positionable(positionable):
        className = positionable["@class"].split("fr.sirs.core.model.")[1]
        label = Utils.get_label(positionable)
        id = positionable["_id"]
        name = className + " - " + label + " - " + id
        return name

    @staticmethod
    def build_list_from_preference(obj):
        result = []
        for item in obj:
            if obj[item]:
                result.append(item)
        return result

    @staticmethod
    def build_list_id_from_data(data):
        result = []
        for className in data:
            result.extend(data[className]["ids"].keys())

        return result
