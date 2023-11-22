import defusedxml.ElementTree as ET

def parse_obj(xml_file):
    oval_ns = {'oval': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
               'red-def': 'http://oval.mitre.org/XMLSchema/oval-definitions-5/linux/Red_Hat/rpminfo'}

    oval_objects = []

    for rpm_object in ET.parse(xml_file).findall('.//oval:objects/*', oval_ns):
        object_info = {'object_id': rpm_object.get('id'), 'object_version': rpm_object.get('version')}

        for subelement in rpm_object:
            if subelement.tag.endswith('pattern'):
                object_info['pattern_operation'] = subelement.get('operation')
            if subelement.tag.endswith('instance'):
                object_info['var_ref'] = subelement.get('var_ref')
            else:
                object_info[subelement.tag.split('}')[1]] = subelement.text

        oval_objects.append(object_info)

    return oval_objects