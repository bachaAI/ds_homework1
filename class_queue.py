from collections import deque
#temporary class of queue
class Queue:
    def __init__(self):
        self.q=deque([])
    def add(self, input):
        self.q.append(input)
        return self.q
    def take(self):
        return self.q.popleft()

#queue=Queue()
#queue.add('3,6,c')
#queue.add('5,6,c')
#queue.add('4,1,c')
#queue.add('3,4,c')
#print queue.q
#print queue.take()
#print queue.q

