
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

height = [0,1,0,2,1,0,1,3,2,1,2,1]
an = Solution().trap(height)
print(an)