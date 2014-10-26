# -*- coding: utf-8 -*-
import csv


def import_insee_variables(backend, csvfile):
    """Load a CSV file variable."""
    dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=";,")
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

    # Build the header
    header = [x.lower() for x in next(reader)]
    assert header[0] == "var_id", header[0]

    # Add all the variables
    variables = 0
    for row in reader:
        obj = {}
        for i in range(min(len(header), len(row))):
            obj[header[i]] = row[i].strip()
        obj["var_lib"] = "%s (%s)" % (obj['var_lib'], obj['annee'])
        obj["var_lib_long"] = "%s (%s)" % (obj['var_lib_long'],
                                           obj['annee'])
        backend.set_variable(row[0].lower(), obj)
        variables += 1

    return variables


def import_insee_data(backend, csvfile, progress=None):
    """Load a CSV file variable."""
    dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=";,")
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

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

        if progress:
            progress(communes)

    return communes, insee_values
