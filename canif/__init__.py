# -*- coding: utf-8 -*-
# Little script that takes a Excel file and put it in Elasticsearch

from __future__ import print_function
import csv
import sys
import asyncio
import asyncio_redis
import limpyd

from canif.models import Communes, Variables, redis_settings


def import_insee_variables():
    """Import INSEE Variables"""
    input_filename = sys.argv[1]

    variables = 0
    with open(input_filename, newline='', encoding='utf-8') as csv_input:
        reader = csv.reader(csv_input, delimiter=';')

        # Build the header
        header = [x.lower() for x in next(reader)]

        # Add all the variables
        for row in reader:
            obj = {}
            for i in range(min(len(header), len(row))):
                obj[header[i]] = row[i]
            Variables(**obj)
            variables += 1

    print("%d variables importées" % variables)


def import_insee_data():
    """Import INSEE Data"""
    @asyncio.coroutine
    def import_line(connection, key, header, values):
        for idx in range(min(len(header), len(values))):
            yield from connection.set(
                "insee:data:codegeo_%s:%s" % (key, header[idx]),
                values[idx])

    @asyncio.coroutine
    def import_file(input_filename):
        sep = ['|', '/', '-', '\\']
        # Create Redis connection
        connection = yield from asyncio_redis.Connection.create(**redis_settings)

        with open(input_filename, newline='', encoding='utf-8') as csv_input:
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

                try:
                    Communes(codgeo=key, libgeo=values[header.index("libgeo")])
                except limpyd.exceptions.UniquenessError:
                    pass
                yield from asyncio.Task(import_line(connection, key, header, values))
                communes += 1
                print("%s %d communes importées" % (sep[communes % 4], communes), end="\r")

        # When finished, close the connection.
        connection.close()

        print(
            "%s variables importées dans %d communes importées soit %d valeurs" % (
                insee_values, communes, insee_values * communes
            )
        )

    # Start the ioloop
    loop = asyncio.get_event_loop()
    input_filename = sys.argv[1]
    loop.run_until_complete(import_file(input_filename))


def export_insee():
    @asyncio.coroutine
    def build_line(connection, codgeo, variables):
        coros = []
        for var in variables:
            coros.append(asyncio.Task(
                connection.get("insee:data:codegeo_%s:%s" % (
                    codgeo, var.lower()))))
        values = yield from asyncio.gather(*coros)
        return [codgeo] + values


    @asyncio.coroutine
    def export_file(output_filename, communes_codes, variables):
        # Create Redis connection
        connection = yield from asyncio_redis.Connection.create(**redis_settings)
    
        with open(output_filename, "w", newline='', encoding='utf-8') as csv_output:
            writer = csv.writer(csv_output, delimiter=';')
            
            coros = []
            # Write header
            writer.writerow(["CODGEO"] + variables)

            # For each codgeo
            for codgeo in communes_codes:
                row = yield from build_line(connection, codgeo, variables)
                writer.writerow(row)
                
            # When finished, close the connection.
            connection.close()

    # Start the ioloop
    loop = asyncio.get_event_loop()
    output_filename = sys.argv[1]
    COMMUNES = ["35281", "69123", "94058", "25539", "25071", "90009", "90010"]
    VARIABLES = ["LIBGEO", "P10_POP", "P99_POP", "D90_POP", "D82_POP", "D75_POP"]
    loop.run_until_complete(export_file(output_filename, COMMUNES, VARIABLES))
