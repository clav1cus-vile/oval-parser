import defusedxml.ElementTree as ET

oval_ns = {'oval': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
           'red-def': 'http://oval.mitre.org/XMLSchema/oval-definitions-5/linux/Red_Hat/rpminfo'}

def extract_comments(criteria_elem):
    comments = [
        criterion_elem.get("comment")
        for criterion_elem in criteria_elem
        if criterion_elem.get("comment")
    ]

    nested_criteria_elem = criteria_elem.find(".//oval:criteria", namespaces=oval_ns)
    if nested_criteria_elem is not None:
        comments.extend(extract_comments(nested_criteria_elem))

    return comments

def parse_def(xml_file):
    oval_definitions = []

    for definition_elem in ET.parse(xml_file).findall(".//oval:definition", namespaces=oval_ns):
        definition = {
            "id": definition_elem.get("id"),
            "class": definition_elem.get("class"),
            "metadata": {},
            "criteria_comments": extract_comments(definition_elem.find(".//oval:criteria", namespaces=oval_ns))
        }

        metadata_elem = definition_elem.find(".//oval:metadata", namespaces=oval_ns)
        if metadata_elem is not None:
            for item_elem in metadata_elem:
                tag_name = item_elem.tag.split("}")[1]

                if tag_name == "affected":
                    platform_elem = item_elem.find(".//oval:platform", namespaces=oval_ns)
                    definition["metadata"][tag_name] = platform_elem.text if platform_elem is not None else item_elem.text
                elif tag_name == "reference":
                    ref_id_elem = item_elem.get("ref_id")
                    ref_url_elem = item_elem.get("ref_url")

                    if ref_id_elem and ref_url_elem:
                        source_elem = item_elem.get("source", "")
                        metadata_key = "RHSA" if "RHSA" in source_elem else "CVE" if "CVE" in source_elem else tag_name
                        url_key = f"{metadata_key}_url"

                        definition["metadata"].setdefault(metadata_key, []).append(ref_id_elem)
                        definition["metadata"].setdefault(url_key, []).append(ref_url_elem)
                else:
                    definition["metadata"][tag_name] = item_elem.text

        oval_definitions.append(definition)

    return oval_definitions