import os_xml_handler.file_handler as fh
groups_dir = '/Users/home/Desktop/work/Apps/groups'
group_dir_list = fh.get_dir_content(groups_dir, True, False, True)
print(group_dir_list)

#
# files = fh.search_files('/Users/home/Programming/android/coroutine/rwdc-coroutines-materials/starter/app/src/main/res', by_extension='.xml')
# content = fh.get_dir_content("/Users/home/Desktop/apps", False, True, False)
# print(files)

# print(content)

