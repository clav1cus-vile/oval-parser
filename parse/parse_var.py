import defusedxml.ElementTree as ET

def parse_var(xml_file):
    oval_ns = {'oval': 'http://oval.mitre.org/XMLSchema/oval-definitions-5'}

    variables_list = []

    for variable in ET.parse(xml_file).findall('.//oval:variables/*', oval_ns):
        variable_info = {
            'variable_id': variable.get('id'),
            'variable_version': variable.get('version'),
            'variable_comment': variable.get('comment'),
            'variable_datatype': variable.get('datatype'),
            'arithmetic': {}
        }

        for subelement in variable:
            if subelement.tag.endswith('arithmetic'):
                arithmetic_info = {
                    'arithmetic_operation': subelement.get('arithmetic_operation'),
                    'components': []
                }

                for component in subelement:
                    component_info = {
                        component.tag.split('}')[1]: component.text if component.tag.endswith('literal_component') else component.get('object_ref')
                    }
                    arithmetic_info['components'].append(component_info)

                variable_info['arithmetic'] = arithmetic_info

        variables_list.append(variable_info)

    return variables_list