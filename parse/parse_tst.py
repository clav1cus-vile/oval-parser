import defusedxml.ElementTree as ET

def parse_tst(xml_file):
    oval_ns = {'oval': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
               'red-def': 'http://oval.mitre.org/XMLSchema/oval-definitions-5/linux/Red_Hat/rpminfo'}

    oval_tests = []

    for rpm_test in ET.parse(xml_file).findall('.//oval:tests/*', oval_ns):
        test_info = {'test_id': rpm_test.get('id'), 'test_version': rpm_test.get('version'), 'test_check': rpm_test.get('check'), 'test_comment': rpm_test.get('comment')}

        for subelement in rpm_test:
            if subelement.tag.endswith('object'):
                test_info['object_ref'] = subelement.get('object_ref')
            elif subelement.tag.endswith('state'):
                test_info['state_ref'] = subelement.get('state_ref')
            else:
                test_info[subelement.tag.split('}')[1]] = subelement.text

        oval_tests.append(test_info)

    return oval_tests