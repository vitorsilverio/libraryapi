def attach_file(response, name, extension):
    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename={name}.{extension}"
