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


#Two Sum
def two_sum(nums, target):
    """
    Time: O(n), Space: O(n)
    """
    num_map = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    
    return []

arr = [2, 7, 11, 15]
target = 9
result = two_sum(arr, target)
print("Two Sum Result:", result)


#two numbers add
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def addTwoNumbers(l1, l2):
    """
    Time: O(max(m, n)), Space: O(max(m, n))
    where m and n are lengths of l1 and l2
    """
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        # Get values from current nodes (0 if node is None)
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        # Calculate sum and carry
        total = val1 + val2 + carry
        carry = total // 10
        digit = total % 10
        
        # Create new node with digit
        current.next = ListNode(digit)
        current = current.next
        
        # Move to next nodes if they exist
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next

def create_linked_list(arr):
    """Create a linked list from an array"""
    dummy = ListNode(0)
    current = dummy
    for num in arr:
        current.next = ListNode(num)
        current = current.next
    return dummy.next

def linked_list_to_list(head):
    """Convert linked list to Python list"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


l1 = create_linked_list([2, 4, 3])
l2 = create_linked_list([5, 6, 4])
result = addTwoNumbers(l1, l2)
print(linked_list_to_list(result))  # Output: [7, 0, 8]



#longest substring without repeating characters

def length_of_longest_substring_map(s):
    """
    Time: O(n), Space: O(min(m, n))
    Stores the most recent index of each character
    """
    char_map = {}  # character -> index
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If character exists in map and is within current window
        if s[right] in char_map and char_map[s[right]] >= left:
            # Move left pointer to position after duplicate
            left = char_map[s[right]] + 1
        
        # Update character's latest position
        char_map[s[right]] = right
        # Update max length
        max_length = max(max_length, right - left + 1)
    
    return max_length

def test_longest_substring():
    test_cases = [
        ("abcabcbb", 3),   # "abc"
        ("bbbbb", 1),      # "b"
        ("pwwkew", 3),     # "wke"
        ("", 0),           # empty string
        (" ", 1),          # single space
        ("au", 2),         # "au"
        ("dvdf", 3),       # "vdf"
        ("abba", 2),       # "ab" or "ba"
    ]
    
    for s, expected in test_cases:
        result2 = length_of_longest_substring_map(s)
        print(result2)

# Run tests
test_longest_substring()