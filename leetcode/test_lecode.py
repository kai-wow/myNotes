
class Solution:
    def trap(self, height) -> int:
        # 动态规划
        leftMax = height.copy()
        rightMax = height.copy()
        i = 1
        while i < len(height):
            if height[i] < leftMax[i-1]:
                leftMax[i] = leftMax[i-1]
                print(leftMax[i])
            if height[-i-1] < rightMax[-i]:
                rightMax[-i-1] = rightMax[-i]
                print(rightMax[i])
            i += 1

        rain = 0
        for n in range(len(height)):
            low = min(rightMax[n], leftMax[n])
            rain += low - height[n]
        return rain

class Solution:
    def trap(self, height) -> int:
        left = 0
        right = len(height) - 1
        left_max = 0
        right_max = 0

        ans = 0
        while left <= right:
            if left_max < right_max:
                ans += max(0, left_max - height[left])
                left_max = max(left_max, height[left])
                left += 1
            else:
                ans += max(0, right_max - height[right])
                right_max = max(right_max, height[right])
                right -= 1
        return ans


class Solution:
    def myAtoi(self, s: str) -> int:
        while s[0] == ' ':
            s = s[1:]
        negative = False
        if s[0] == '-':
            negative =  True
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]
        
        while s[0] == '0':
            s = s[1:]
        i = 0
        while i<len(s) and s[i] in ['0', '1','2','3','4','5','6','7','8','9']:
            i += 1
        s = s[:i]
        ans = int(s)
        if negative:
            ans = -ans
        return ans

class Solution:
    def myAtoi(self, s: str) -> int:
        negative = False
        i = 0
        ans = ''
        
        while i < len(s) and s[i] == ' ':
            i += 1
        if i < len(s) and s[i] in ['+', '-']:
            if  s[i] == '-':
                negative =  True
            i += 1
        while i < len(s) and s[i] in ['0', '1','2','3','4','5','6','7','8','9']:
            ans += s[i] 
            i += 1
        if ans == '':
            ans = 0
        else:
            ans = int(ans)
            if negative:
                ans = -ans
            if ans > 2**31 - 1:
                ans = 2**31 - 1
            elif ans < -2**31:
                ans = -2**31
        return ans

s = "words and 987"
a = Solution().myAtoi(s)
print(a)