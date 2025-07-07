from sys import exception


class node:
    def __init__(self,state,parent,action):
        self.state=state
        self.parent=parent
        self.action=action

class StackFrontier():
    def __init__(self):
        self.frontier=[]
    
    def add(self,node_):
        self.frontier.append(node_)

    def contains_state(self,state):
        return any(node.state==state for node in self.frontier)

    def empty(self):
        return len(self.frontier)==0

    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier.")
        else:
            node=self.frontier[-1]
            self.frontier=self.frontier[-1]
            return node



class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier.")
        else:
            node=self.frontier[0]
            self.frontier=self.frontier[1:]
            return node



    