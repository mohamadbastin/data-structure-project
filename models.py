# idk wth im doing

class Patient:
    _order = 103  # to show that order is relative

    def __init__(self, pk, health):
        self.pk = pk
        self.health = health
        Patient._order += 12
        self.order = self._order

    def __str__(self):
        return f'{self.pk} {self.health} {self.order}'


class Node:
    def __init__(self, patient, key):
        self.patient = patient
        self.key = key
        self.right = None
        self.left = None

    def __str__(self):
        return str(self.patient)


class AVLTree:

    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

        # if len(args) == 1:
        #     for i in args[0]:
        #         self.insert(i)

    def height(self):
        if self.node:
            return self.node.height
        else:
            return 0

    def is_leaf(self):
        return self.height == 0

    def insert(self, patient, key):
        tree = self.node

        newnode = Node(patient, key)

        if tree is None:
            self.node = newnode
            self.node.left = AVLTree()
            self.node.right = AVLTree()
            # print("Inserted key [" + str(key) + "]")

        elif key < tree.key:
            self.node.left.insert(patient, key)

        elif key > tree.key:
            self.node.right.insert(patient, key)

        else:
            # print("Key [" + str(key) + "] already in tree.")
            pass

        self.rebalance()

    def rebalance(self):
        """
            Rebalance a particular (sub)tree
            """
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.lrotate()  # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rrotate()  # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()

    def rrotate(self):
        # Rotate left pivoting on self
        # print('Rotating ' + str(self.node.key) + ' right')
        A = self.node
        B = self.node.left.node
        T = B.right.node

        self.node = B
        B.right.node = A
        A.left.node = T

    def lrotate(self):
        # Rotate left pivoting on self
        # print('Rotating ' + str(self.node.key) + ' left')
        A = self.node
        B = self.node.right.node
        T = B.left.node

        self.node = B
        B.left.node = A
        A.right.node = T

    def update_heights(self, recurse=True):
        if self.node is not None:
            if recurse:
                if self.node.left is not None:
                    self.node.left.update_heights()
                if self.node.right is not None:
                    self.node.right.update_heights()

            self.height = max(self.node.left.height,
                              self.node.right.height) + 1
        else:
            self.height = -1

    def update_balances(self, recurse=True):
        if self.node is not None:
            if recurse:
                if self.node.left is not None:
                    self.node.left.update_balances()
                if self.node.right is not None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def delete(self, patient, key):
        # print()("Trying to delete at node: " + str(self.node.key))
        if self.node is not None:
            if self.node.key == key and self.node.patient == patient:
                # print("Deleting ... " + str(key))
                if self.node.left.node is None and self.node.right.node is None:
                    self.node = None  # leaves can be killed at will
                # if only one subtree, take that
                elif self.node.left.node is None:
                    self.node = self.node.right.node
                elif self.node.right.node is None:
                    self.node = self.node.left.node

                # worst-case: both children present. Find logical successor
                else:
                    replacement = self.logical_successor(self.node)
                    if replacement is not None:  # sanity check
                        print("Found replacement for " + str(key) + " -> " + str(replacement.key))
                        self.node.key = replacement.key

                        # replaced. Now delete the key from right child
                        self.node.right.delete(replacement.key)

                self.rebalance()
                return
            elif key <= self.node.key:
                self.node.left.delete(patient, key)
            elif key > self.node.key:
                self.node.right.delete(patient, key)

            self.rebalance()
        else:
            return

    def delete_first_node(self):
        first_node = self.node
        print("Deleting First Node ... ")
        if self.node.left.node is None and self.node.right.node is None:
            self.node = None  # leaves can be killed at will
        # if only one subtree, take that
        elif self.node.left.node is None:
            self.node = self.node.right.node
        elif self.node.right.node is None:
            self.node = self.node.left.node

        # worst-case: both children present. Find logical successor
        else:
            replacement = self.logical_successor(self.node)
            if replacement is not None:  # sanity check
                # print("Found replacement for " + str(key) + " -> " + str(replacement.key))
                self.node.key = replacement.key

                # replaced. Now delete the key from right child
                self.node.right.delete(replacement.key)

        self.rebalance()
        # return first_node

    def delete_smallest(self):
        node = self.node
        while node.left.node is not None:
            node = node.left.node
        nn = node
        self.delete(node.patient, node.key)
        return nn.patient

    #
    # def logical_predecessor(self, node):
    #     """
    #         Find the biggest valued node in LEFT child
    #         """
    #     node = node.left.node
    #     if node is not None:
    #         while node.right is not None:
    #             if node.right.node is None:
    #                 return node
    #             else:
    #                 node = node.right.node
    #     return node

    def logical_successor(self, node):
        """
            Find the smallest valued node in RIGHT child
            """
        node = node.right.node
        if node is not None:  # just a sanity check

            while node.left is not None:
                print("LS: traversing: " + str(node.key))
                if node.left.node is None:
                    return node
                else:
                    node = node.left.node
        return node

    def check_balanced(self):
        if self is None or self.node is None:
            return True

        # We always need to make sure we are balanced
        self.update_heights()
        self.update_balances()
        return (abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced()

    def inorder_traverse(self):
        if self.node is None:
            return []

        inlist = []
        l = self.node.left.inorder_traverse()
        for i in l:
            inlist.append(i)

        inlist.append(self.node.key)

        l = self.node.right.inorder_traverse()
        for i in l:
            inlist.append(i)

        return inlist

    def display(self, level=0, pref=''):
        """
            Display the whole tree. Uses recursive def.
            TODO: create a better display using breadth-first search
            """
        self.update_heights()  # Must update heights before balances
        self.update_balances()
        if self.node is not None:
            print('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(
                self.balance) + "]", 'L' if self.is_leaf() else ' ')
            if self.node.left is not None:
                self.node.left.display(level + 1, '<')
            if self.node.left is not None:
                self.node.right.display(level + 1, '>')


class PatientBook:
    order_book = AVLTree()
    pk_book = AVLTree()
    health_book = AVLTree()

    @classmethod
    def display(cls):
        cls.pk_book.display()
        print('--------------------------------------------')

        cls.order_book.display()
        print('--------------------------------------------')

        cls.health_book.display()
        print('--------------------------------------------')

    @classmethod
    def add(cls, patient):
        # print(f"adding patient {patient.pk} with {patient.health} health and order {patient.order}")
        cls.order_book.insert(patient, patient.order)
        cls.pk_book.insert(patient, patient.pk)
        cls.health_book.insert(patient, patient.health)
        # print(f"patient added. {patient.pk}")
        # print('--------------------------------------------')

    @classmethod
    def update(cls, patient):
        pass

    @classmethod
    def delete_first_by_order(cls):
        # cls.display()
        # print("removing first arrived patient")
        patient = cls.order_book.delete_smallest()
        cls.pk_book.delete(patient, patient.pk)

        # cls.display()
        return patient

    @classmethod
    def delete_first_by_health(cls):
        pass


class Secretary:

    @staticmethod
    def add_patient(patient):
        PatientBook.add(patient)

    @staticmethod
    def update_patient(patient):
        PatientBook.update(patient)

    @staticmethod
    def serve_first_patient():
        patient = PatientBook.delete_first_by_order()
        print(patient)

    @staticmethod
    def serve_sickest_patient():
        PatientBook.delete_first_by_health()


Secretary.add_patient(Patient(3, -20))
Secretary.add_patient(Patient(2, 10))
Secretary.add_patient(Patient(1, 100))
#
# Secretary.serve_first_patient()
# Secretary.serve_first_patient()
# Secretary.serve_first_patient()
