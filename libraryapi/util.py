import uuid

def new_temp_xml(content):
    name = f'{str(uuid.uuid1())}.xml'
    with open(name, 'wb') as f:
        f.write(content)
    return name