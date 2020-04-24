while True:
    age = input("Please enter your age: ")
    if age.isdigit():
        age = int(age)
        break
    else:
        print("Invalid number '{age}'. Try again.".format(age=age))

if age >= 18:
    print("You are able to vote in the United States!")
else:
    print("You are not able to vote in the United States.")