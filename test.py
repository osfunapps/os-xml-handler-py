from os_xml_handler import xml_handler as xh

# groups_dir = '/Users/home/Desktop/work/Apps/groups'
# group_dir_list = fh.get_dir_content(groups_dir, True, False, True)
# print(group_dir_list)

xml1 = xh.read_xml_file('/Users/home/Desktop/bv/xml1.xml')
root = xh.get_root_node(xml1)
holder = xh.get_root_direct_child_nodes(xml1, 'holder')[0]
next_dhdren = xh.get_all_direct_child_nodes(holder, False)
print(next_dhdren)



# xml2 = xml_handler.read_xml_file('/Users/home/Desktop/bv/xml2.xml')
#
# xml3 = xml_handler.merge_xml1_with_xml2(xml1, xml2)
# xml_handler.save_xml_file(xml3, '/Users/home/Desktop/bv/xml3.xml')
#
# files = fh.search_files('/Users/home/Programming/android/coroutine/rwdc-coroutines-materials/starter/app/src/main/res', by_extension='.xml')
# content = fh.get_dir_content("/Users/home/Desktop/apps", False, True, False)
# print(files)

# print(content)
