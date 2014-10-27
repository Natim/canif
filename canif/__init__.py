# -*- coding: utf-8 -*-
# Little script that takes a Excel file and put it in Redis

from __future__ import print_function
import sys

from canif.exporter import export_insee_data
from canif.importer import csv, xls

# from canif.redis import RedisBackend
# backend = RedisBackend()

from canif.elasticsearch import ElasticsearchBackend
backend = ElasticsearchBackend()


#######################
# CSV file management #
#######################

def import_csv_variables():
    """Import INSEE Variables from a CSV file"""
    input_filename = sys.argv[1]

    with open(input_filename) as csv_input:
        variables = csv.import_insee_variables(backend, csv_input)

    print("%d variables importées" % variables)


def import_csv_data():
    """Import INSEE Data"""
    input_filename = sys.argv[1]

    def progress(communes):
        sep = ['|', '/', '-', '\\']
        print("%s %d communes importées" % (sep[communes % 4], communes),
              end="\r")

    with open(input_filename) as csv_input:
        communes, insee_values = csv.import_insee_data(
            backend, csv_input, progress
        )

    print("%s variables importées dans %d communes importées "
          "soit %d valeurs" % (
              insee_values, communes, insee_values * communes
          ))


def export_csv():
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


#######################
# XLS file management #
#######################

def import_xls_variables():
    """Import INSEE Variables from a XLS file"""
    input_filename = sys.argv[1]

    variables = xls.import_insee_variables(backend, input_filename)

    print("%d variables importées" % variables)


def import_xls_data():
    """Import INSEE data from a XLS file"""
    input_filename = sys.argv[1]

    def progress(communes):
        sep = ['|', '/', '-', '\\']
        print("%s %d communes importées" % (sep[communes % 4], communes),
              end="\r")

    communes, insee_values = xls.import_insee_data(
        backend, input_filename, progress)

    print("%s variables importées dans %d communes importées "
          "soit %d valeurs" % (
              insee_values, communes, insee_values * communes
          ))
