# 刷题中
## 390 消除游戏
### 1. 题目
列表 arr 由在范围 [1, n] 中的所有整数组成，并按严格递增排序。请你对 arr 应用下述算法：

* 从左到右，删除第一个数字，然后每隔一个数字删除一个，直到到达列表末尾。
* 重复上面的步骤，但这次是从右到左。也就是，删除最右侧的数字，然后剩下的数字每隔一个删除一个。
* 不断重复这两步，从左到右和从右到左交替进行，直到只剩下一个数字。

给你整数 n ，返回 arr 最后剩下的数字。

示例 1：

输入：n = 9
输出：6
解释：
arr = [1, ~~2~~, 3, ~~4~~, 5, ~~6~~, 7, ~~8~~, 9]
arr = [2, ~~4~~, 6, ~~8~~]
arr = [~~2~~, 6]
arr = [6]

提示： 1 <= n <= 10e9
### 2. 考点与优秀答案
#### 考点
1. 因为测试用例输入可大至 10e9，所以挨个循环delete是不可行的，得找规律/做数学题。

(1) **找规律**\
***思路***：每个回合更新和记录head变量，当数组的总数变为1时，head就是输出的数

例如：\
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24\
2 4 6 8 10 12 14 16 18 20 22 24\
2 6 10 14 18 22\
6 14 22\
14

**何时更新head变量？**

- 当我们从左边开始移除时
- 当我们从右边开始移除并且剩余的数的总数为奇数时\
比如 ~~2~~ 4 ~~6~~ 8 ~~10~~，移除10，6，2，head被移除并且变为4\
比如 2 ~~4~~ 6 ~~8~~ 10 ~~12~~，移除12，8，4，head仍然是2

**如何移动head变量？**

我们发现每次移动head只会往右移动一步，而相邻的两个数之间的距离是有规律的：\
- 第一行（第0次移除），step=1
- 第二行（第1次移除），step=2
- 第三行（第2次移除），step=4
- 第四行（第3次移除），step=8\
即，移动步长为 2^round

**因此可得到代码逻辑**\
```python
# 我修改后的代码
class Solution:
    def lastRemaining(self, n: int) -> int:
        self.head = 1
        self.len = n
        self.left = True
        self.step = 0
        round = 0
        while self.len > 1:
            if self.len % 2 == 1 or (self.len % 2 == 0 and self.left):
                self.step = 2 ** round
                self.head += self.step

            self.len = self.len // 2
            self.left = not self.left
            round += 1
        return self.head
# 优秀代码
class Solution:
    def lastRemaining(self, n: int) -> int:
        head = 1
        step = 1
        left = True
        
        while n > 1:
            # 从左边开始移除 or（从右边开始移除，数列总数为奇数）
            if left or n % 2 != 0:
                head += step
            
            step <<= 1 # 步长 * 2, 此次为二进制左移操作符
            n >>= 1 # 总数 / 2，此次为二进制右移操作符
            left = not left #取反移除方向

        return head
```

1. 如何正确按照loc删除元素（删除元素后，列表长度会变化）？
```python
def elim_left2right(self):
    i = 0
    while i < len(self.arr):
        del self.arr[i]
        i += 1  # 从前往后 隔一步删一个（loc会变，因为从前往后删，所以少减1）

def elim_right2left(self):
    i = len(self.arr) - 1
    while i > 0:
        del self.arr[i]
        i -= 2  # 从后往前 隔一步删一个（loc不会变，因为从后删）
```
## 42 接雨水
2022.4.1 0.00-2.00 九坤笔试遇到这道题 （牛客网）
### 1. 题目
给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

示例 1：\
输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]\
输出：6
 
示例 2：\
输入：height = [4,2,0,3,2,5]\
输出：9
 
提示：\
    n == height.length
    1 <= n <= 2 * 10e4
    0 <= height[i] <= 10e5

### 2. 考点与优秀答案
#### 解法 1  动态规划
- 思路
在loc为 i 的柱子上，能累积的雨水的最大高度 = $min(左边的最大高度, 右边的最大高度) - 自身的高度$

因此，对于数组 height 中的每个元素，分别向左和向右扫描并记录**左边**和**右边的最大高度**，然后计算每个下标位置能接的雨水量。

![接雨水leetcode实例图](https://assets.leetcode-cn.com/solution-static/42/1.png)

- 如何更新leftMax 和 rightMax
显然，leftMax[0]=height[0]，rightMax[n−1]=height[n−1]

当 1≤i≤n−1 时，leftMax[i]=max⁡(leftMax[i−1],height[i])

当 0≤i≤n−2 时，rightMax[i]=max⁡(rightMax[i+1],height[i])

- 代码
```python
# 我的代码
class Solution:
    def trap(self, height) -> int:
        # 动态规划
        leftMax = height.copy()  
        rightMax = height.copy()  # 一定要 copy , 否则指针直接指向 height 的位置，最后 leftMax rightMax 和 height 会是同一个列表
        i = 1
        while i < len(height):
            if height[i] < leftMax[i-1]:  # 正向循环
                leftMax[i] = leftMax[i-1]

            if height[-i-1] < rightMax[-i]:  # 负向循环
                rightMax[-i-1] = rightMax[-i]
            i += 1

        rain = 0
        for n in range(len(height)):
            low = min(rightMax[n], leftMax[n])
            rain += low - height[n]
        return rain

# 优秀代码
class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0
        
        n = len(height)
        leftMax = [height[0]] + [0] * (n - 1)
        for i in range(1, n):
            leftMax[i] = max(leftMax[i - 1], height[i])

        rightMax = [0] * (n - 1) + [height[n - 1]]
        for i in range(n - 2, -1, -1):
            rightMax[i] = max(rightMax[i + 1], height[i])

        ans = sum(min(leftMax[i], rightMax[i]) - height[i] for i in range(n))
        return ans

```
- 复杂度分析
    时间复杂度：O(n)。
    空间复杂度：O(n)。需要创建两个长度为 n 的数组 leftMax 和 rightMax。


#### 解法 2  单调栈
**放弃这个方法了，栈不好理解**
除了计算并存储每个位置两边的最大高度以外，也可以用单调栈计算能接的雨水总量。

维护一个单调栈，单调栈存储的是下标，满足从栈底到栈顶的下标对应的数组 height中的元素递减。

从左到右遍历数组，遍历到下标 i 时，如果栈内至少有两个元素，记栈顶元素为 top 的下面一个元素是 left，则一定有 height[left]≥height[top]。如果 height[i]>height[top]，则得到一个可以接雨水的区域，该区域的宽度是 i−left−1，高度是 min⁡(height[left],height[i])−height[top]，根据宽度和高度即可计算得到该区域能接的雨水量。

为了得到 left，需要将 top 出栈。在对 top计算能接的雨水量之后，left 变成新的 top，重复上述操作，直到栈变为空，或者栈顶下标对应的 height 中的元素大于或等于 height[i]

在对下标 i 处计算能接的雨水量之后，将 i 入栈，继续遍历后面的下标，计算能接的雨水量。遍历结束之后即可得到能接的雨水总量。

- 复杂度分析\
    时间复杂度：O(n)

    空间复杂度：O(n)

#### 解法 3 双指针
我们先明确几个变量的意思：

left_max：左边的最大值，它是从左往右遍历找到的
right_max：右边的最大值，它是从右往左遍历找到的
left：从左往右处理的当前下标
right：从右往左处理的当前下标

定理一：在某个位置i处，它能存的水，取决于它左右两边的最大值中较小的一个。

定理二：当我们从左往右处理到left下标时，左边的最大值left_max对它而言是可信的，但right_max对它而言是不可信的。（见下图，由于中间状况未知，对于left下标而言，right_max未必就是它右边最大的值）

定理三：当我们从右往左处理到right下标时，右边的最大值right_max对它而言是可信的，但left_max对它而言是不可信的。
```
                                   right_max
 left_max                             __
   __                                |  |
  |  |__   __??????????????????????  |  |
__|     |__|                       __|  |__
        left                      right
```
对于位置left而言，它左边最大值一定是left_max，右边最大值“大于等于”right_max，这时候，如果left_max\<right_max成立，那么它就知道自己能存多少水了。无论右边将来会不会出现更大的right_max，都不影响这个结果。 所以当left_max<right_max时，我们就希望去处理left下标，反之，我们希望去处理right下标。

```python
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
```