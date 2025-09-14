"""
Python Decorators — A Minimal Guide
-----------------------------------
Concepts covered:
1. First-class functions
2. Returning functions (closures)
3. Why and how we use decorators
"""

# ----------------------------------------
# 1. First-class functions
# ----------------------------------------
# Functions in Python can be:
#   (1) Assigned to variables
#   (2) Passed as arguments
#   (3) Returned from other functions

def square(x):
    return x * x

# (1) Assigned to variable
f = square   # without (), means function is stored (not executed yet)
print(f(5))  # 25

# (2) Passed as arguments
def add_one(func, num):
    return func(num) + 1

print(add_one(f, 3))  # square(3) + 1 = 10

# (3) Returned from functions (closure)
def display(message):
    def inner_func():
        print("Display:", message)
    return inner_func

message1 = display("Hi")  # returns inner_func
message1()                # executes inner_func → Display: Hi

# Key point: function does not execute until we call it with ()
# when inner_func is returned, it's not executed yet.
# So message1 = display("Hi") means message1 is now inner_func without executing it.
# When you add () after message1, it executes inner_func. And inner_func has stored "Hi".


# Example: HTML tag wrapper
def html_tag(tag):
    def wrap_text(msg):
        print("<{0}>{1}</{0}>".format(tag, msg))
    return wrap_text

print_h1 = html_tag("h1")
print_h1("Test Headline!")
print_h1("Another Headline!")

print_p = html_tag("p")
print_p("Test Paragraph!")

# Output:
# <h1>Test Headline!</h1>
# <h1>Another Headline!</h1>
# <p>Test Paragraph!</p>


# ----------------------------------------
# 2. Why use decorators?
# ----------------------------------------
# A decorator allows us to "attach" new behavior
# to an existing function without changing its code.

# --- decorator convention ---
# A decorator is a function that takes another function as an argument,
# adds some kind of functionality and returns another function.
# The inner function is called a "wrapper" function.
# 1. Define a decorator
def decorator(func):
    def wrapper():
        print("Before function")
        func()                # call the original function
        print("After function")
    return wrapper           # return the new function

# 2. Use the decorator
@decorator
def say_hello():
    print("Hello!")

# --- Traditional way ---
def reminder(func):
    func()
    print("Don't forget...")

def action1():
    print("I want to buy sth1")

def action2():
    print("I want to buy sth2")

reminder(action1)
# Output:
# I want to buy sth1
# Don't forget...
reminder(action2)
# Output:
# I want to buy sth2
# Don't forget...

# --- Using decorator ---
def reminder(func):
    def inner_method():
        func()
        print("Don't forget...")
    return inner_method

@reminder
def action3():
    print("I want to buy sth3")

action3()
# Output:
# I want to buy sth3
# Don't forget...


# ----------------------------------------
# 3. Example: Handling exceptions with decorator
# ----------------------------------------
def check(func):
    def inside(a, b):
        if b == 0:
            print("Can't divide by 0")
            return
        return func(a, b)
    return inside

# Traditional usage
def div(a, b):
    return a / b

div = check(div)  # attach decorator manually
print(div(10, 0)) # Can't divide by 0

# Explanation:
# 'def inside(a,b)' → only defines the function. It does not run its code.
# when you do 'div = check(div)'.
# check(div) would take the func 'div' and return another function 'inside'.
# So now the original func 'div' is gone and returns 'inside' instead.
# so 'div = check(div)' means 'div = inside'
# *******************************Important******************************************
# * The core of the decorator is to replace arg function with the wrapper function.*
# **********************************************************************************
# At this point, 'inside' has not run yet.
# When you do 'div(10,0)', it actually means 'inside(10,0)' now.
# Now 'inside' runs its code, which checks if b==0 first.
# If b==0, it prints the message and returns None.
# If b!=0, it runs 'return func(a,b)', which calls the original 'div' function.



# Better usage with @decorator
@check
def div2(a, b):
    return a / b

print(div2(10, 0))  # Can't divide by 0
print(div2(10, 2))  # 5.0

