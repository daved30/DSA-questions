from collections import Counter, defaultdict, OrderedDict

import inspect
import re
import ast

def parse_input_line(input_line: str):
    """
    Parse an input line like:
    'numbers = [2,7,11,15], target = 9'
    into a dict: {'numbers': [2,7,11,15], 'target': 9}
    """
    args_dict = {}
    # Split only on commas that separate key=value pairs (not inside lists)
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

def run_all_functions(module):
    # Collect functions in the order they appear in the file
    funcs = OrderedDict(
        sorted(
            inspect.getmembers(module, inspect.isfunction),
            key=lambda x: x[1].__code__.co_firstlineno
        )
    )

    for name, func in funcs.items():
        doc = func.__doc__
        if not doc:
            continue

        print(f"\nFunction: {name}")
        print("Docstring:", doc.strip())

        # Find all Input/Output pairs in the docstring
        inputs = re.findall(r"Input:\s*(.*)", doc)
        outputs = re.findall(r"Output:\s*(.*)", doc)

        for idx, input_line in enumerate(inputs, start=1):
            try:
                args_dict = parse_input_line(input_line)
                result = func(**args_dict)

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


def validParanthesis(s):
    stack, mapping = [], {')': '(', '}': '{', ']': '['}
    for ch in s:
        if ch in mapping:
            if not stack or stack.pop() != mapping[ch]:
                return False
        elif ch in mapping.values():
            stack.append(ch)
    return not stack

def mergeIntervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval.copy())
        else:
            merged[-1] = [merged[-1][0], max(merged[-1][1], interval[1])]
    return merged

def shiftZeros(arr):
    left = 0
    for right in range(len(arr)):
        if arr[right] != 0:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
    return arr

def groupAnagrams(strs):
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

def groupAnagramsNeetCodeSolution(strs):
    res = defaultdict(list)
    for word in strs:
        sortedS = "".join(sorted(word))
        res[sortedS].append(word)
    return list(res.values())

def topKFrequent(nums, k):
    count = {}
    for i in nums:
        count[i] = count.get(i, 0) + 1
    sorted_items = sorted(count.items(), key = lambda x: x[1], reverse = True)[:k]
    return [k for k, v in sorted_items]

def encodeEZApproach(strs):
    if len(strs) <= 1:
        return [strs]
    for word in strs:
        encStr = "#".join(strs)
    return encStr

stringValEnc = encodeEZApproach(["Hello","World"])

def decodeEZApproach(s):
    splitString = s.split("#")
    lst = [word for word in splitString]
    return lst

stringValDec = decodeEZApproach(stringValEnc)

def encode(strs):
    res = ""
    for s in strs:
        res += str(len(s)) + "#" + s
    return res

stringValEnc = encode(["Hello","World"])

def decode(s):
    res, i = [], 0
    
    while i < len(s):
        j = i
        while s[j] != "#":
            j+=1
        length = int(s[i:j])
        res.append(s[j + 1: j + 1 + length])
        i = j + 1 + length
    return res

stringValDec = decode(stringValEnc)

def productExceptSelf(nums):
    prod = 1
    for i in nums:
        prod = prod * i
    lst = []
    for i in range(len(nums)):
        lst.append(prod // nums[i])
    return lst

def productExceptSelf(nums):
    # Input: nums = [1,2,4,6] Output: [48,24,12,8]
    res = [1] * len(nums)
    prefix = 1
    for i in range(len(nums)):
        res[i] = prefix
        prefix *= nums[i]
    postfix = 1
    for i in range(len(nums) - 1, -1, -1):
        res[i] *= postfix
        postfix *= nums[i]
    return res

def longestConsecutive(nums):
    numS = set(nums)
    longest = 0
    for n in numS:
        if (n - 1) not in numS:
            length = 1
            while (n + length) in numS:
                length += 1
            longest = max(length, longest)
    return longest

def alNum(c):
    return (ord('A') <= ord(c) <= ord('Z') or
            ord('a') <= ord(c) <= ord('z') or
            ord('0') <= ord(c) <= ord('9'))

def isPalindrome(s):
    # Input: s = "Was it a car or a cat I saw?" Output: true
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not alNum(s[l]):
            l += 1
        while r > l and not alNum(s[r]):
            r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l, r = l + 1, r - 1
    return True

def hasAlternatingBits(n):
    x = n ^ (n >> 1)
    return (x & (x + 1)) == 0

def twoSum2(numbers, target):
    """
    Input: numbers = [2,7,11,15], target = 9
    Output: [1,2]
    Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
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

def threeSum(nums):
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

def missingNumber(nums):
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

def maxProfit(prices):
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

def lengthOfLongestSubstring(s):
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

def characterReplacement(s, k):
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

def minWindow(s, t):
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

def isValid(s):
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

def findMin(nums):
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

def search(nums, target):
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

if __name__ == "__main__":
    import main
    run_all_functions(main)