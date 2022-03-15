# -*- coding: utf-8 -*-
"""
A catch-all for various functions helpful in a wide number of applications, or
that I've found myself reproducing in a variety of other projects.

@author: Tyler King

Trans rights are human rights.
"""



def scrape_directory(path, flag, recursive=True):
    '''
    Parses contents of provided path, returns list of instances where an item
    within the provided path has an extension matching the string provided
    as "flag".

    By default, performs recursive search on all subdirectories of "path". Can
    be disabled by setting kwd "recursive" to False.

    The special value "*" can be used as a wildcard to list all files,
    regardless of their extension.

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
    if flag is not '*':
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
    else: returned_files = catalog
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

def find_nearest_member(container, query, truncate=False):
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
    c_min = min(container)
    c_max = max(container)
    if truncate:
        if query > c_max or query < c_min:
            raise ValueError('Query is not within range of container.')
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
    import numpy as np
    x1, y1 = a
    x2, y2 = b
    distance = np.sqrt((x2-x1)**2+(y2-y1)**2)
    return distance

def fit_distribution(x, y, p, dist='gaussian'):
    '''
    Fit a statistical distribution to data y using initial guess parameters p
    '''
    from scipy.optimize import curve_fit
    from scipy import exp
    import numpy as np

    def _gaussian_(x, a, x0, sigma):
        '''
        In probability theory, the normal (or Gaussian or Gauss or Laplace–Gauss)
        distribution is a very common continuous probability distribution. Normal
        distributions are important in statistics and are often used in the
        natural and social sciences to represent real-valued random variables
        whose distributions are not known. A random variable with a Gaussian
        distribution is said to be normally distributed and is called a normal deviate.
        '''
        return a*exp(-(x-x0)**2/(2*sigma**2))
    def _laplace_(x, a, mu, sigma):
        '''
        In probability theory and statistics, the Laplace distribution is a
        continuous probability distribution named after Pierre-Simon Laplace.
        It is also sometimes called the double exponential distribution, because
        it can be thought of as two exponential distributions (with an additional
        location parameter) spliced together back-to-back, although the term is
        also sometimes used to refer to the Gumbel distribution. The difference
        between two independent identically distributed exponential random
        variables is governed by a Laplace distribution, as is a Brownian motion
        evaluated at an exponentially distributed random time. Increments of
        Laplace motion or a variance gamma process evaluated over the time scale
        also have a Laplace distribution.
        '''
        return a*(np.exp(-(np.abs(x-mu))/sigma)/(2*sigma))
    def _cauchy_(x, a, x0, hwhm):
        '''
        The Cauchy distribution, named after Augustin Cauchy, is a continuous
        probability distribution. It is also known, especially among physicists,
        as the Lorentz distribution (after Hendrik Lorentz), Cauchy–Lorentz
        distribution, Lorentz(ian) function, or Breit–Wigner distribution. The
        Cauchy distribution is the distribution of the x-intercept of a ray
        issuing from (x0, hwhm) with a uniformly distributed angle. It is also
        the distribution of the ratio of two independent normally distributed
        random variables if the denominator distribution has mean zero.
        '''
        return a*((hwhm**2 / ((x-x0)**2 + hwhm**2))*(1/x0/np.pi))

    dist_options = set(['gaussian', 'laplace', 'cauchy'])
    if dist in dist_options:
        if dist.upper() == 'GAUSSIAN':
            popt, pcov = curve_fit(_gaussian_, x, y, p)
            fitted = np.array([_gaussian_(i,p[0],p[1],p[2]) for i in x])
        elif dist.upper() == 'LAPLACE':
            popt, pcov = curve_fit(_laplace_, x, y, p)
            fitted = np.array([_laplace_(i,p[0],p[1],p[2]) for i in x])
        elif dist.upper() == 'CAUCHY':
            popt, pcov = curve_fit(_cauchy_, x, y, p)
            fitted = np.array([_cauchy_(i,p[0],p[1],p[2]) for i in x])
        else:
            raise KeyError('Selected distribution is not a valid option.')
            fitted = popt = None
    else: fitted = popt = None
    return fitted, popt

def find_quartiles(data):
    '''
    Analyzes 1D array to identify statistical quartiles, as well as associated
    ranges and outliers.
    '''
    import numpy as np
    data = list(data)
    data.sort()
    data = np.array(data)
    second = np.median(data)
    lower = data[np.where(data<=second)]
    upper = data[np.where(data>=second)]
    first = np.median(lower)
    third = np.median(upper)
    quartiles = (first, second, third)
    iqr = third-first
    upper_cutoff = third + 1.5*iqr
    lower_cutoff = first - 1.5*iqr
    whiskers = []
    whiskers.append(data[np.where(data>=lower_cutoff)][0])
    whiskers.append(data[np.where(data<=upper_cutoff)][-1])
    whiskers = tuple(whiskers)
    outliers = 0
    outliers += len(data[np.where(data<lower_cutoff)])
    outliers += len(data[np.where(data>upper_cutoff)])
    return quartiles, whiskers, outliers

def time_function(f, *args, **kwds):
    import time
    t0 = time.time()
    output = f(*args, **kwds)
    return time.time() - t0

def apply_polynomial(x, c):
    '''
    Applies nth order polynomial to input array x. n is equal to len(c) - 1.

    when c = (1, -2, 3), function is equivalent to:
        f(x) = 3*x**2 - 2*x + 1

    Input:
    --------
        x : array-like
            data to be evaluated with polynomial
        c : array-like
            polynomial coefficients in ascending polynomial order
    '''
    import numpy as np
    x = np.asarray(x)
    y = np.empty_like(x, dtype=np.float64)
    for i, xi in enumerate(x):
        y_i = 0
        for idx, coeff in enumerate(np.flip(c)):
            y_i += (xi**idx)*coeff
        y[i] = y_i
    return y

def downsample_2d(array, target_resolution):
    import numpy as np
    initial_shape = array.shape
    d_array = np.empty(shape=target_resolution, dtype=np.float32)
    resample_axes = np.array([np.linspace(0, initial_shape[i], target_resolution[i]+1) for i in range(2)], dtype=int)
    x = list(range(initial_shape[0]))
    y = list(range(initial_shape[1]))
    for i, row in enumerate(d_array):
        for j, pixel in enumerate(row):
            mask = ((resample_axes[0, i], resample_axes[0, i+1]),(resample_axes[1, j], resample_axes[1, j+1]))
            window = array[mask[0][0]:mask[0][1], mask[1][0]:mask[1][1]]
            d_array[i,j] = np.mean(window)

    return d_array
    return d_array

def proxy_sort(template, data, reverse=False):
    import numpy as np
    order = np.argsort(template)
    sorted_data = []
    for i in order:
        sorted_data.append(data[i])
    if reverse:
        sorted_data.reverse()
    return sorted_data

def scatter3d(data_array, fname, labels=None):

    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import imageio
    import os
    import matplotlib.pyplot as plt

    if labels is None:
        labels = np.zeros((data_array.shape[0]))

    x = np.array([d[0] for d in data_array])
    y = np.array([d[1] for d in data_array])
    z = np.array([d[2] for d in data_array])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, marker='o',c=labels, alpha=0.2)

    images = []
    for angle in range(0, 360):
        ax.view_init(30, angle)
        plt.draw()
        plt.savefig('.kscatter_temp.png')
        im = imageio.imread('.kscatter_temp.png')
        images.append(im)
        os.remove('.kscatter_temp.png')

    imageio.mimwrite(fname, images, format='gif')
    plt.close()
    return

element_mass_lookup_table = {
    'H':1.00797,'He':4.0026,'Li':6.941,'Be':9.01218,'B':10.81,'C':12.011,
    'N':14.0067,'O':15.9994,'F':18.998403,'Ne':20.179,'Na':22.98977,
    'Mg':24.305,'Al':26.98154,'Si':28.0855,'P':30.97376,'S':32.06,
    'Cl':35.453,'K':39.0983,'Ar':39.948,'Ca':40.08,'Sc':44.9559,
    'Ti':47.9,'V':50.9415,'Cr':51.996,'Mn':54.938,'Fe':55.847,'Ni':58.7,
    'Co':58.9332,'Cu':63.546,'Zn':65.38,'Ga':69.72,'Ge':72.59,
    'As':74.9216,'Se':78.96,'Br':79.904,'Kr':83.8,'Rb':85.4678,
    'Sr':87.62,'Y':88.9059,'Zr':91.22,'Nb':92.9064,'Mo':95.94,
    'Tc':98,'Ru':101.07,'Rh':102.9055,'Pd':106.4,'Ag':107.868,
    'Cd':112.41,'In':114.82,'Sn':118.69,'Sb':121.75,'I':126.9045,
    'Te':127.6,'Xe':131.3,'Cs':132.9054,'Ba':137.33,'La':138.9055,
    'Ce':140.12,'Pr':140.9077,'Nd':144.24,'Pm':145,'Sm':150.4,
    'Eu':151.96,'Gd':157.25,'Tb':158.9254,'Dy':162.5,'Ho':164.9304,
    'Er':167.26,'Tm':168.9342,'Yb':173.04,'Lu':174.967,'Hf':178.49,
    'Ta':180.9479,'W':183.85,'Re':186.207,'Os':190.2,'Ir':192.22,
    'Pt':195.09,'Au':196.9665,'Hg':200.59,'Tl':204.37,'Pb':207.2,
    'Bi':208.9804,'Po':209,'At':210,'Rn':222,'Fr':223,'Ra':226.0254,
    'Ac':227.0278,'Pa':231.0359,'Th':232.0381,'Np':237.0482,
    'U':238.029,'Pu':242,'Am':243,'Bk':247,'Cm':247,'No':250,'Cf':251,
    'Es':252,'Hs':255,'Mt':278,'Fm':257,'Md':258,'Lr':266,'Rf':267,
    'Bh':270,'Db':268,'Sg':269,'Ds':281,'Rg':282,'Cn':285,'Nh':286,
    'Fl':289,'Mc':290,'Lv':293,'Ts':294,'Og':294
    }

def r_squared(measured, predicted):
    import numpy as np
    corr = np.corrcoef(measured, predicted)[0,1]
    return corr ** 2

def liveplot(x, y, q=1, length=60, fname='liveplot.gif', figsize=(6,4)):
    import numpy as np
    import os
    import matplotlib.pyplot as plt
    from PIL import Image
    
    xmin = x[0]/3600
    xbounds = (0, (x[-1]/3600) - xmin)
    ybounds = (min(y), max(y))
    yrange = ybounds[1] - ybounds[0]
    ybounds = (ybounds[0]-(yrange*0.1), ybounds[1]+(yrange*0.1))
    images = []
    counter = 1
    tempnames = []
    for i in range(len(x)):
        if i%q != 0:
            continue
        xi = (np.array(x[:i]) / 3600) - xmin
        yi = np.array(y[:i])
        plt.figure(figsize=figsize)
        plt.xlim(xbounds[0],xbounds[1])
        plt.ylim(ybounds[0],ybounds[1])
        plt.plot(xi,yi)
        plt.xlabel('Time (hours)')
        plt.ylabel('Potential (V)')
        tempname = f'temp_{counter}.png'
        plt.savefig(tempname)
        plt.close()
        tempnames.append(tempname)
        counter += 1
    for tempname in tempnames:
        images.append(Image.open(tempname))
    nframes = len(images)
    length = (length*1000/nframes)
    images[0].save(fname, save_all=True, append_images=images[1:], duration=length, loop=1)
    
    for tempname in tempnames:
        os.remove(tempname)
    return