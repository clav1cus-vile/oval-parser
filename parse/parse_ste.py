import defusedxml.ElementTree as ET

def parse_ste(xml_file):
    oval_ns = {'oval': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
               'red-def': 'http://oval.mitre.org/XMLSchema/oval-definitions-5/linux/Red_Hat/rpminfo'}

    oval_states = []

    for rpm_state in ET.parse(xml_file).findall('.//oval:states/*', oval_ns):
        state_info = {'state_id': rpm_state.get('id'), 'state_version': rpm_state.get('version')}

        for subelement in rpm_state:
            if subelement.tag.endswith('arch'):
                state_info['arch_operation'] = subelement.get('operation')
                state_info['arch_text'] = subelement.text
            elif subelement.tag.endswith('evr'):
                state_info['evr_operation'] = subelement.get('operation')
                state_info['evr_text'] = subelement.text
            elif subelement.tag.endswith('os_release'):
                state_info['os_operation'] = subelement.get('operation')
                state_info['os_text'] = subelement.text
            elif subelement.tag.endswith('signature_keyid'):
                state_info['signature_keyid_operation'] = subelement.get('operation')
                state_info['signature_keyid_text'] = subelement.text
            elif subelement.tag.endswith('name'):
                state_info['name_operation'] = subelement.get('operation')
                state_info['name_text'] = subelement.text
            elif subelement.tag.endswith('version'):
                state_info['version_operation'] = subelement.get('operation')
                state_info['version_text'] = subelement.text
            elif subelement.tag.endswith('text'):
                state_info['text_operation'] = subelement.get('operation')
                state_info['text_text'] = subelement.text
            else:
                state_info[subelement.tag.split('}')[1]] = subelement.text

        oval_states.append(state_info)

    return oval_states