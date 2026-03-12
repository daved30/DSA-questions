class Node:
    def __init__(self, val, next = None):
        self.val = val
        self.next = next
        
class LinkedList:
    def __init__(self, head = None, tail = None):
        self.head = head
        self.tail = tail
        
    def disp(self):
        if self.isEmpty():
            return
        curr = self.head
        while curr:
            print(f"{curr.val} -> ", end="")
            curr = curr.next
        print("None")
        self.dispHeadTail()
        
    def isEmpty(self):
        if None == self.head and None == self.tail:
            print("Empty LL!")
            return True
        print("LL contains nodes!")
        return False
        
    def insertHead(self, node):
        if self.isEmpty():
            print(f"New node {node.val} is the Head now!")
            self.head = self.tail = node
            return
        node.next = self.head
        self.head = node
        print(f"LL not empty! New node {node.val} is the Head now!")
        
    def insertTail(self, node):
        if self.isEmpty():
            print(f"LL not empty! New node {node.val} is the Tail now!")
            self.head = self.tail = node
            return
        self.tail.next = node
        self.tail = node
        print(f"LL not empty! New node {node.val} is the Tail now!")
        
    def deleteNode(self, val):
        if self.isEmpty():
            return
        if self.head.val == val:
            self.head = self.head.next
            return
        curr = self.head
        while curr.next and curr.next.val != val:
            curr = curr.next
        if curr.next:  # found target
            if curr.next == self.tail:  # if deleting tail
                self.tail = curr
            curr.next = curr.next.next
        
    def search(self, val):
        if self.isEmpty():
            return
        curr = self.head
        while curr:
            if curr.val == val:
                print(f"Node found with value: {curr.val} refers to {curr.next}")
                return
            curr = curr.next
        print(f"Node with value {val} not found!")

    def dispHeadTail(self):
        if self.isEmpty():
            print("No head/tail node!")
            return
        print(f"HEAD -> {self.head.val if self.head else None} | TAIL -> {self.tail.val if self.tail else None}")
        
class Stack:
    pass

class Queue:
    pass

class PQ:
    pass

node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node1.next = node2
node2.next = node3
l = LinkedList(node1, node3)
l.disp()
node0 = Node(0)
l.insertHead(node0)
l.disp()
l.deleteNode(0)
l.disp()
l.search(100)
l.disp()