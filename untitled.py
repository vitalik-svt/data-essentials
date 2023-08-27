class Employee:

    rating = 10

    def __init__(self, age, name):
        self.age = age
        self.name = name

    @staticmethod
    def sample(x):
        print('Inside static method', x)

    @classmethod
    def change_rating(cls, new_rating):
        cls.rating = new_rating


ab = Employee(2, 3)
cd = Employee(2, 3)
print(ab.rating)
print(cd.rating)

ab.change_rating(15)
print(cd.rating)