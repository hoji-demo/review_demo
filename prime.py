def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, number):
        if number % i == 0:
            return False
    return True

def nth_prime(n):
    count = 0
    number = 1
    while count < n:
        number += 1
        if is_prime(number):
            count += 1
    return number

# Example: Find the 10th prime number
n = 10
prime = nth_prime(n)
print(f"The {n}th prime number is: {prime}")

