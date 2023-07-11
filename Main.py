# Function for running the gravitational physics simulator
from nbody.calculations import sumOfForces, nextPositionAndVelocity
from nbody.data import generateObjects
from nbody.plotting import plotObject

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
