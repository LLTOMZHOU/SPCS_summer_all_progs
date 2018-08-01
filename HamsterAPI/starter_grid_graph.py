'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          grid_graph_starter.py
   By:            Qin Chen
   Last Updated:  6/10/18
    
   Definition of class GridGraph. Description of all the methods is
   provided. Students are expected to implement the methods for Lab#6.
   ========================================================================*/
'''
import Tkinter as tk

class GridGraph(object):
    def __init__(self):
        self.nodes = [] # {node_name: set(neighboring nodes), ...}
        self.startNode = None  # string
        self.goalNode = None    # string
        self.grid_rows = None
        self.grid_columns = None
        self.obs_list = []
        self.node_display_locations=[]
        return

    # set number of rows in the grid
    def set_grid_rows(self, rows):
        self.grid_rows = rows

    # set number of columns in the grid
    def set_grid_cols(self, cols):
        self.grid_columns = cols

    # this method is used by make_grid() to create a key-value pair in self.nodes{},
    # where value is created as an empty set which is populated later while connecting
    # nodes.
    def add_node(self, name):
        self.nodes.append([name, []])

    # set start node name
    def set_start(self, name):
        self.startNode = name

    # returns start node name
    def get_start_node(self):
        return self.startNode

    # set goal node name
    def set_goal(self, name):
        self.goalNode = name

    # return goal node name
    def get_goal_node(self):
        return self.goalNode

    # Given two neighboring nodes. Put them to each other's neighbors-set. This
    # method is called by self.connect_nodes() 
    def add_neighbor(self, node1, node2):

        x1 = int(node1[0])
        y1 = int(node1[2])
        x2 = int(node2[0])
        y2 = int(node2[2])
        
        if [x1, y1] in self.obs_list:
            return 
        if [x2, y2] in self.obs_list:
            return
        
        '''
        print node1
        print node2

        print "\n\n"
        '''

        for node in self.nodes:
            if node[0] == node1:
                node[1].append(node2)

            # if node[0] == node2:
                # node[1].append(node1)

    # populate graph with all the nodes in the graph, excluding obstacle nodes
    def make_grid(self):
        for i in range(self.grid_rows):
            for j in range(self.grid_columns):
                flag = False
                for obs in self.obs_list:
                    if i == obs[0] and j == obs[1]:
                        flag = True
                if not flag:
                    name = str(i)+"-"+str(j)
                    self.add_node(name)



    # Based on node's name, this method identifies its neighbors and fills the 
    # set holding neighbors for every node in the graph.
    def connect_nodes(self):
        for node in self.nodes:
            x1 = int(node[0][0])
            y1 = int(node[0][2])
            if y1 - 1 >= 0:
                self.add_neighbor(node[0], str(x1)+"-"+str(y1-1))
                # print node[0]
                # print str(x1)+"-"+str(y1-1)
            if y1 + 1 < self.grid_columns:
                self.add_neighbor(node[0], str(x1)+"-"+str(y1+1))
                # print node[0]
                # print str(x1)+"-"+str(y1+1)
            if x1 - 1 >= 0:
                self.add_neighbor(node[0], str(x1-1)+"-"+str(y1))
                # print node[0]
                # print str(x1-1)+"-"+str(y1)
            if x1 + 1 < self.grid_rows:
                self.add_neighbor(node[0], str(x1+1)+"-"+str(y1))
                # print node[0]
                # print str(x1+1)+"-"+str(y1)
    # For display purpose, this function computes grid node location(i.e., offset from upper left corner where is (1,1)) 
    # of display area. based on node names.
    # Node '0-0' is displayed at bottom left corner 
    def compute_node_locations(self):
        print "something happened in grid_graph.py"
        for node in self.nodes:
            self.node_display_locations.append((int(node[0][0]), int(node[0][2])))

###########################################################
#  A testing program of your implementaion of GridGraph class.
###########################################################
def main():
    graph = GridGraph()
    # grid dimension
    graph.set_grid_rows(4)
    graph.set_grid_cols(3)

    # origin of grid is (0, 0) lower left corner
    # graph.obs_list = ([1,1],)    # in case of one obs. COMMA
    graph.obs_list = ([1,1], [3,0], [2,2])
    
    graph.set_start('0-0')
    graph.set_goal('2-1')
    
    graph.make_grid()
    '''
    for node in graph.nodes:
        print node
        print "\n"
    '''
    graph.connect_nodes()

    graph.compute_node_locations()

    for node in graph.nodes:
        print node
        print "\n"

    return

if __name__ == "__main__":
    main()