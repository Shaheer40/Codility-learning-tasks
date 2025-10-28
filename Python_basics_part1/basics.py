print("Hello World")

a = 5
b = 10

c = "Python"
print("Language:", c)

list_example = [1, 2, 3, 4, 5]

sum = a + b
print("Sum:", sum)
diff = b - a
print("Difference:", diff)
prod = a * b
print("Product:", prod)
quot = b / a
print("Quotient:", quot)

str_example = "This is a string example."
print(str_example)
print(sorted(list_example))

if a < b:
    print(f"{a} is less than {b}") 
else:
    print(f"{a} is not less than {b}")

for i in list_example:
    print("List item:", i)