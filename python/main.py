from collections import Counter, defaultdict, OrderedDict
import inspect, re, ast
from typing import List, Optional


# Input parser
def parse_input_line(input_line: str):
    args_dict = {}
    parts = re.split(r',(?![^\[]*\])', input_line)
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            key, value = key.strip(), value.strip()
            try:
                args_dict[key] = ast.literal_eval(value)
            except Exception:
                args_dict[key] = value
    return args_dict

# Runner for class methods
def run_all_classes(module):
    for cls_name, cls in inspect.getmembers(module, inspect.isclass):
        if cls_name == "Solution":
            solution = cls()
            methods = OrderedDict(
                sorted(
                    inspect.getmembers(cls, inspect.isfunction),
                    key=lambda x: x[1].__code__.co_firstlineno
                )
            )
            for name, method in methods.items():
                doc = method.__doc__
                if not doc:
                    continue

                print(f"\nMethod: {name}")
                print("Docstring:", doc.strip())

                inputs = re.findall(r"Input:\s*(.*)", doc)
                outputs = re.findall(r"Output:\s*(.*)", doc)

                for idx, input_line in enumerate(inputs, start=1):
                    try:
                        args_dict = parse_input_line(input_line)

                        # Convert linked list inputs
                        for key, value in args_dict.items():
                            if isinstance(value, list) and key in ["head", "list1", "list2"]:
                                args_dict[key] = list_to_linked(value)

                        result = method(solution, **args_dict)

                        # Normalize outputs
                        if isinstance(result, ListNode):
                            result = linked_to_list(result)
                        elif result is None:
                            result = []

                        expected = None
                        if idx-1 < len(outputs):
                            try:
                                expected = ast.literal_eval(outputs[idx-1].strip())
                            except Exception:
                                expected = outputs[idx-1].strip()

                        print(f"Example {idx} Output: {result}")
                        if expected is not None:
                            if result == expected:
                                print("✅ Matches expected:", expected)
                            else:
                                print("❌ Mismatch! Expected:", expected)
                    except Exception as e:
                        print(f"Could not run Example {idx} automatically:", e)


# Linked list helpers
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def list_to_linked(lst):
    dummy = ListNode(0)
    curr = dummy
    for val in lst:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next

def linked_to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

class Solution:
    def __init__(self):
        self.stringValEnc = self.encode(["Hello","World"])
        self.stringValDec = self.decode(self.stringValEnc)
        
    def hasDuplicate(self, nums: list[int]) -> bool:
        """
        Example 1:
        Input: nums = [1,2,3,1]
        Output: true
        Explanation:
        The element 1 occurs at the indices 0 and 3.

        Example 2:
        Input: nums = [1,2,3,4]
        Output: false
        Explanation:
        All elements are distinct.

        Example 3:
        Input: nums = [1,1,1,3,3,4,3,2,4,2]
        Output: true
        """
        count = {}
        for i in nums:
            if i in count.keys():
                return True
            count[i] = 1
        return False
    
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Example 1:
        Input: s = "anagram", t = "nagaram"
        Output: True

        Example 2:
        Input: s = "rat", t = "car"
        Output: False
        """
        a, b = {}, {}
        for i in s:
            a[i] = a.get(i, 0) + 1
        for j in t:
            b[j] = b.get(j, 0) + 1
        if a == b:
            return True
        return False
    
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """
        Example 1:
        Input: nums = [2,7,11,15], target = 9
        Output: [0,1]
        Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
        
        Example 2:
        Input: nums = [3,2,4], target = 6
        Output: [1,2]
        
        Example 3:
        Input: nums = [3,3], target = 6
        Output: [0,1]
        """
        count = {}
        for i in range(len(nums)):
            num = nums[i]
            diff = target - num
            if num in count.keys():
                return [count[num], i]
            count[diff] = i
        return [0, 0]

    def mergeIntervals(self, intervals: list[list[int]]) -> list[list[int]]:
        """
        Example 1:
        Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
        Output: [[1,6],[8,10],[15,18]]
        Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
        
        Example 2:
        Input: intervals = [[1,4],[4,5]]
        Output: [[1,5]]
        Explanation: Intervals [1,4] and [4,5] are considered overlapping.
        
        Example 3:
        Input: intervals = [[4,7],[1,4]]
        Output: [[1,7]]
        Explanation: Intervals [1,4] and [4,7] are considered overlapping.
        """
        intervals.sort(key=lambda x: x[0])
        merged = []
        for interval in intervals:
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval.copy())
            else:
                merged[-1] = [merged[-1][0], max(merged[-1][1], interval[1])]
        return merged

    def shiftZeros(self, nums: list[int]) -> None:
        """
        Example 1:
        Input: nums = [0,1,0,3,12]
        Output: [1,3,12,0,0]
        
        Example 2:
        Input: nums = [0]
        Output: [0]
        """
        left = 0
        for right in range(len(arr)):
            if arr[right] != 0:
                arr[left], arr[right] = arr[right], arr[left]
                left += 1
        return arr

    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        """
        Example 1:
        Input: strs = ["eat","tea","tan","ate","nat","bat"]
        Output: [['bat'], ['nat', 'tan'], ['ate', 'eat', 'tea']]
        Explanation:
        There is no string in strs that can be rearranged to form "bat".
        The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.
        The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.
        
        Example 2:
        Input: strs = [""]
        Output: [[""]]
        
        Example 3:
        Input: strs = ["a"]
        Output: [["a"]]
        """
        if len(strs) == 0:
            return [[""]]
        if len(strs) == 1:
            return [[strs[0]]]
        anagrams = {}
        for word in strs:
            char_count = {}
            for ch in word:
                char_count[ch] = char_count.get(ch, 0) + 1
            key = tuple(sorted(char_count.items()))
            if key not in anagrams:
                anagrams[key] = []
            anagrams[key].append(word)
        return list(anagrams.values())

    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        """
        Example 1:
        Input: strs = ["eat","tea","tan","ate","nat","bat"]
        Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
        Explanation:
        There is no string in strs that can be rearranged to form "bat".
        The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.
        The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.
        
        Example 2:
        Input: strs = [""]
        Output: [[""]]
        
        Example 3:
        Input: strs = ["a"]
        Output: [["a"]]
        """
        res = defaultdict(list)
        for word in strs:
            sortedS = "".join(sorted(word))
            res[sortedS].append(word)
        return list(res.values())

    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        """
        Example 1:
        Input: nums = [1,1,1,2,2,3], k = 2
        Output: [1,2]

        Example 2:
        Input: nums = [1], k = 1
        Output: [1]

        Example 3:
        Input: nums = [1,2,1,2,1,2,3,1,3,2], k = 2
        Output: [1,2]
        """
        count = {}
        for i in nums:
            count[i] = count.get(i, 0) + 1
        sortedKeys = sorted(count.items(), key = lambda x: x[1], reverse = True)[:k]
        return [k for k, v in sortedKeys]

    def encode(self, strs: list[str]) -> str:
        """
        Input: ["Hello","World"]
        Output: ["Hello","World"]
        Explanation:
        Machine 1:
        Codec encoder = new Codec();
        String msg = encoder.encode(strs);
        Machine 1 ---msg---> Machine 2

        Machine 2:
        Codec decoder = new Codec();
        String[] strs = decoder.decode(msg);
        """
        res = ""
        for word in strs:
            res += str(len(word)) + "#" + word
        return res

    def decode(self, s: str) -> list[str]:
        """
        Input: ["Hello","World"]
        Output: ["Hello","World"]
        Explanation:
        Machine 1:
        Codec encoder = new Codec();
        String msg = encoder.encode(strs);
        Machine 1 ---msg---> Machine 2

        Machine 2:
        Codec decoder = new Codec();
        String[] strs = decoder.decode(msg);
        """
        res, i = [], 0
        while i in range(len(s)):
            j = i
            while s[j] != "#":
                j += 1
            length = int(s[i : j])
            res.append(s[j + 1 : j + 1 + length])
            i = j + 1 + length
        return res

    def productExceptSelf(self, nums: list[int]) -> list[int]:
        """
        Example 1:
        Input: nums = [1,2,3,4]
        Output: [24,12,8,6]
        
        Example 2:
        Input: nums = [-1,1,0,-3,3]
        Output: [0,0,9,0,0]
        """
        prod = 1
        for i in nums:
            prod = prod * i
        lst = []
        for i in range(len(nums)):
            lst.append(prod // nums[i])
        return lst

    def productExceptSelf(self, nums: list[int]) -> list[int]:
        """
        Example 1:
        Input: nums = [1,2,3,4]
        Output: [24,12,8,6]
        
        Example 2:
        Input: nums = [-1,1,0,-3,3]
        Output: [0,0,9,0,0]
        """
        length = len(nums)
        res = [1] * length
        pre = 1
        for i in range(length):
            res[i] = pre
            pre *= nums[i]
        post = 1
        for i in range(length - 1, -1, -1):
            res[i] *= post
            post *= nums[i]
        return res

    def longestConsecutive(self, nums: list[int]) -> int:
        """
        Example 1:
        Input: nums = [100,4,200,1,3,2]
        Output: 4
        Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
        
        Example 2:
        Input: nums = [0,3,7,2,5,8,4,6,0,1]
        Output: 9
        
        Example 3:
        Input: nums = [1,0,1,2]
        Output: 3
        """
        numSet = set()
        l = 0
        longest = 0
        for n in nums:
            if n - 1 not in nums:
                length = 1
                while n + length in nums:
                    length += 1
                longest = max(longest, length)
        return longest

    def alNum(self, c: str) -> bool:
        """
        ASCII bool conversion and checks of the character
        """
        return (ord('A') <= ord(c) <= ord('Z') or
        ord('a') <= ord(c) <= ord('z') or
        ord('0') <= ord(c) <= ord('9'))

    def isPalindrome(self, s: str) -> bool:
        """
        Example 1:
        Input: s = "A man, a plan, a canal: Panama"
        Output: True
        Explanation: "amanaplanacanalpanama" is a palindrome.
        
        Example 2:
        Input: s = "race a car"
        Output: False
        Explanation: "raceacar" is not a palindrome.
        
        Example 3:
        Input: s = " "
        Output: True
        Explanation: s is an empty string "" after removing non-alphanumeric characters.
        Since an empty string reads the same forward and backward, it is a palindrome.
        """
        l, r = 0, len(s) - 1
        while l < r:
            while l < r and not self.alNum(s[l]):
                l += 1
            while l < r and not self.alNum(s[r]):
                r -= 1
            if s[l].lower() != s[r].lower():
                return False
            l, r = l + 1, r - 1
        return True

    def hasAlternatingBits(self, n: int) -> bool:
        x = n ^ (n >> 1)
        return (x & (x + 1)) == 0

    def twoSum2(numbers, target):
        """
        Example 1:
        Input: numbers = [2,7,11,15], target = 9
        Output: [1,2]
        Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
        
        Example 2:
        Input: numbers = [2,3,4], target = 6
        Output: [1,3]
        Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].
        
        Example 3:
        Input: numbers = [-1,0], target = -1
        Output: [1,2]
        Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].
        """
        length = len(numbers) - 1
        l, r = 0, length
        while l < r:
            sum = numbers[l] + numbers[r]
            if sum == target:
                return [l + 1, r + 1]
            elif sum > target:
                r -= 1
            else:
                l += 1
        return [0, 0]

    def threeSum(self, nums: list[int]) -> list[list[int]]:
        """
        Input: nums = [-1,0,1,2,-1,-4]
        Output: [[-1,-1,2],[-1,0,1]]
        Explanation:
        nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
        nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
        nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
        The distinct triplets are [-1,0,1] and [-1,-1,2].
        """
        res = []
        nums.sort()
        for i, a in enumerate(nums):
            if i > 0 and a == nums[i - 1]:
                continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                sum = a + nums[l] + nums[r]
                if sum > 0:
                    r -= 1
                elif sum < 0:
                    l += 1
                else:
                    res.append([a, nums[l], nums[r]])
                    l += 1
                    while nums[l] == nums[l - 1] and l < r:
                        l += 1
        return res

    def missingNumber(self, nums: list[int]) -> int:
        """
        Input: nums = [3,0,1]

        Output: 2

        Explanation:

        n = 3 since there are 3 numbers, so all numbers are in the range [0,3]. 2 is the missing number in the range since it does not appear in nums.
        """
        length = len(nums)
        isZero = False
        sum = 0
        for i in nums:
            sum += i
        actualSum = (length * (length + 1)) // 2
        return actualSum - sum

    def maxProfit(self, prices: list[int]) -> int:
        """
        Input: prices = [10,1,5,6,7,1]
        
        Output: 6
        """
        l, r = 0, 1
        maxP = 0
        while r < len(prices):
            if prices[l] < prices[r]:
                profit = prices[r] - prices[l]
                maxP = max(maxP, profit)
            else:
                l = r
            r += 1
        return maxP

    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Input: s = "zxyzxyz"

        Output: 3
        """
        charSet = set()
        l = 0
        res = 0
        for r in range(len(s)):
            while s[r] in charSet:
                charSet.remove(s[l])
                l += 1
            charSet.add(s[r])
            res = max(res, r - l + 1)
        return res

    def characterReplacement(self, s: str, k: int) -> int:
        """
        Input: s = "XYYX", k = 2
        
        Output: 4
        """
        count = {}
        l = 0
        res = 0
        for r in range(len(s)):
            count[s[r]] = count.get(s[r], 0) + 1
            while (r - l + 1) - max(count.values()) > k:
                count[s[l]] -= 1
                l += 1
            res = max(res, (r - l + 1))
        return res

    def minWindow(self, s: str, t: str) -> str:
        """
        Input: s = "OUZODYXAZV", t = "XYZ"

        Output: "YXAZ"
        """
        if t == "":
            return ""
        
        countT, window = {}, {}
        
        for c in t:
            countT[c] = countT.get(c, 0) + 1
            
        have, need = 0, len(countT)
        res, resLen = [-1, -1], float("infinity")
        l = 0
        for r in range(len(s)):
            c = s[r]
            window[c] = window.get(c, 0) + 1
            
            if c in countT and window[c] == countT[c]:
                have += 1
                
            while have == need:
                # update our result
                if (r - l + 1) < resLen:
                    res = [l, r]
                    resLen = (r - l + 1)
                # pop from the left of our window
                window[s[l]] -= 1
                if s[l] in countT and window[s[l]] < countT[s[l]]:
                    have -= 1
                l += 1
        
        l, r = res
        return s[l : r + 1] if resLen != float("infinity") else ""

    def isValid(self, s: str) -> bool:
        """
        Input: s = "([{}])"

        Output: True
        """
        stack = []
        closedToOpen = {']': '[', '}': '{', ')': '('}
        for c in s:
            if c in closedToOpen:
                if stack and stack[-1] == closedToOpen[c]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(c)
        return True if not stack else False

    def findMin(self, nums: list[int]) -> int:
        """
        Input: nums = [3,4,5,1,2]
        Output: 1
        Explanation: The original array was [1,2,3,4,5] rotated 3 times.
        """
        length = len(nums)
        l, r = 0, length - 1
        while l < r:
            m = (l + r) // 2
            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m
        return nums[l]

    def search(self, nums: list[int], target: int) -> int:
        """
        Example 1:
        Input: nums = [4,5,6,7,0,1,2], target = 0
        Output: 4
        Example 2:
        Input: nums = [4,5,6,7,0,1,2], target = 3
        Output: -1
        Example 3:
        Input: nums = [1], target = 0
        Output: -1
        """
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if target == nums[m]:
                return m
            if nums[l] <= nums[m]:
                if target > nums[m] or target < nums[l]:
                    l = m + 1
                else:
                    r = m - 1
            else:
                if target < nums[m] or target > nums[r]:
                    r = m - 1
                else:
                    l = m + 1
        return -1
    
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Example 1:
        Input: head = [1,2,3,4,5]
        Output: [5,4,3,2,1]
        
        Example 2:
        Input: head = [1,2]
        Output: [2,1]
        
        Example 3:
        Input: head = []
        Output: None
        """
        prev, curr = None, head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev
    
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Example 1:
        Input: list1 = [1,2,4], list2 = [1,3,4]
        Output: [1,1,2,3,4,4]
        
        Example 2:
        Input: list1 = [], list2 = []
        Output: []
        
        Example 3:
        Input: list1 = [], list2 = [0]
        Output: [0]
        """
        dummy = ListNode()
        tail = dummy

        while list1 and list2:
            if list1.val < list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        if list1:
            tail.next = list1
        elif list2:
            tail.next = list2
        
        return dummy.next
    
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        Example 1:
        Input: head = [3,2,0,-4]
        Output: True
        Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).
        
        Example 2:
        Input: head = [1,2]
        Output: True
        Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.
        """
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return False
        return True
    
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Example 1:
        Input: head = [1,2,3,4]
        Output: [1,4,2,3]
        
        Example 2:
        Input: head = [1,2,3,4,5]
        Output: [1,5,2,4,3]
        """
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        prev = slow.next = None
        while second:
            tmp = second.next
            second.next = prev
            prev = second
            second = tmp
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first, second = tmp1, tmp2

if __name__ == "__main__":
    import main
    run_all_classes(main)