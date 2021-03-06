# idk wth im doing

class Patient:
    tmp = None
    _order = 100  # to show that order is relative

    def __init__(self, pk, health):
        self.pk = pk
        self.health = health
        Patient._order += 10
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

    def is_leaf(self):
        return self.height == 0

    def insert(self, patient, key):
        tree = self.node

        newnode = Node(patient, key)

        if tree is None:
            self.node = newnode
            self.node.left = AVLTree()
            self.node.right = AVLTree()

        elif key <= tree.key:
            self.node.left.insert(patient, key)

        elif key > tree.key:
            self.node.right.insert(patient, key)

        else:
            pass

        self.rebalance()

    def rebalance(self):
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.lrotate()
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rrotate()
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()

    def rrotate(self):
        A = self.node
        B = self.node.left.node
        T = B.right.node

        self.node = B
        B.right.node = A
        A.left.node = T

    def lrotate(self):
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

    def delete(self, pk, key, flag=True):

        if self.node is not None:
            if self.node.key == key and self.node.patient.pk == pk:
                # the_node = self.node
                if flag:
                    Patient.tmp = self.node.patient
                # print("Deleting ... " + str(self.node))
                if self.node.left.node is None and self.node.right.node is None:
                    self.node = None  # leaves can be killed at will
                # if only one subtree, take that
                elif self.node.left.node is None:
                    self.node = self.node.right.node
                elif self.node.right.node is None:
                    self.node = self.node.left.node

                else:
                    replacement = self.logical_successor(self.node)
                    if replacement is not None:  # sanity check
                        self.node.key = replacement.key
                        self.node.patient = replacement.patient

                        self.node.right.delete(replacement.patient.pk, replacement.key, flag=False)

                self.rebalance()
                return
            elif key <= self.node.key:
                self.node.left.delete(pk, key)
            elif key > self.node.key:
                self.node.right.delete(pk, key)

            self.rebalance()
        else:
            return

    def delete_smallest(self):
        node = self.node
        if node.left is None and node.right is None:
            nn = node.patient
            self.delete(node.patient.pk, node.key)
            return nn
        while node.left.node is not None:
            node = node.left.node
        nn = node
        self.delete(node.patient.pk, node.key)
        return nn.patient

    def logical_successor(self, node):

        node = node.right.node
        if node is not None:

            while node.left is not None:
                if node.left.node is None:
                    return node
                else:
                    node = node.left.node
        return node

    def display(self, level=0, pref=''):

        self.update_heights()
        self.update_balances()
        if self.node is not None:
            print('-' * level * 2, pref, self.node.key, "[" + str(self.node.patient) + "]",
                  'L' if self.is_leaf() else ' ')
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
        cls.order_book.insert(patient, patient.order)
        cls.pk_book.insert(patient, patient.pk)
        cls.health_book.insert(patient, patient.health)

    @classmethod
    def update(cls, pk, health):

        cls.pk_book.delete(pk, pk)
        p = Patient.tmp
        cls.health_book.delete(pk, p.health)
        cls.order_book.delete(pk, p.order)

        new_p = Patient(pk, health)
        new_p.order = p.order - 1

        cls.pk_book.insert(new_p, new_p.pk)
        cls.order_book.insert(new_p, new_p.order)
        cls.health_book.insert(new_p, new_p.health)

    @classmethod
    def delete_first_by_order(cls):

        patient = cls.order_book.delete_smallest()
        cls.pk_book.delete(patient.pk, patient.pk)
        cls.health_book.delete(patient.pk, patient.health)

        return patient

    @classmethod
    def delete_first_by_health(cls):
        patient = cls.health_book.delete_smallest()
        cls.pk_book.delete(patient.pk, patient.pk)
        cls.order_book.delete(patient.pk, patient.order)

        return patient


class Secretary:

    @staticmethod
    def add_patient(patient):
        PatientBook.add(patient)

    @staticmethod
    def update_patient(pk, health):
        PatientBook.update(pk, health)

    @staticmethod
    def serve_first_patient():
        patient = PatientBook.delete_first_by_order()
        print(patient)

    @staticmethod
    def serve_sickest_patient():
        patient = PatientBook.delete_first_by_health()
        print(patient)


DEBUG = False


if DEBUG:
    Secretary.add_patient(Patient(30, -20))
    Secretary.add_patient(Patient(20000, 10))
    Secretary.add_patient(Patient(111, 100))

    # Secretary.serve_first_patient()
    # Secretary.serve_first_patient()
    # Secretary.serve_first_patient()

    Secretary.serve_sickest_patient()
    # Secretary.serve_sickest_patient()
    Secretary.serve_first_patient()

    Secretary.serve_sickest_patient()

else:
    inputs = []
    while True:
        inp = input()
        if inp == "":
            break
        inputs.append(inp)

    for i in inputs:
        if i[:3] == "Add":
            patient = Patient(int(i.split()[1]), int(i.split()[2]))
            Secretary.add_patient(patient)

        elif "Serve First" in i:
            Secretary.serve_first_patient()

        elif "Serve Sickest" in i:
            Secretary.serve_sickest_patient()

        elif "Update" in i:
            Secretary.update_patient(int(i.split()[1]), int(i.split()[2]))
