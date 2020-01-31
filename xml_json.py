import xml.etree.ElementTree as ET
import copy
from collections import OrderedDict


def _visit_child_element(elem):
    tv_pair = OrderedDict()
    if elem.text != None:
        tv_pair[elem.tag] = elem.text
        tv_pair.update(elem.attrib)
    else:
        tv_pair[elem.tag] = copy.deepcopy(elem.attrib)

    return tv_pair

def _visit_parent_element(elem):
    parent_m = OrderedDict()
    
    child_m = []
    for child in elem:
        child_m.append(xml_element_json(child))

    child_keys = [k for c in child_m for k in c.keys()]
    set_child_keys = set(child_keys)
    if len(child_keys) == len(set_child_keys) and len(set_child_keys) != 1:
        parent_m[elem.tag] = OrderedDict()
        for c in child_m:
            for k, v in c.items():
                parent_m[elem.tag][k] = v
    elif len(set_child_keys) == -1:
        parent_m[elem.tag] = []
        for c in child_m:
            for k, v in c.items():
                parent_m[elem.tag].append(v)
    else:
        parent_m[elem.tag] = child_m
    return parent_m

def xml_element_json(elem):
    if len(elem) > 0:
        return _visit_parent_element(elem)
    else:
        return _visit_child_element(elem)

if __name__ == '__main__':
    tree = ET.parse('a.xml')
    json_data = xml_element_json(tree.getroot())
    import json
    print(json.dumps(json_data, separators=(',', ':')))
