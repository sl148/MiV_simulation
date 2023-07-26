from spatialmath import SE3
from roboticstoolbox.models.DH import Panda
from roboticstoolbox import DHRobot
from roboticstoolbox.tools import ctraj,jtraj
import numpy as np
import os
import time

class Coordinator():
    def __init__(self,dataGantry, dataLid, dataMea, garageData, q0 = None):
        super().__init__()
        
        if(q0 == None):
            self.q0 = [0.]*5
        else:
            self.q0 = q0
        self.q = self.q0
        self.p = self.fk_pos(self.q)
        
        self.set_q(self.q,1)

        self.dataGantry = dataGantry
        self.dataLid = dataLid
        self.dataMea = dataMea
        self.garageData = garageData

    def spawn_objects(self):
        for key in self.dataLid.keys():
            initPos = self.dataLid[key][0,:3]
            print(key, initPos)
            os.system(f"ros2 run gantry_test spawn_object {key} {key} {initPos[0]} {initPos[1]} {initPos[2]}")

        for key in self.dataMea.keys():
            initPos = self.dataMea[key][0,:3]
            print(key, initPos)
            os.system(f"ros2 run gantry_test spawn_object {key} {key} {initPos[0]} {initPos[1]} {initPos[2]}")

        for key in self.garageData.keys():
            initPos = self.garageData[key][0,:3]
            print(key, initPos)
            os.system(f"ros2 run gantry_test spawn_object {key} {key} {initPos[0]} {initPos[1]} {initPos[2]}")


    def fk_pos(self, q):
        p = [0., 0., 0.]
        p[0] = q[2]
        p[1] = q[3]
        p[2] = q[4]
        return p
    
    def string_q(self, q):
        s=''
        for value in q:
            s+=str(value)+' '
        return s
    
    def string_gantry_qs(self, qs):
        s=''
        for q in qs:
            q_filtered = q[2:]
            for value in q_filtered:
                s+=str(value)+' '
        return s

    def string_object_qs(self, qs):
        s=''
        for q in qs:
            q_filtered = q[:3]
            for value in q_filtered:
                s+=str(value)+' '
        return s

    def execute_plan(self,t): # t is the time duration we want  
        for key in self.dataGantry.keys():
            cfgPlan = self.dataGantry[key]
            n = len(cfgPlan)
            print("cfg plan length: ", n)
            dt = t/n
            os.system(f'ros2 run gantry_test multi_point_controller {n} {int(dt*1e9)} {self.string_gantry_qs(cfgPlan)}')
        
        # print("Now planning lid")
        # for key in self.dataLid.keys():
        #     data = self.dataLid[key]
        #     for i in range(len(data)):
        #         n = len(data)*3
        #         dt = t/n
        #         tic = time.time()
        #         print(data[i])
        #         cmd = 'ros2 service call /gazebo/set_entity_state gazebo_msgs/SetEntityState ' \
        #                 + '"state: {name: ' + str(key) + ', pose: {position: {x: ' \
        #                     + str(data[i][1]) + ", y: " + str(-data[i][0]) + ", z: " + str(data[i][2]-0.72) + '}}, reference_frame: world}"'
        #         os.system(cmd)
        
    def set_q(self, q, t):
        os.system(f'ros2 run chess_manipulator multi_point_controller 1 {int(t*1e9)} {self.string_q(q)} ')        
            
if __name__ == '__main__':
    robot = Coordinator()

