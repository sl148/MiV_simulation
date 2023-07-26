
import numpy as np
import coordinatorClass
import sys



num_stacks = 6
seed = 31163221
basefile_name = f'/home/lee/parasol/multi-robot-experiments/gantry_stack/stacks_{num_stacks}/'
data_gantry = np.loadtxt(basefile_name+f'NBS-{seed}::FinalPath::gantry_0')

meaData = {}
lidData = {}
garageData = {}
robotData = {}


for n in range(1):
    robot_data_path = basefile_name+f'NBS-{seed}::FinalPath::'+'gantry_'+str(n)
    data = np.loadtxt(robot_data_path)
    offset = np.ones((len(data),1))*-0.05
    print(np.shape(data), np.shape(offset))
    data[:,-1] += offset.flatten()
    robotData['gantry_'+str(n)] = data 
    

for n in range(num_stacks):
    mea_data_path = basefile_name+f'NBS-{seed}::FinalPath::'+'mea_'+str(n)
    data = np.loadtxt(mea_data_path)
    y_offset = np.ones((len(data),1))*-0.2
    z_offset = np.ones((len(data),1))*-0.72
    data[:,1] += y_offset.flatten()
    data[:,2] += z_offset.flatten()
    meaData['mea_'+str(n)] = data

for n in range(num_stacks):
    lid_data_path = basefile_name+f'NBS-{seed}::FinalPath::'+'lid_'+str(n)
    data = np.loadtxt(lid_data_path)
    y_offset = np.ones((len(data),1))*-0.2
    z_offset = np.ones((len(data),1))*-0.72
    data[:,1] += y_offset.flatten()
    data[:,2] += z_offset.flatten()
    lidData['lid_'+str(n)] = data

garageData['garage'] = np.array([[-0.12, -0.32, 0.03]])

l = max([len(meaData[key]) for key in meaData.keys()]\
            +[len(lidData[key]) for key in lidData.keys()]\
                +[len(robotData[key]) for key in robotData.keys()])
print(l)

## Gantry
for key in robotData.keys():
    print(l-len(robotData[key]))
    for i in range(l-len(robotData[key])):
        robotData[key] = np.vstack((robotData[key],robotData[key][-1,:]))
    print(key, len(robotData[key]))

# Add blocks
for key in meaData.keys():
    print(l-len(meaData[key]))
    for i in range(l-len(meaData[key])):
        meaData[key] = np.vstack((meaData[key],meaData[key][-1,:]))
    print(key, len(meaData[key]))

for key in lidData.keys():
    print(l-len(lidData[key]))
    for i in range(l-len(lidData[key])):
        lidData[key] = np.vstack((lidData[key],lidData[key][-1,:]))
    print(key, len(lidData[key]))

for key in garageData.keys():
    print(l-len(garageData[key]))
    for i in range(l-len(garageData[key])):
        garageData[key] = np.vstack((garageData[key],garageData[key][-1,:]))
    print(key, len(garageData[key]))


coordinator = coordinatorClass.Coordinator(robotData, meaData, lidData, garageData)

def main():
    # for key in meaData.keys():

    # for key in lidData.keys():

    # for key in robotData.keys():
    #     robot.execute_plan(robotData[key],60)
    coordinator.spawn_objects()
    coordinator.execute_plan(num_stacks*5)
    

if __name__ == '__main__':
    main()
    

