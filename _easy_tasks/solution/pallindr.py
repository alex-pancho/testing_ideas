# from functools import cache
# @cache
def fib_recursive(n):
    if n <=0:
        return 0
    elif n==1:
        return 1
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)


def fib_iter(n):
    if n <=0:
        return 0
    elif n==1:
        return 1
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a+b
    return b

a = 100
# print(fib_recursive(a))
print(fib_iter(a))

def is_palindrome(string):
    """
    Check if a string is a palindrome using slicing.
    
    :param string: Input string
    :return: True if the string is a palindrome, False otherwise
    """
    middle = len(string) // 2

    return string[:middle] == string[-1:-(middle + 1):-1]

# Example usage:
print(is_palindrome("radar"))  # True
print(is_palindrome("abba"))  # True
print(is_palindrome("record"))  # False
print(is_palindrome("hello"))  # False