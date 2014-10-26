# -*- coding: utf-8 -*-
from xlrd import open_workbook


def import_insee_variables(backend, input_filename):
    """Load a CSV file variable."""
    book = open_workbook(input_filename, on_demand=True)
    variables = 0
    sheet = book.sheet_by_name("Liste des variables")
    nb_rows = sheet.nrows

    for x in range(20):
        if sheet.cell(x, 0).value.lower() == "var_id":
            header_row = x
            break

    header = [x.value.lower() for x in sheet.row(header_row)]

    variables_first_row = header_row + 1

    for row in range(nb_rows - variables_first_row):
        current_row_number = variables_first_row + row
        current_row = list(sheet.row(current_row_number))

        obj = {}
        for i, cell in enumerate(current_row):
            if isinstance(cell.value, float):
                value = "%d" % cell.value
            else:
                value = "%s" % cell.value
            obj[header[i]] = value.strip()
        obj["var_lib"] = "%s (%s)" % (obj['var_lib'], obj['annee'])
        obj["var_lib_long"] = "%s (%s)" % (obj['var_lib_long'],
                                           obj['annee'])

        backend.set_variable(current_row[0].value.lower(), obj)
        variables += 1

    return variables


def import_insee_data(backend, input_filename, progress=None):
    """Load an XLS file data."""

    def import_sheet(book, sheet_name):
        sheet = book.sheet_by_name(sheet_name)
        nb_rows = sheet.nrows

        for x in range(20):
            if sheet.cell(x, 0).value.lower() == "codgeo":
                header_row = x
                break

        header = [x.value.lower() for x in sheet.row(header_row)][1:]
        data_first_row = header_row + 1

        # Add all the codegeo
        communes = 0
        insee_values = len(header)
        for row in range(nb_rows - data_first_row):
            current_row_number = data_first_row + row
            current_row = list(sheet.row(current_row_number))

            key = current_row[0].value
            values = current_row[1:]

            obj = {}
            for i, cell in enumerate(values):
                if isinstance(cell.value, float):
                    value = "%d" % cell.value
                else:
                    value = "%s" % cell.value
                obj[header[i]] = value.strip()

                backend.set_data(header[i], key, {"value": value})

            backend.set_commune(key, {
                "codgeo": key,
                "libgeo": values[header.index("libgeo")].value
            })

            communes += 1

            if progress:
                progress(communes)

        return communes, insee_values

    # Import communes
    book = open_workbook(input_filename, on_demand=True)

    print("COMMUNES")
    com_communes, com_insee_values = import_sheet(book, "COM")

    print("\nARRONDISSEMENTS")
    arm_communes, arm_insee_values = import_sheet(book, "ARM")

    return com_communes + arm_communes, com_insee_values + com_insee_values
