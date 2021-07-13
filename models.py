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
    pass


class PatientBook:
    order_book = AVLTree()
    pk_book = AVLTree()
    health_book = AVLTree()

    @classmethod
    def add(cls, patient):
        pass

    @classmethod
    def update(cls, patient):
        pass

    @classmethod
    def delete_first_by_order(cls):
        pass

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
        PatientBook.delete_first_by_order()

    @staticmethod
    def serve_sickest_patient():
        PatientBook.delete_first_by_health()
