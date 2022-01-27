# Classes are a way of grouping together objects with similar attributes

class dog:
    # Here species would be a class attribute, as every instance of dog would be the same species, Pooch
    species = "Pooch"

    # __init__ has to be done for every class, and defines the characteristics which are unique to each instance
    # It always starts with self
    def __init__(self, colour, name, age, breed):
        self.breed = breed
        self.colour = colour
        self.name = name
        self.age = age

    # __str__ will define what is returned when you print an object of a certain class
    def __str__(self):
        return f"{self.name} is a {self.age} year old {self.breed} with {self.colour} fur"

    # Below is an instance method, which can only be called by objects/instances of this class
    # An instance methods first parameter is also always self
    def speak(self, sound):
        return f"{self.name} says {sound}"

# You can create a child of a parent class as well, for example for different breeds of dogs
# To do this, just include the parent class in the parentheses when creating the child class
class RhodesianRidgeback(dog):
    pass

class Rottweiler(dog):
    pass

class Dachshund(dog):
    pass

print(type(Dachshund))

# The child classes will inherit all of the same attributes of their parents
saffi = RhodesianRidgeback("brown", "Saffi", "11", "rhodesian ridgeback")
milly = Dachshund("black", "Milly", 5, "Dachshund")

print(saffi)

print(saffi.species)

print(isinstance(saffi, RhodesianRidgeback))

