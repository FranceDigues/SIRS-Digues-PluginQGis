import glob
import json
import sys


def load_labels_from_properties():
    propertieDictionnary = {}
    propertiesFileName = glob.glob('newModel/*')

    # iterate on file properties
    for path in propertiesFileName:
        filestr = path.split('/')[1]
        clazz = filestr.split('.')[0]
        propertieDictionnary[clazz] = {}

        with open(path) as propertieFile:
            propertieFileStr = propertieFile.read()
            rows = propertieFileStr.split('\n')[2:-1]
        for row in rows:
            r = row.split('=')
            propertieDictionnary[clazz][r[0]] = r[1]

        # Does not exist in properties file
        propertieDictionnary[clazz]["_id"] = "_id (ne pas modifier/supprimer)"
    return propertieDictionnary


def print_new_labels():
    print(json.dumps(load_labels_from_properties(), sort_keys=True, indent=2))


def pretty_print_json(js):
    print(json.dumps(js, sort_keys=True, indent=2))


def load_user_preferences_from_labels():
    labels = load_labels_from_properties()
    user_preferences = {}

    for clazz in labels:
        user_preferences[clazz] = {"attributes": {}}
        for attribute in labels[clazz]:
            user_preferences[clazz]["attributes"][attribute] = True

        # Does not exist in propertie file
        user_preferences[clazz]["attributes"]["_id"] = True
        user_preferences[clazz]["attributes"]["_rev"] = True
        user_preferences[clazz]["attributes"]["@class"] = True
    return user_preferences


def update_photo(data, clazz):
    # Fit for classical photos
    # photos = {
    #     "photos actuelle: author": "str",
    #     "photos actuelle: borneDebutId": "str",
    #     "photos actuelle: borneFinId": "str",
    #     "photos actuelle: borne_debut_aval": "str",
    #     "photos actuelle: borne_debut_distance": "float",
    #     "photos actuelle: borne_fin_aval": "str",
    #     "photos actuelle: borne_fin_distance": "float",
    #     "photos actuelle: chemin": "str",
    #     "photos actuelle: commentaire": "str",
    #     "photos actuelle: coteId": "str",
    #     "photos actuelle: date": "str",
    #     "photos actuelle: designation": "str",
    #     "photos actuelle: editedGeoCoordinate": "bool",
    #     "photos actuelle: geometry": "str",
    #     "photos actuelle: geometryMode": "str",
    #     "photos actuelle: latitudeMax": "float",
    #     "photos actuelle: latitudeMin": "float",
    #     "photos actuelle: libelle": "str",
    #     "photos actuelle: longitudeMax": "float",
    #     "photos actuelle: longitudeMin": "float",
    #     "photos actuelle: orientationPhoto": "str",
    #     "photos actuelle: photographeId": "str",
    #     "photos actuelle: positionDebut": "str",
    #     "photos actuelle: positionFin": "str",
    #     "photos actuelle: prDebut": "float",
    #     "photos actuelle: prFin": "float",
    #     "photos actuelle: systemeRepId": "str",
    #     "photos actuelle: valid": "bool",
    # }
    photos = {
        "photos actuelle: author": "str",
        "photos actuelle: chemin": "str",
        "photos actuelle: commentaire": "str",
        "photos actuelle: date": "str",
        "photos actuelle: libelle": "str",
        "photos actuelle: photographeId": "str",
        "photos actuelle: valid": "bool",
    }
    for key in photos:
        data[clazz][key] = photos[key]


def update_observation(data, clazz):
    # Fit for classical Observations
    observations = {
        "observations actuelle: author": "str",
        "observations actuelle: date": "str",
        "observations actuelle: designation": "str",
        "observations actuelle: evolution": "str",
        "observations actuelle: nombreDesordres": "int",
        "observations actuelle: observateurId": "str",
        "observations actuelle: photos actuelle: author": "str",
        "observations actuelle: photos actuelle: borneDebutId": "str",
        "observations actuelle: photos actuelle: borneFinId": "str",
        "observations actuelle: photos actuelle: borne_debut_aval": "str",
        "observations actuelle: photos actuelle: borne_debut_distance": "float",
        "observations actuelle: photos actuelle: borne_fin_aval": "str",
        "observations actuelle: photos actuelle: borne_fin_distance": "float",
        "observations actuelle: photos actuelle: chemin": "str",
        "observations actuelle: photos actuelle: commentaire": "str",
        "observations actuelle: photos actuelle: coteId": "str",
        "observations actuelle: photos actuelle: date": "str",
        "observations actuelle: photos actuelle: designation": "str",
        "observations actuelle: photos actuelle: editedGeoCoordinate": "bool",
        "observations actuelle: photos actuelle: geometry": "str",
        "observations actuelle: photos actuelle: geometryMode": "str",
        "observations actuelle: photos actuelle: latitudeMax": "float",
        "observations actuelle: photos actuelle: latitudeMin": "float",
        "observations actuelle: photos actuelle: libelle": "str",
        "observations actuelle: photos actuelle: longitudeMax": "float",
        "observations actuelle: photos actuelle: longitudeMin": "float",
        "observations actuelle: photos actuelle: orientationPhoto": "str",
        "observations actuelle: photos actuelle: photographeId": "str",
        "observations actuelle: photos actuelle: positionDebut": "str",
        "observations actuelle: photos actuelle: positionFin": "str",
        "observations actuelle: photos actuelle: prDebut": "float",
        "observations actuelle: photos actuelle: prFin": "float",
        "observations actuelle: photos actuelle: systemeRepId": "str",
        "observations actuelle: photos actuelle: valid": "bool",
        "observations actuelle: suite": "str",
        "observations actuelle: urgenceId": "str",
        "observations actuelle: valid": "bool"
    }
    for key in observations:
        data[clazz][key] = observations[key]


def load_attribute_type_from_labels():
    labels = load_labels_from_properties()
    attribute_types = {}

    for clazz in labels:
        attribute_types[clazz] = {}

        for attribute in labels[clazz]:
            if attribute in ["class", "classAbrege", "classPlural"]:
                continue
            if attribute[-3:] == 'Ids':
                attribute_types[clazz][attribute + " actuelle:"] = "str"
            elif attribute == 'observations':
                update_observation(attribute_types, clazz)
            elif attribute == 'photos':
                update_photo(attribute_types, clazz)
            else:
                attribute_types[clazz][attribute] = "str"

        # Does not exist in properties file
        attribute_types[clazz]["@class"] = "str"
        attribute_types[clazz]["_id"] = "str"
        attribute_types[clazz]["_rev"] = "str"

    return attribute_types


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "-l":
            labels = load_labels_from_properties()
            pretty_print_json(labels)
        elif sys.argv[1] == "-p":
            up = load_user_preferences_from_labels()
            pretty_print_json(up)
        elif sys.argv[1] == "-a":
            at = load_attribute_type_from_labels()
            pretty_print_json(at)
        else:
            print("\totpion1 = -l (display labels)\n\toption2 = -p (display"
                  " preferences)\n\toption3 = -a (display attributes)")
    else:
        print("\totpion1 = -l (display labels)\n\toption2 = -p (display"
              " preferences)\n\toption3 = -a (display attributes)")



