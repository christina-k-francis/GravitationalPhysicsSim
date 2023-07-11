# script for running the gravitational physics simulator


# Original G is 6.6742*10**-11
# So if our units are in the millions
G = 6.6742 * 10 ** -5


# CALCULATIONS
def distance_calc(s1,s2):
    '''s1 and s2 are coordinate pairs (x1, y1) and (x2, y2)'''
    dist = math.sqrt(((s1[0]-s2[0])**2 + (s1[1]-s2[1])**2))
    return dist

def force_calc(m1,m2,s):
    '''m1 is mass of first object, m2 is mass of second object, s is distance between'''
    return (G * m1 * m2) / s**2

def angle_calc(vec1, vec2):
    '''Given vec1 and vec2 vectors like: (x1, y1) and (x2, y2)'''
    return math.atan2(vec2[1] - vec1[1], vec2[0] - vec1[0])

def forceVec(vec1, vec2):
    '''Calculate the force vector between vec1 and vec2, where vec1 and vec2 are like [x, y, mass, velx, vely]
    The force vector should be of the form [Fx, Fy]
    '''
    m1 = vec1[2]
    m2 = vec2[2]
    s = distance_calc(vec1[0:2], vec2[0:2])
    force = force_calc(m1,m2,s)
    angle = angle_calc(vec1,vec2)
    Fx = force*(math.cos(angle))
    Fy = force*(math.sin(angle))
    return (Fx,Fy)

def exp(a,n):
    '''return the value of a^n implemented recursively'''
    if n == 0:
        return 1
    if n < 0:
        exp_arr = np.empty([abs(n)])  
        exp_arr.fill(a)
        return (1/np.prod(exp_arr))
    else:
        return a * exp(a,n-1)
        
def perms(v):
    ''' prints a list of all permutations of v. You can assume v is a list or a string'''
    no_comb = fact(len(v)) # all potential combinations
    combos = [] # this should ultimately have len == no_comb
    elmts_pos = np.arange(len(v)) # the position of v elements
    pot_arrangements = [] # all potential arrangements of v elements
    while len(combos) != no_comb:
        temp_combo = []
        temp = random.sample(list(elmts_pos), len(elmts_pos)) # random arrangement of the position of v elements
        if (temp in pot_arrangements) == False:
            pot_arrangements.append(temp)
            for y in range(len(v)):
                temp_combo.append(v[temp[y]]) # new combination of v
            combos.append(temp_combo)
        if (temp in pot_arrangements) == True:
            if len(combos) == no_comb:
                print(combos,  '%s permutations' %(no_comb))    
            else:
                continue
    
def fact(n):
    ''' returns the factorial of positive integers'''
    if n == 1:
        return n
    else:
        return n*fact(n-1)
      
def isPalindrome(w):
    '''given a string w, return True if it is a palindrome, otherwise return False, recursively'''
    if len(w) == 0:
        return True
    if len(w) == 1:
        return True
    if w[0] != w[-1]:
        return False
    if w[0] == w[-1]:
        return isPalindrome(w[1:-1])
    
def sumOfForces(objects):
    '''Given an Nx5 array of objects of the form (x, y, mass, xvel, yvel), return an Nx2 array of the cumulative force acting on each object in x and y
    returns Nx(sumFx, sumFy)'''
    N = objects.shape[0] # number of objects
    objects_forceSum = []
    for prim_obj in range(N): # prim_obj = primary object
        XforceSum = 0
        YforceSum = 0
        for other_obj in range(N): # other_onj = non_primary objects
            if (objects[prim_obj] == objects[other_obj]).all(): 
                continue
            else:
                Fx,Fy = forceVec(objects[prim_obj], objects[other_obj])
                XforceSum += Fx
                YforceSum += Fy
        objects_forceSum.append([XforceSum,YforceSum])
    objects_forceSum = np.array(objects_forceSum)
    return(objects_forceSum)

def nextPositionAndVelocity(vec, forcevec, delta_t):
    '''Calculate the next velocity and position of vector based on the forces acting on it
    delta_t is in seconds
    Returns [new positionx, new positiony, mass, newvelocityx, newvelocityy]
    '''
    # x-axis calculations
    new_velx = vec[-2] + (forcevec[0]/vec[2])*delta_t
    new_posx = vec[0] + (vec[-2]*delta_t)
    # y-axis calculations
    new_vely = vec[-1] + (forcevec[1]/vec[2])*delta_t
    new_posy = vec[1] + (vec[-1]*delta_t)
    return np.array([new_posx, new_posy, vec[2], new_velx, new_vely])
    
# DATA
# # edited generateObjects for hw5
def generateObjects(count, center=0, width=10, massmult=100, vcenter=0, vwidth=10):
    '''Generate a `count` x 5 matrix of (x, y) coordinates corresponding
    to `count` the number of arbitrarly placed elements
    
    Args:
        count (int): the number of (x, y) pairs to generate
        center (float): the center of our distribution
        width (float): the width of our distribution
        massmult (float): mass multiplier
        vcenter (float): the center of our velocity distribution
        vwidth (float): the width of our velocity distribution

    Returns:
        a (`count`, 5) array/list of positions

        The return value should look like:
            [[x1, y1, mass1, velocityx1, velocityy1],
             [x2, y2, mass2, velocityx2, velocityy2],
             ...
            ]
    '''
    coords = np.random.normal(center,width,(count,2))
    mass_values = np.random.ranf(count)*massmult
    vel = np.random.normal(vcenter,vwidth,(count,2))
    return(np.column_stack((coords,mass_values,vel)))


def generateObjectsNormal(count, center=0, width=10, massmult=100):
    ''' Creating a 2-d bell curve of (x,y,mass) matrix '''
    return np.random.multivariate_normal([center, center, massmult],
                                         [[width/2, 0, 0],
                                          [0, width/2, 0],
                                          [0, 0, massmult*10]],
                                         count).tolist()

# PLOTTING
def plotObjects(objects):
    '''Draw a matplotlib chart of our
    objects. `objects` argument is an Nx3 matrix of (x,y,mass) coordinates'''
    plt.figure(figsize=(5,4))
    plt.scatter(objects[:,0],objects[:,1], s=objects[:,2], alpha=0.75,
                c=np.arange(len(objects)), cmap='nipy_spectral')
    plt.show()
      

# EXECUTION
def main(t_delta=2):
    count = int(input("how many objects should we generate?"))
    objects = generateObjects(count)
    plotObjects(objects)
    # calculating the sum of forces on all objects
    forces_sum = sumOfForces(objects)
    objects_new = []
    for obj in range(count):
        output = nextPositionAndVelocity(objects[obj], forces_sum[obj], t_delta)
        objects_new.append(output)
    plotObjects(np.array(objects_new))
    keep_going = input("calculate next position? y/n")
    while keep_going == 'y':
        forces_sum = sumOfForces(np.array(objects_new))
        objects_old = copy.deepcopy(objects_new)
        objects_new = []
        for obj in range(count):
            output = nextPositionAndVelocity(objects_old[obj], forces_sum[obj], t_delta)
            objects_new.append(output)
        plotObjects(np.array(objects_new))
        keep_going = input("calculate next position? y/n")
