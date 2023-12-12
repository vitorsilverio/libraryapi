import xml.etree.ElementTree as ET
from io import BytesIO
from typing import Callable

import pymarc  # type: ignore
from fastapi.responses import Response
from fastapi.responses import StreamingResponse
from pymarc import Record


def attach_file(response, name, extension):
    response.headers["Content-Disposition"] = f"attachment; filename={name}.{extension}"


def marc_provider(record: Record) -> Response:
    response = StreamingResponse(
        BytesIO(record.as_marc()), media_type="application/marc"
    )
    attach_file(response, record.get_fields("001")[0].data, "mrc")
    return response


def xml_provider(record: Record) -> Response:
    node = pymarc.marcxml.record_to_xml_node(record, namespace=True)
    xml = ET.tostring(node, encoding="utf-8", xml_declaration=True)
    return Response(xml, media_type="application/xml; charset=utf-8")


def txt_provider(record: Record) -> Response:
    response = Response(str(record), media_type="text/plain; charset=utf-8")
    attach_file(response, record.get_fields("001")[0].data, "mrk")
    return response


def json_provider(record: Record) -> Response:
    return Response(record.as_json(), media_type="application/json; charset=utf-8")


media_types: dict[str, Callable[[Record], Response]] = {
    "application/marc": marc_provider,
    "application/xml": xml_provider,
    "text/plain": txt_provider,
    "application/json": json_provider,
}
