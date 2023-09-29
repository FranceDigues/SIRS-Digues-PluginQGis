#!/bin/bash

rm couchdb_importer*.zip

if [ -z "$1" ]
then
zip -r couchdb_importer.zip ./couchdb_importer
else
zip -r couchdb_importer_"$1".zip ./couchdb_importer
fi
