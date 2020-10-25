
###########################################################################
#
# this module meant to provide intuitive functions to work with xml files
#
###########################################################################


# will return a list of nodes specified by an attribute key and an attribute value
def get_nodes(xml_file, node_tag, node_att_name=None, node_att_val=None):
    root = xml_file.getroot()
    if root.tag == node_tag:
        return [root]
    selector = node_tag
    if node_att_name is not None:
        if node_att_val is not None:
            selector = node_tag + "/[@" + node_att_name + "='" + node_att_val + "']"
        else:
            selector = node_tag + "/[@" + node_att_name + "]"
    return root.findall(selector)


# will return a list of nodes which doesn't have a specific attribute
def get_nodes_from_xml_without_att(xml_file, node_tag, node_att_name=None):
    root = xml_file.getroot()
    relevant_nodes = []
    nodes = root.findall(node_tag)
    for node in nodes:
        if get_node_att(node, node_att_name) is None:
            relevant_nodes.append(node)
    return relevant_nodes


def nodes_to_dict(nodes, att_key):
    """
    Will turn a list of xml nodes to a dictionary carrying the nodes.
    The keys of the dictionary will be the attribute value of each node and the values of of the dictionary will be the inner text
    of each node.

    For example, if we have these xml nodes:
        <string name="app_name">First Remote</string>
        <string name="app_short_name" translatable="false">remote</string>

    xml_nodes_to_dict(nodes, 'name') will return:
    dict = {'app_name': 'First Remote', 'app_short_name': 'remote'}

    param nodes: the xml nodes to search upon
    param att_key: the attribute to search for it's value in each node
    return: a dictionary representation of the nodes
    """

    nodes_dict = {}
    for node in nodes:
        nodes_dict[get_node_att(node, att_key)] = get_text_from_node(node)
    return nodes_dict

# will return all of the direct children of a given node
def get_all_direct_child_nodes(node):
    return list(node)

# will return the text (inner html) of a given node
def get_text_from_node(node):
    return node.text


# will return the text from a specific node
def get_text(xml_file, node_tag, node_att_name=None, node_att_val=None):
    return get_text_from_node(get_nodes(xml_file, node_tag, node_att_name, node_att_val)[0])


# will set the text (inner html) in a given node
def set_node_text(node, text):
    node.text = text


# will return the value of a given att from a desired node
def get_node_att(node, att_name):
    return node.get(att_name)


# will return an xml file
def read_xml_file(xml_path):
    import xml.etree.ElementTree as et
    return et.parse(xml_path)


# will save the changes made in an xml file
def save_xml_file(xml_file, xml_path, add_utf_8_encoding=False):
    if add_utf_8_encoding:
        xml_file.write(xml_path, encoding="UTF-8")
    else:
        xml_file.write(xml_path)


# will create an xml file
def create_xml_file(root_node_tag, output_file):
    import xml.etree.ElementTree as et
    xml = et.Element(root_node_tag)
    tree = et.ElementTree(xml)
    save_xml_file(tree, output_file)
    return tree


def add_node(doc, node_tag, att_dict={}, node_text=None, parent_node=None):
    """
    Will add a node to a certain (relative) location
    Args:
        param xml: the xml file
        param parent_node: the parent of the node to add (for root, leave blank)
        param node_tag: the tag of the node ('String', for example)
    """
    if parent_node is None:
        parent_node = doc.getroot()
    import xml.etree.ElementTree as et
    node = et.SubElement(parent_node, node_tag, att_dict)
    if node_text is not None:
        set_node_text(node, node_text)
    return node


# will add attribute to a given node
def set_node_atts(node, atts_dict):
    for key, val in atts_dict.items():
        node.set(key, val)


# Will turn a simple dictionary to an xml file, by hierarchical order
def simple_dict_to_xml(xml_dict, root_name, output_path):
    # will unpack the parent recursively
    def recursive_unpack_parent(parent_dict, parent=None):
        for key, val in parent_dict.items():
            parent = add_node(xml, key, parent_node=parent)
            if type(val) is dict:
                recursive_unpack_parent(val, parent)

    xml = create_xml_file(root_name, output_path)
    recursive_unpack_parent(xml_dict)
    save_xml_file(xml, output_path)


def get_root_node(xml_file):
    return xml_file.getroot()
