# -*- coding: utf-8 -*-

def scrape_directory(path, flag, recursive=True):
    '''
    Parses contents of provided path, returns list of instances where an item
    within the provided path has an extension matching the string provided
    as "flag".
    
    By default, performs recursive search on all subdirectories of "path". Can
    be disabled by setting kwd "recursive" to False.
    '''
    import os
    catalog = []
    dir_dump = os.listdir(path)
    for item in dir_dump:
        fullname = os.path.join(path, item)
        if os.path.isfile(fullname):
            catalog.append(fullname)
        elif os.path.isdir(fullname):
            if recursive:
                contents = scrape_directory(fullname, flag)
                for entry in contents:
                    catalog.append(entry)
            else:
                pass
        else:
            pass
    returned_files = []
    for item in catalog:
        split_item = item.split('.')
        try:
            if split_item[1] == flag:
                returned_files.append(item)
        except IndexError:
            continue
    return returned_files