import matplotlib.pyplot as plt

def plotObjects(objects):
    '''Draw a matplotlib chart of our
    objects. `objects` argument is an Nx3 matrix of (x,y,mass) coordinates'''
    plt.figure(figsize=(5,4))
    plt.scatter(objects[:,0],objects[:,1], s=objects[:,2], alpha=0.75,
                c=np.arange(len(objects)), cmap='nipy_spectral')
    plt.show()
    
