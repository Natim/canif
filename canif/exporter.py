# -*- coding: utf-8 -*-
import csv

from six import StringIO


def export_insee_data(backend, communes, variables):
    csv_output = StringIO()
    writer = csv.writer(csv_output, delimiter=';')

    vars = backend.get_variables(variables)
    header_vars = [v['var_lib'] for v in vars]
    # Write header
    writer.writerow(["CODGEO"] + header_vars)

    # For each codgeo
    for codgeo in communes:
        values = [codgeo]
        for var in variables:
            values.append(backend.get_data(var.lower(), codgeo)['value'])
        writer.writerow(values)

    csv_output.seek(0)
    return csv_output
