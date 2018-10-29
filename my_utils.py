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
    #Dump all contents of path into temporary container
    dir_dump = os.listdir(path)         
    #Iterate through temporary container, categorize contents as files or directories
    for item in dir_dump:
        fullname = os.path.join(path, item)
        #If item is a file, append the absolute filename to catalog
        if os.path.isfile(fullname):
            catalog.append(fullname)
        #If item is a subdirectory...
        elif os.path.isdir(fullname):
            #If recursive mode is enabled, recursively calls scrape_directory to read and categorize contents
            if recursive:
                contents = scrape_directory(fullname, flag)
                for entry in contents:
                    catalog.append(entry)
            #If recursive mode is disabled, passes over subdirectory
            else:
                pass
        else:
            pass
    returned_files = []
    #Iterate through items identified as files
    for item in catalog:
        #Split item to extract file extension
        split_item = item.split('.')
        try:
            #If extracted extension matches flag, append item to list of items to be returned
            if split_item[1] == flag:
                returned_files.append(item)
        #If item has no associated extension, pass over item
        except IndexError:
            continue
    return returned_files