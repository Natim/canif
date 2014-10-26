# -*- coding: utf-8 -*-
# Little script that takes a Excel file and put it in Redis

from __future__ import print_function
import csv
import sys
import redis
import json

redis_settings = dict(
    host="localhost",
    port=6379,
    db=1
)

connection = redis.StrictRedis(**redis_settings)


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
                obj[header[i]] = row[i]
            connection.set("insee_variable:%s" % row[0].lower(),
                           json.dumps(obj))
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

            for idx in range(min(len(header), len(values))):
                connection.set(
                    "insee_data_%s:%s" % (header[idx], key),
                    values[idx])
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
        writer = csv.writer(csv_output, delimiter=';')

        # Write header
        writer.writerow(["CODGEO"] + VARIABLES)

        # For each codgeo
        for codgeo in COMMUNES:
            values = [codgeo]
            for var in VARIABLES:
                values.append(connection.get(
                    "insee_data_%s:%s" % (var.lower(), codgeo)))

            writer.writerow(values)

    print("%s variables exportées pour %d communes soit %d valeurs" % (
        len(VARIABLES), len(COMMUNES), len(VARIABLES) * len(COMMUNES)
    ))
