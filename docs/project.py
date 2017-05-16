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

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

def map_of_maze(X, Y, objects):
    import random
    from collections import defaultdict
    random.random()
    print objects
    MAZE = ["-" for i in range(0,(X*Y))]

    number_of_lava = ((X+Y)/10) ** 2
    LAVA = []
    result = defaultdict(list)
    c = 0
    while c != number_of_lava:
        x = random.randint(0, X-1)
        y = random.randint(0, Y-1)
        if (x, y) not in LAVA and MAZE[x*(X-1)+y] == "-":
            LAVA.append((x,y))
            MAZE[ x*(X-1) + y] = 'L'
            c+=1
    result["lava"] = LAVA
    OBJECTS = objects

    l = []
    maze_size = X*Y
    for i in objects:
        times = random.randint(2,5) / float(100)
        times = int(times*maze_size)
        for j in range(times):
            l.append(i)
    c = 0
    while c != len(l):
        x = random.randint(0, X-1)
        y = random.randint(0, Y-1)
        if (x,y) not in LAVA and MAZE[x*(X-1)+y] == "-":
            MAZE[ x*(X-1) + y] = l[c]
            result[l[c]].append((x,y))
            c+=1
    return result


def getItemDrawing(position_dict):
    """Create the XML for the items."""
    drawing = ""
    for item in position_dict.keys():
        for position in position_dict[item]:
            drawing += '<DrawBlock x="' + str(position[0]) + '" y="227" z="' + str(position[1]) + '" type="' + str(item)
            drawing += '" />'
    return drawing

def GetMissionXML():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
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
                    <DrawCuboid x1="0" y1="226" z1="0" x2="50" y2="226" z2="50" type="dirt" />
                    <DrawCuboid x1="0" y1="227" z1="0" x2="50" y2="227" z2="50" type="grass" />
                    <DrawCuboid x1="0" y1="226" z1="0" x2="2" y2="226" z2="2" type="diamond_block" />
                    <DrawBlock x="1" y="227" z="1" type="beacon" />
                    <DrawCuboid x1="48" y1="226" z1="48" x2="50" y2="226" z2="50" type="diamond_block" />
                    <DrawBlock x="49" y="227" z="49" type="beacon" />
                    <DrawCuboid x1="0" y1="226" z1="48" x2="2" y2="226" z2="50" type="diamond_block" />
                    <DrawBlock x="1" y="227" z="49" type="beacon" />
                    <DrawCuboid x1="48" y1="226" z1="0" x2="50" y2="226" z2="2" type="diamond_block" />
                    <DrawBlock x="49" y="227" z="1" type="beacon" />
                    ''' + getItemDrawing(map_of_maze(50, 50, [])) +'''

                  </DrawingDecorator>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="25" y="228.5" z="25"/>
                </AgentStart>
                <AgentHandlers>
                    <AgentQuitFromTouchingBlockType>
                        <Block type="redstone_block"/>
                    </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''



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

if agent_host.receivedArgument("test"):
    num_repeats = 1
else:
    num_repeats = 10

for i in range(num_repeats):
    my_mission = MalmoPython.MissionSpec(GetMissionXML(), True)
    my_mission_record = MalmoPython.MissionRecordSpec()

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

    # Loop until mission ends:
    while world_state.is_mission_running:
        sys.stdout.write(".")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print "Error:",error.text

    print
    print "Mission ended"
    # Mission has ended.