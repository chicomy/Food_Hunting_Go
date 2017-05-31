__author__ = 'Chongmiw'
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #7: The Maze Decorator

import MalmoPython
import os
import sys
import time
import json
import math
import random
from collections import defaultdict
from timeit import default_timer as timer

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately


class Agent:
    def __init__(self, recepies, aim):
        self.aim = aim
        self.aimRecipy = recepies[aim]
        self.x = 0
        self.y = 0
        self.steps = 0
        self.action_trans = {1:"movenorth 1", 5:"moveeast 1", 3:"movewest 1", 7:"movesouth 1"}
        self.pos_tran = {'movewest 1':(1,0),  'movesouth 1':(0,1),  'moveeast 1':(-1,0), 'movenorth 1':(0,-1)}
        self.visited = set()
        self.trainResult = dict()
        self.inv = defaultdict(int)
        self.mapItem = defaultdict(int)
        self.trainDone = False
        self.search = False
        self.done = False

    def resetCord(self):
        self.x = 0
        self.y = 0
        self.visited.clear()

    def updateMap(self, grid, ob):
        last_inv = self.inv
        self.inv = self.getSlotInf(ob)
        for i, s in self.inv.items():
            self.mapItem[(grid[4], i)] += s - last_inv[i]

    def processTrain(self):
        for i in self.aimRecipy:
            s = 0
            d = {}
            for block, item in self.mapItem:
                if item == i:
                    s += self.mapItem[(block, item)]
                    d[block] = self.mapItem[(block, item)]
            temp = [(a, v/float(s)) for a,v in d.items()]
            temp.sort(key=lambda x: x[1],reverse = True)
            self.trainResult[i] = temp
        print self.trainResult

    def getSlotInf(self, ob):
        slotList = defaultdict(int)
        for i in range(36):
            slotName = "InventorySlot_" + str(i) + "_item"
            slotSize = "InventorySlot_" + str(i) + "_size"
            slotName = ob.get(slotName, 0)
            slotSize = ob.get(slotSize, 0)
            # print slotName
            if (slotName == 0):
                break
            slotList[slotName] = slotSize

        return slotList

    def DFSTraverse(self, agent_host, grid, ob):  # stop condition!!!!
        if self.steps == 2499:
            self.trainDone = True
            self.resetCord()
            self.processTrain()
            agent_host.sendCommand('tp 52.5 227 0.5')
        self.visited.add((self.x, self.y))
        for i, v in self.action_trans.items():
            next = self.updateCord(v)
            if grid[i] != u'air' and grid[i] != u'lava' and next not in self.visited:
                agent_host.sendCommand(v)
                self.updateMap(grid, ob)
                # print self.trainResult
                self.x = next[0]
                self.y = next[1]
                self.steps += 1
                break

    def itemInBlock(self, item, block):  # Only looking for the first choice right now
        # print 'iteminblock: block = ', block
        # print self.trainResult[item][0][0]

        if self.trainResult[item][0][0] == block:
            return True
        return False

    def itemInBag(self,item):
        for i in self.mapItem.keys():
            if i[1] == item:
                return True
        return False

    def updateCord(self, dir):
        pos = self.pos_tran[dir]
        next = (self.x - pos[0], self.y + pos[1])
        
        
        return next

    # self.action_trans = {1:"movenorth 1", 5:"moveeast 1", 3:"movewest 1", 7:"movesouth 1"}
    # self.pos_tran = {'movewest 1':(1,0),  'movesouth 1':(0,1),  'moveeast 1':(-1,0), 'movenorth 1':(0,-1)}
        

    def searchTraverse(self, agent_host, cord, grid, ob):
        self.mapItem.clear()
        print (self.x, self.y)
        self.visited.add((self.x, self.y))
        if not self.aimRecipy:
            print 'search done, crafting'
            agent_host.sendCommand('craft '+ self.aim)
            self.done = True
            return
        item = self.aimRecipy[0]
        print 'fiding item: ', item
        if self.itemInBlock(item, grid[4]):
            
            print 'finding item in current block type...'
            for i, v in self.action_trans.items():
        
                next = self.updateCord(v)
                if grid[i] != u'air' and grid[i] == grid[4] and next not in self.visited:
                    agent_host.sendCommand(v)
                    self.updateMap(grid, ob)
                    self.x = next[0]
                    self.y = next[1]
                    if self.itemInBag(item):
                        self.aimRecipy.remove(item)
                        return
                    return
        else:

            aimBlock = cord[self.trainResult[item][0][0]][0]
            print "going to aim block...", aimBlock
            direction = (aimBlock[0] - self.x, aimBlock[1] - self.y)
            print 'direction', direction
            self.updateMap(grid, ob)
            if self.itemInBag(item):
                self.aimRecipy.remove(item)
                return
            if direction[0] != 0:
                # time.sleep(5)
                if direction[0] > 0:
                    agent_host.sendCommand('moveeast 1')
                    next = self.updateCord('moveeast 1')
                    self.x = next[0]
                    self.y = next[1]
                    return
                else:
                    agent_host.sendCommand('movewest 1')
                    next = self.updateCord('movewest 1')
                    self.x = next[0]
                    self.y = next[1]
                    return
            else:
                # time.sleep(5)
                if direction[1] != 0:
                    if direction[1] > 0:
                        agent_host.sendCommand('movesouth 1')
                        next = self.updateCord('movesouth 1')
                        self.x = next[0]
                        self.y = next[1]
                        return
                    else:
                        agent_host.sendCommand('movenorth 1')
                        next = self.updateCord('movenorth 1')
                        self.x = next[0]
                        self.y = next[1]
                        return


def map_of_maze(X, Y, objects):
    # objects = {"pumpkin":"sandstone", "egg":"diamond_block", "apple":"grass", "sugar":"glass"}
    
    """
    <DrawSphere x="-27" y="70" z="0" radius="30" type="air"/>
    <DrawCuboid x1="0" y1="226" z1="0" x2="49" y2="226" z2="49" type="dirt" />
    <DrawCuboid x1="0" y1="227" z1="0" x2="
    24" y2="227" z2="24" type="grass" />
    <DrawCuboid x1="25" y1="227" z1="25" x2="49" y2="227" z2="49" type="diamond_block" />
    <DrawCuboid x1="0" y1="227" z1="25" x2="24" y2="227" z2="49" type="glass" />
    <DrawCuboid x1="25" y1="227" z1="0" x2="49" y2="227" z2="24" type="sandstone" />
    """
    number = int(math.sqrt(len(objects))) # number of sides
    lavaDict = defaultdict(list)
    LAVA = []
    with_lava = False   # True to add lava on this map

    random.random()
    MAZE = ["-" for i in range(0, (X * Y))]
    keys = []
    for i in objects:
        keys.append(i)
    itemDict = defaultdict(list)
    c = 0

    if with_lava:
        number_of_lava = ((X + Y) / 10) ** 2
        
        
        while c != number_of_lava:
            x = random.randint(0, X-1)
            y = random.randint(0, Y-1)
            if (x, y) not in LAVA and MAZE[x*(X-1)+y] == "-":
                LAVA.append((x,y))
                MAZE[ x*(X-1) + y] = 'L'
                c+=1
        lavaDict["lava"] = LAVA

    OBJECTS = objects
    blocks = len(objects)

    l = []
    maze_size = X * Y
    # this is to generate a list of objects ocurring 2-3% of the whole map.
    for i in objects:
        times = random.randint(2, 3) / float(100)
        times = int(times * maze_size)
        for j in range(times):
            l.append(i)

    c = 0  # is the current position in list l, which is a list of objects that need to be placed

    # counter = 0 # is counter for matching range tuples.
    # this is to put those objects in corressponding area
    while c != len(l):
        x = random.randint(0, X-1)
        y = random.randint(0, Y-1)
        for i in range(len(l[c])):
            if (x, y) not in LAVA:
                MAZE[x*(X-1) + y] = l[c]
                itemDict[l[c]].append((x, y))
        c += 1


    # itemDict = {A:[(0,0), [1,0], B:[(1,1), (2,1)]}
    return lavaDict, itemDict


def getBlockDrawing(DictSet):
    """Create the XML for the items."""
    lavaDict = DictSet[0]
    itemDict = DictSet[1]
    drawing = ""
    # for item in lavaDict.keys():
    #     for position in lavaDict[item]:
    #         drawing += '<DrawBlock x="' + str(position[0]) + '" y="227" z="' + str(position[1]) + '" type="' + str(item)
    #         drawing += '" />'
    for item in itemDict.keys():
        for position in itemDict[item]:
            drawing += '<DrawItem x="' + str(position[0]) + '" y="228" z="' + str(position[1]) + '" type="' + str(item)
            drawing += '" />'
    return drawing


def getItemDrawing(x, y, DictSet):
    # x, y position of the map
    itemDict = DictSet[1]
    drawing = ""
    for item in itemDict.keys():
        for position in itemDict[item]:
            drawing += '<DrawItem x="' + str(position[0]+x) + '" y="227" z="' + str(position[1]+y) + '" type="' + str(item)
            drawing += '" />'
    return drawing

def mapGenerater(x, y, itemList, start_x, start_y, num):
    # itemList: [(diamond, diamond_block), (apple, grass), (sugar, glass), (egg, dirt)]
    result = ""
    # determine the x, y of each small part of the maze

    length = num
    counter = [i for i in range(0,num**2)]  
    outputList = num**2 *[0]
    flag = False
    cordMap = defaultdict(list) 
    while not flag:

        for i in itemList:
            
            rnum = random.choice(counter)
            outputList[rnum] = i
            if len(counter) != 1:
                counter.pop(counter.index(rnum))
            else:
                flag = True

    # for i in range(length):
    #     for j in range(length):
    #         randNum = random.randint(0,3)
    #         result += '<DrawCuboid x1="' + str(int(j*x/length)+start_x)+'" y1="226" z1="' + \
    #                   str(int(i*y/length)+start_y) + '" x2="' + str(int((j+1)*x/length)+start_x)\
    #                   + '" y2="226" z2="' + str(int((i+1)*x/length)+start_y) + '" type="' + itemList[randNum][1] + '"/>'
    #         result += getItemDrawing(int(j*x/length+start_x), int((i)*x/length+start_y),
    #                                  map_of_maze((int((j+1)*x/length)-int(j*x/length)),
    #                                              (int((i+1)*x/length)-int(i*y/length)), [itemList[randNum][0]]))

    for i in range(length):
        for j in range(length):
            randNum = random.randint(0, num)
            result += '<DrawCuboid x1="' + str(int(j*x/length)+start_x)+'" y1="226" z1="' + \
                      str(int(i*y/length)+start_y) + '" x2="' + str(int((j+1)*x/length)+start_x)\
                      + '" y2="226" z2="' + str(int((i+1)*x/length)+start_y) + '" type="' + outputList[i*num+j][1] + '"/>'
            result += getItemDrawing(int(j*x/length+start_x), int((i)*x/length+start_y),
                                     map_of_maze((int((j+1)*x/length)-int(j*x/length)),
                                                 (int((i+1)*x/length)-int(i*y/length)), [outputList[i*num+j][0]]))
            cordMap[outputList[i*num+j][1]].append((j*x/num+7, i*y/num+7))

    return result, cordMap

def jammingItem(x, y, itemList):
    drawing = ""
    itemInf = defaultdict(list)
    for item in itemList:
        itemInf[item] = []
        for i in range(int(50*50/100)):
            itemInf[item].append((random.randint(0,50), random.randint(0,50)))
    drawing = getItemDrawing(x, y, ([],itemInf))
    print (itemInf)
    return drawing

def GetMissionXML():
    xml, cord = mapGenerater(44, 44, [("egg", "diamond_block"), ("apple", "grass"), ("sugar", "glass"), ("pumpkin", "sandstone")], 52, 0, 3)
    return  '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Food Hunting!</Summary>
              </About>

            <ServerSection>
              <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
              </ServerInitialConditions>
              <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,100*1,2;3;,biome_1" />
                  <DrawingDecorator>
                    <DrawSphere x="-27" y="70" z="0" radius="30" type="air"/>                    
                    ''' + mapGenerater(49, 49, [("pumpkin", "sandstone"), ("egg", "diamond_block"), ("apple", "grass"), ("sugar","glass")], 0, 0, 2)[0] +'''
                    ''' + jammingItem(0, 0, ["cookie", "cooked_fish"]) + '''
                    ''' + xml + '''
                  </DrawingDecorator>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="227" z="0.5"/>
                </AgentStart>
                <AgentHandlers>
                <AbsoluteMovementCommands/>
                <SimpleCraftCommands/>
                 <ObservationFromFullStats/>
                  <ObservationFromGrid>
                      <Grid name="floor3x3">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="-1" z="1"/>
                      </Grid>
                  </ObservationFromGrid>
                    <ObservationFromFullInventory/>
                    <DiscreteMovementCommands/>
                </AgentHandlers>
              </AgentSection>
            </Mission>''', cord



# Create default Malmo objects:
agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

# if agent_host.receivedArgument("test"):
#     num_repeats = 1
# else:
#     num_repeats = 10
xml, cord = GetMissionXML()
my_mission = MalmoPython.MissionSpec(xml, True)
my_mission_record = MalmoPython.MissionRecordSpec()
print "cord to agent: ", cord
# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print "Error starting mission:",e
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission running ",
#     s
#   8 7 6
# e 5 4 3 w
#   2 1 0
#     n
# Loop until mission ends:
agent = Agent({'pumpkin_pie': ['pumpkin', 'egg', 'sugar']}, 'pumpkin_pie')
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.14)
    world_state = agent_host.getWorldState()
    for error in world_state.errors: 
        print "Error:",error.text
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        # print observations
        # print(msg)
        grid = observations.get(u'floor3x3', 0)
        if agent.trainDone:
            agent.searchTraverse(agent_host, cord, grid, observations)
        else:
            agent.DFSTraverse(agent_host, grid, observations)
        if agent.done:
            break

print
print "Mission ended"
    # Mission has ended.