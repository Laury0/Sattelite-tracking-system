"""
name = "Laurynas ";
Surname = "Davidavicius ";
greeting = f"Hello, my name is {name+Surname}";

a=17;
b= 5;

birth_year = input("enter your birth year: ");

my_list = ["Thing1", "Thing2", "Thing3", "Thing4", "Thing5"];

shoppingList = [];
shoppingList.append(my_list[0]);
shoppingList.append(my_list[1]);
shoppingList.append(my_list[3]);
x=len(shoppingList);
print(x);
print(shoppingList);
shoppingList.remove(my_list[0]);
x=len(shoppingList);
print(x);
print(shoppingList);

book={
    "title":"plaveholderTitle",
    "author":"placeholderAuthor",
    "year":"placeholderYear",
    "pages":"placeholderPages",
    "is_available":"Wouldnt you want to know?"
    };
print(book);

score=75;
if score>=90:
    print("Excellent");
elif score>=70:
    print("good");
elif score>=50:
    print("Satisfactory");
else:
    print("fail");

is_sunny=True;
is_warm=True;
is_weekedn=False;
print(is_sunny and is_warm);
print(is_sunny or is_warm);
print(not is_warm);
print(not is_sunny or is_weekedn);

print(greeting + birth_year);
print(a+b, a-b, a*b, a/b, a//b, a%b, a**b);
print(my_list[0], my_list[4], my_list[2:5]);
"""
"""
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name empty")
        self.__name=value

    @property
    def student_id(self):
        return self.__student_id

    @student_id.setter
    def student_id(self, value):
        if not (value.startswith("S") and 
                len(value) == 4 and 
                value[1:].isdigit()):
            raise ValueError("Must start with S")
        self.__student_id = value
class Person:
    def __init__(self, name, id):
        self._name=name;
        self._id=id;

    def display_info(self):
        return print(f"Studet: name='{self._name}' id={self._id})")

class Teacher(Person):
    def __init__(self, name, id, subject):
        super().__init__(name, id);
        self._subject=subject;
        self._students=[];

    def add_student(self, student):
        self._students.append(student);

    def get_class_average(self):
        total=0;
        count=0;
        for student in self._students:
            for grade in student._grades:
                total += grade;
                count += 1;
        if count == 0:
            cavg = 0;
        else:
            cavg=total/count;
        return cavg

    def display_info(self):
        print(f"Teacher: name='{self._name}' id={self._id}")
        print(f"Subject: {self._subject}")
        print("Students:")
        for student in self._students:
            student.display_info()

class Student(Person):
    def __init__(self, name, id):
        super().__init__(name, id);
        self._grades=[];

    def add_grade(self, grade):
        if not (0 <= grade <= 100):
            raise ValueError("Grade must be between 0 and 100.")
        self._grades.append(grade);

    @property
    def get_average(self):
        if not self._grades:
            return 0
        return sum(self._grades)/len(self._grades);

    def display_info(self):
        print(f"Student: name='{self._name}' id={self._id}")
        print(f"Grades: {self._grades}")
        print(f"Average: {self.get_average}")
        
teacher = Teacher("Dr. Smith", "T001", "Mathematics") 
student1 = Student("Anna", "S001") 
student1.add_grade(85) 
student1.add_grade(90) 
student2 = Student("John", "S002") 
student2.add_grade(75) 
student2.add_grade(80) 
teacher.add_student(student1) 
teacher.add_student(student2) 
teacher.display_info()  # Shows teacher info, subject, 2 students 
print(f"Class average: {teacher.get_class_average()}")  # 82.5 

student1 = Student("Anna", "S001")
student1.add_grade(85) 
student1.add_grade(90) 
student1.add_grade(100)
print(student1.get_average)
student1.display_info()
"""

class Product:
    def __init__(self, name, price, stock):
        self._name=name;
        self._price=price;
        self._stock=stock;

    def get_total_price(self, quanity):
        return self._price*quanity;

    def display_info(self):
        print(f"Product name: {self._name}")
        print(f"Product price: {self._price}")
        print(f"Product Stock: {self._stock}")

class CartItem:
    def __init__(self, product, quanity):
        self._product=product;
        self._quanity=quanity;

    def get_subtotal(self):
        return self._product.get_total_price(self._quanity)


class ShoppingCart:
    def __init__(self, items):
        self._items=items;

    def add_product(self, product, quantity):
        item = CartItem(product, quantity)
        self._items.append(item)

    def remove_product(self, product_name):
        for i, item in enumerate(self._items):
            if item._product._name == product_name:
                self._items.pop(i)
                break

    def get_total(self):
        return sum(item.get_subtotal() for item in self._items)

    def display_cart(self):
        for item in self._items:
            print(f"{item._product._name} x{item._quanity} = {item.get_subtotal()}")

        print(f"Total: {self.get_total()}")

class Customer:
    def __init__(self, name, email):
        self._name = name
        self._email = email
        self._cart = ShoppingCart([])

    def shop(self, product, quanity):
        for _ in range(quanity):
            self._cart.add_product(product, quanity);

    def view_cart(self):
        self._cart.display_cart()

    def checkout(self):
        total = self._cart.get_total()
        print(f"Total: {total}")
        self._cart._items.clear() 
        
class CartManager: 
    _instance = None 

    def __new__(cls): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
            cls._instance._carts = {}  # Dictionary of customer_id: cart 
        return cls._instance
    
    def get_cart(self, customer_id): 
        if customer_id not in self._carts: 
            self._carts[customer_id] = ShoppingCart([]) 
        return self._carts[customer_id]
    
    def get_all_carts_total(self): 
        return sum(cart.get_total() for cart in 
self._carts.values()) 

class Book(Product):
    def __init__(self, name, price, stock, author):
        super().__init__(name, price, stock);
        self._author=author;
        self._total=0;

    def get_total_price(self, quanity):
        if(quanity>=3):
            self._total=self._price*quanity-((self._price*quanity)*0.1);
        else: 
            self._total=self._price*quanity;
        return self._total;

    def display_info(self):
        super().display_info()
        print(f"Book Author: {self._author}")

class Electronics(Product):
    def __init__(self, name, price, stock, warranty):
        super().__init__(name, price, stock);
        self._warranty=warranty;
        self._total=0;

    def get_total_price(self, quanity):
        self._total=self._price*quanity+(self._warranty*10)
        return self._total;

    def display_info(self):
        super().display_info()
        print(f"Book Author: {self._warranty}")

# Create products 
book1 = Book("Python Guide", 30, 10, "Smith") 
laptop = Electronics("Dell Laptop", 800, 5, 2) 
# Create customer (composition: customer owns cart) 
customer = Customer("Anna", "anna@email.com") 
# Shopping (aggregation: cart references products, doesn't own them) 
customer.shop(book1, 2) 
customer.shop(laptop, 1) 
customer.view_cart() 
total = customer.checkout() 
# Products still exist after checkout (aggregation) 
print(book1._name)  # Still accessible 
# But cart items are gone (composition) 
customer.view_cart()  # Empty cart ,,  f3

# These are the SAME object 
manager1 = CartManager() 
manager2 = CartManager() 
print(manager1 is manager2)  # True 
# Both see the same carts 
cart1 = manager1.get_cart("customer1") 
cart2 = manager2.get_cart("customer1") 
print(cart1 is cart2)  # True 

"""
for Product in Products:
    print(f"{Product._name}: {Product.get_total_price(3)} euros")
    Product.display_info()
"""