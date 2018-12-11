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

def progress_counter(i, end, interval=None):
    '''
    Simple linear integer progress counter. To be called during every iteration
    of process being monitored/counted.'
    
    Input:
    --------
    i : int
        index of item being counted (ex. the counter output of an enumerator)
    end : int
        total number of items to be counted
    interval : int or None (optional)
        suppresses output if i is not a multiple of interval
    '''
    if abs(i) > 0 and i % 1000 == 0:
        print('%i / %i'%(i,end))
    return

def binning(container, n_bins, cores=None):
    '''
    Simple 1-dimensional binning algorithm. Reduces number of datapoints
    in a linear counting-style measurement, such that the input and output
    variables have the same integral.
    
    Input:
    --------
    container : list or numpy.array
        container object containing values to be binned
    n_bins : int
        number of bins in returned container
    cores : int
        number of cores to use for multiprocessing (planned feature)
        
    Output:
    --------
    new_container : numpy.array
        container object of length n_bins containing binned values
    '''
    import numpy as np
    ctype = type(container)
    if ctype == np.ndarray:
        old_shape = container.shape
        try:
            old_height, old_length = old_shape
            binned_container = np.empty(shape=(old_height,n_bins))
        except ValueError:
            old_length = old_shape[0]
            binned_container = np.empty(shape=n_bins)
    elif ctype == list or ctype == tuple:
        old_length = len(container)
        binned_container = np.empty(shape=n_bins)
    else:
        print('Incompaible container type.')
    container = np.array(container)
    old_indices = np.array(range(old_length))
    n_old_indices = old_indices/np.max(old_indices)
    new_indices = np.array(range(n_bins))
    n_new_indices = new_indices/np.max(new_indices)
    index_gap = (n_new_indices[1] - n_new_indices[0])/2
    new_container = np.empty(shape=(n_bins))
    for idx, n in enumerate(n_new_indices):
        window = np.where(abs(n_old_indices - n) < index_gap)
        old_values = container[window]
        new_container[idx] = np.sum(old_values)
    return new_container, n_new_indices

def cartesian_distance(a, b):
    '''
    Calculates the distance between two points within a cartesian coordinate plane
    
    Input:
    --------
        a : tuple or list
        First point to consider for distance calculation
        
        b : tuple or list
        Second point to consider for distance calculation
    
    Output:
    --------
        distance : float
        Distance between points a and b, expressed in the same units as the coordinates given for a and b
    '''
    x1, y1 = a
    x2, y2 = b
    distance = np.sqrt((x2-x1)**2+(y2-y1)**2)
    return distance