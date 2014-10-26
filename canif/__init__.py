# -*- coding: utf-8 -*-
# Little script that takes a Excel file and put it in Redis

from __future__ import print_function
import csv
import sys

from canif.redis import RedisBackend
from canif.exporter import export_insee_data

backend = RedisBackend()


def import_insee_variables():
    """Import INSEE Variables"""
    input_filename = sys.argv[1]

    variables = 0
    with open(input_filename) as csv_input:
        reader = csv.reader(csv_input, delimiter=';')

        # Build the header
        header = [x.lower() for x in next(reader)]
        assert header[0] == "var_id", header[0]

        # Add all the variables
        for row in reader:
            obj = {}
            for i in range(min(len(header), len(row))):
                obj[header[i]] = row[i].strip()
            obj["var_lib"] = "%s (%s)" % (obj['var_lib'], obj['annee'])
            obj["var_lib_long"] = "%s (%s)" % (obj['var_lib_long'],
                                               obj['annee'])
            backend.set_variable(row[0].lower(), obj)
            variables += 1

    print("%d variables importées" % variables)


def import_insee_data():
    """Import INSEE Data"""
    sep = ['|', '/', '-', '\\']
    input_filename = sys.argv[1]

    with open(input_filename) as csv_input:
        reader = csv.reader(csv_input, delimiter=';')
        # Build the header
        header = [x.lower() for x in next(reader)]
        assert header[0] == "codgeo", header[0]
        header = header[1:]

        # Add all the codegeo
        communes = 0
        insee_values = len(header)

        for row in reader:
            key = row[0]
            values = row[1:]

            backend.set_commune(key, {
                "codgeo": key,
                "libgeo": values[header.index("libgeo")]
            })

            for idx in range(min(len(header), len(values))):
                backend.set_data(header[idx], key, {"value": values[idx]})
            communes += 1
            print("%s %d communes importées" % (sep[communes % 4], communes),
                  end="\r")

        print("%s variables importées dans %d communes importées "
              "soit %d valeurs" % (
                  insee_values, communes, insee_values * communes
              ))


def export_insee():
    output_filename = sys.argv[1]
    COMMUNES = ["35281", "69123", "94058", "25539", "25071", "90009", "90010"]
    VARIABLES = ["LIBGEO", "P10_POP", "P99_POP", "D90_POP", "D82_POP",
                 "D75_POP"]

    with open(output_filename, "w") as csv_output:
        csv_output.write(
            export_insee_data(backend, COMMUNES, VARIABLES).read()
        )

    print("%s variables exportées pour %d communes soit %d valeurs" % (
        len(VARIABLES), len(COMMUNES), len(VARIABLES) * len(COMMUNES)
    ))
