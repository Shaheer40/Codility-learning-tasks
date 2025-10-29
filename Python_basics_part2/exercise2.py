#Palindrome number
def is_palindrome(num):
    """
    Convert number to string and check palindrome
    Time: O(n), Space: O(n)
    """
    num_str = str(num)
    if num_str == num_str[::-1]:
        return True
    else:
        return False

# Example usage
z = 121
print(is_palindrome(z))