import sys
import threading 
import time,schedule
import random

from opcua import ua, Server

class Opcua(threading.Thread):
    def __init__(self,num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        
        server,idx,Myobj = self.CreateServer(self.num)
        
        Dice_NO = Myobj.add_variable( idx , "Dice_NO" , 1500, ua.VariantType.Int32 )
        Dice_NO.set_read_only()    # Set MyVariable to be writable by clients

        User_NO = Myobj.add_variable( idx , "User_NO" , 0 , ua.VariantType.Int32 )
        User_NO.set_read_only()    # Set MyVariable to be writable by clients

        Time = Myobj.add_variable( idx , "Time" , 0 , ua.VariantType.Int32 )
        Time.set_read_only()    # Set MyVariable to be writable by clients

        server.start() # starting!
        try:
            startime = 0

            dice_number_list = ["1_dot","2_dot","3_dot","4_dot","5_dot","6_dot"]

            user_list = ["Joe","Clement","Jack","Devid"]


            while True:
                time.sleep(3)
                dice = random.choice(dice_number_list)
                Dice_NO.set_value(dice)
                user = random.choice(user_list)
                User_NO.set_value(user)
                Time.set_value(startime)
                startime+=1   

        finally:
            #close connection, remove subcsriptions, etc
            server.stop()    

    def CreateServer(self,num):
        print("num:",num)
        server= Server()
        server.set_endpoint("opc.tcp://0.0.0.0:"+str(4840+int(num)))
        # setup our own namespace, not really necessary but should as spec
        uri = "https://www.google.com"
        idx = server.register_namespace(uri)

        # get Objects node, this is where we should put our nodes
        objects = server.get_objects_node()

        # populating our address space
        Myobj = objects.add_object(idx, "Dice_NO")

        return server,idx,Myobj

    def timer(self):
        startTime=+1
OpcuaThreads = []
simulatorNumber = input('Please input threading number:')
for i in range(int(simulatorNumber)):
    OpcuaThreads.append(Opcua(i))
    OpcuaThreads[i].start()

for i in range(int(simulatorNumber)):
    OpcuaThreads[i].join()
    print("Done")    


