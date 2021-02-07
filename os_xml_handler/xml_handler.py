from lxml import etree


#########################################################################
# this module aim to provide intuitive functions to work with xml files #
#########################################################################


# will return a list of nodes specified by an attribute key and an attribute value from a parent node
def get_child_nodes(node_parent, node_tag, node_att_name=None, node_att_val=None, namespace_map=None, filter_comment_nodes=True):
    selector = node_tag
    return find_all_nodes(node_parent, node_tag, node_att_name, node_att_val, recursive=False, namespace_map=namespace_map, filter_comment_nodes=filter_comment_nodes)


# will search in all of the direct children of the root
def get_root_direct_child_nodes(xml_file, node_tag, node_att_name=None, node_att_val=None, namespace_map=None, filter_comment_nodes=True):
    return get_child_nodes(get_root_node(xml_file), node_tag, node_att_name, node_att_val, namespace_map, filter_comment_nodes)


# will return a list of nodes which doesn't have a specific attribute
def get_nodes_from_xml_without_att(xml_file, node_tag, node_att_name=None, namespace_map=None, filter_comment_nodes=True):
    root = xml_file.getroot()
    relevant_nodes = []
    node_att_name = _sanitize_att_name(node_att_name, namespace_map)
    nodes = root.findall(node_tag)
    for node in nodes:
        if get_node_att(node, node_att_name) is None:
            relevant_nodes.append(node)
    if filter_comment_nodes:
        relevant_nodes = filter_comments(relevant_nodes)
    return relevant_nodes


# will remove any comment nodes from a node list
def filter_comments(node_list):
    res = []
    for node in node_list:
        if not is_comment_node(node):
            res.append(node)
    return res


# will check if a node is a comment node
def is_comment_node(node):
    return type(node) is etree._Comment


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
def get_all_direct_child_nodes(node, filter_comment_nodes=True):
    nodes = list(node)
    if filter_comment_nodes:
        return filter_comments(nodes)
    return nodes


# will return the text (inner html) of a given node
def get_text_from_node(node):
    text = node.text
    if text == '\n        ':
        return None
    return node.text


# will return the text from a child node, using the parent node.
# NOTICE: this function will not crash but return None if the node isn't exists
def get_text_from_child_node(parent_node, child_node_tag, child_node_att_name=None, child_node_att_val=None):
    child_nodes = get_child_nodes(parent_node, child_node_tag, child_node_att_name, child_node_att_val)
    if child_nodes:
        return get_text_from_node(child_nodes[0])
    else:
        return None


# will set the text (inner html) in a given node
def set_node_text(node, text):
    node.text = text


# will return the value of a given att from a desired node
def get_node_att(node, att_name, namespace_map=None):
    att_name = _sanitize_att_name(att_name, namespace_map)
    return node.get(att_name)


# will read and return an xml file.
# added a custom parser to prevent the commends from being removed
def read_xml_file(xml_path, namespace_dict=None, remove_comments=False):
    parser = etree.XMLParser(remove_comments=remove_comments)
    tree = etree.parse(xml_path, parser=parser)
    etree.set_default_parser(parser)
    if namespace_dict:
        for prefix, uri in namespace_dict.items():
            etree.register_namespace(prefix, uri)
    return tree


# will save the changes made in an xml file
def save_xml_file(xml_file, xml_path, add_utf_8_encoding=False):
    if add_utf_8_encoding:
        xml_file.write(xml_path, encoding="UTF-8")
    else:
        xml_file.write(xml_path)


# will create an xml file
def create_xml_file(root_node_tag, output_file):
    xml = etree.Element(root_node_tag)
    tree = etree.ElementTree(xml)

    # create dir if not exists
    from os_file_handler import file_handler
    parent_dir = file_handler.get_parent_path(output_file)
    if not file_handler.is_dir_exists(parent_dir):
        file_handler.create_dir(parent_dir)

    save_xml_file(tree, output_file)
    # tree = read_xml_file(output_file)   # maybe to read the xml again, to prevent the comments from being removed?
    return tree


# will add a node to a relative location
def create_and_add_new_node(parent_node, node_tag, att_val_dict=None, node_text=None, namespace_map=None):
    if att_val_dict is None:
        att_val_dict = {}
    if att_val_dict is not None and namespace_map is not None:
        node_att_val_dict = {}
        for key, val in att_val_dict.items():
            node_att_val_dict[_sanitize_att_name(key, namespace_map)] = val
        att_val_dict = node_att_val_dict

    node = etree.SubElement(parent_node, node_tag, att_val_dict)
    if node_text is not None:
        set_node_text(node, node_text)
    return node


# will add an existing node to a parent node
def add_node(parent_node, child_node):
    direct_children = get_all_direct_child_nodes(parent_node)
    location = 0
    if direct_children:
        location = len(direct_children)
    parent_node.insert(location, child_node)


# will add a bunch of already existing nodes to a parent node
def add_nodes(parent_node, child_nodes):
    for child_node in child_nodes:
        add_node(parent_node, child_node)


# will merge xml1 with xml2 and return a new xml comprising both of them.
# NOTICE: this function will compare the direct root child nodes and merge/append them.
def merge_xml1_with_xml2(xml1, xml2):
    xml1_root = get_root_node(xml1)
    xml1_direct_children = get_all_direct_child_nodes(xml1_root)
    for xml2_child in get_all_direct_child_nodes(get_root_node(xml2)):
        parent_node = None
        for xml1_child in xml1_direct_children:
            # if the direct child already exists, add the appended tag content to the existing one
            if xml2_child.tag == xml1_child.tag:
                parent_node = xml1_child
                break

        if parent_node is not None:
            xml2_direct_children = get_all_direct_child_nodes(xml2_child)
            if len(xml2_direct_children) > 0:
                add_nodes(parent_node, xml2_direct_children)
            else:
                # if reached here, it means that only the text is resembled
                set_node_text(parent_node, f'{get_text_from_node(parent_node)}\n{get_text_from_node(xml2_child)}')
        else:
            add_node(xml1_root, xml2_child)

    return xml1


# Will turn a simple dictionary to an xml file, by hierarchical order
def simple_dict_to_xml(xml_dict, root_name, output_path, namespace_map=None):
    # will unpack the parent recursively
    def recursive_unpack_parent(parent_dict, parent=None):
        for key, val in parent_dict.items():
            parent = create_and_add_new_node(parent, xml, key, namespace_map=namespace_map)
            if type(val) is dict:
                recursive_unpack_parent(val, parent)

    xml = create_xml_file(root_name, output_path)
    recursive_unpack_parent(xml_dict)
    save_xml_file(xml, output_path)


def get_root_node(xml_file):
    return xml_file.getroot()


# will add attribute to a given node.
# If adding a namespace map, add, for example {'android', 'http://schemas.android.com/apk/res/android'}. The keys should be normal. Like: {"android:value": xxxx}
def set_node_atts(node, atts_dict, namespace_map=None):
    for key, val in atts_dict.items():
        key = _sanitize_att_name(key, namespace_map)
        node.set(key, val)


# will search for a node
def find_all_nodes(parent_node, node_tag, node_att_name=None, node_att_val=None, recursive=True, namespace_map=None, filter_comment_nodes=True):
    selector = node_tag
    if node_att_name is not None:
        node_att_name = _sanitize_att_name(node_att_name, namespace_map)
        if node_att_val is not None:
            selector = node_tag + "/[@" + node_att_name + "='" + node_att_val + "']"
        else:
            selector = node_tag + "/[@" + node_att_name + "]"
    if recursive:
        nodes = parent_node.findall(f'.//{selector}')
    else:
        nodes = parent_node.findall(selector, namespace_map)
    if filter_comment_nodes:
        return filter_comments(nodes)
    return nodes


# will parse the namespace, as required, in the att_name
def _sanitize_att_name(att_name, namespace_map):
    if namespace_map is not None:
        for prefix, uri in namespace_map.items():
            if prefix in att_name:
                att_name = '{' + str(att_name).replace(':', '}').replace(prefix, uri)
                break
    return att_name
