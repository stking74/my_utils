# -*- coding: utf-8 -*-

def scrape_directory(path, flag, recursive=True):
    '''
    Parses contents of provided path, returns list of instances where an item
    within the provided path has an extension matching the string provided
    as "flag".
    
    By default, performs recursive search on all subdirectories of "path". Can
    be disabled by setting kwd "recursive" to False.
    
    Input:
    --------
    path : str
        Directory to be scraped
    flag : str
        Flag to identify directory contents to be returned
    recursive : bool
        If true, subdirectories of path are also scraped, results returned with root (default recursive=True)
    
    Output:
    --------
    returned_files : list of str
        Contents of path which matched flag
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

def soft_append(container, addendum):
    '''
    Appends addendum item to container only if addendum is not already member
    of container. Returns nothing, since container is appended in-place.
    
    Input:
    --------
    container : list
        container object to be appended
    addendum : any
        value to be soft-appended to container
    '''
    if addendum not in container:
        container.append(addendum)
        return
    return

def find_nearest_member(container, query):
    '''
    Finds the member of a container whose value is nearest to query. Returns
    index of nearest value within container. Intended to be used when 
    list.index(query) is, for whatever reason, not a viable option for locating
    the desired value within the container.
    
    Input:
    --------
    container : container variable (eg list, tuple, set, Numpy array)
        The container to be searched by the function
    query : number (eg int or float)
        Value to be searched for within container
        
    Output:
    --------
    mindex : int
        Index of item in container whose value most nearly matches query
    '''
    try:
        diffs = abs(container - query)
    except:
        diffs = []
        for entry in container:
            difference = entry - query
            diffs.append(abs(difference))
    minimum = min(diffs)
    mindex = list(diffs).index(minimum)
    return mindex

def progress_counter(i, interval, end):
    if abs(i) > 0 and i % 1000 == 0:
        print('%i / %i'%(i,end))
    return


    