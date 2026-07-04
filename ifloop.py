num = int(input("Enter a number: "))
if num > 5:
    print("The number is greater than 5.")
elif num == 5:
    print("The number is equal to 5.")
elif num < 5 and num > 0:
    print("The number is less than 5.")
elif num < 5 and num <0:
    print("The number is negative.")
else:
    print("The number is zero.")