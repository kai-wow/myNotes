# 常见方法

| 方法       | 出现次数 |         题号 |
|  -------   |:----:|-----------:|
| 双指针法    |  2   | 11, 31, 32, 42 |
| 单调栈      |  1   |         42 |
| 栈          |  1   |      20, 32|
| 动态规划    |  3   |  22, 32, 42 |
|确定有限状态机|  1   |         8 |
|哈希表       |  1   |       3, 20 |

# 常见题型
## 括号题
| 题号           | 方法           |
|  -------      |:---------------|
| 20 有效的括号  | 栈             |
| 22 括号生成    | 1.动态规划<br/>2.递归法   | 
| 32 最长有效括号| 1.动态规划<br/>2.栈 <br/>3.双指针+正向逆向结合|
## 子字符
| 题号           | 方法           |
|  -------      |:---------------|
| 3 无重复字符的最长子串  | 哈希表             |
|      | 1. <br/>2.    | 
|      | 1. <br/>2.   |

# Python刷题中
## 390 消除游戏
### 1. 题目
列表 arr 由在范围 [1, n] 中的所有整数组成，并按严格递增排序。请你对 arr 应用下述算法：

* 从左到右，删除第一个数字，然后每隔一个数字删除一个，直到到达列表末尾。
* 重复上面的步骤，但这次是从右到左。也就是，删除最右侧的数字，然后剩下的数字每隔一个删除一个。
* 不断重复这两步，从左到右和从右到左交替进行，直到只剩下一个数字。

给你整数 n ，返回 arr 最后剩下的数字。

示例 1：

输入：n = 9\
输出：6\
解释：\
arr = [1, ~~2~~, 3, ~~4~~, 5, ~~6~~, 7, ~~8~~, 9]\
arr = [2, ~~4~~, 6, ~~8~~]\
arr = [~~2~~, 6]\
arr = [6]

提示： 1 <= n <= 10e9
### 2. 考点与优秀答案
#### 考点
1. 因为测试用例输入可大至 10e9，所以挨个循环delete是不可行的，得找规律/做数学题。

(1) **找规律**\
***思路***：每个回合更新和记录head变量，当数组的长度变为1时，head就是输出的数

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

# 我修改后的代码
class Solution:
    def lastRemaining(self, n: int) -> int:
        head = 1
        len = n
        left = True
        step = 0
        round = 0
        while len > 1:
            if len % 2 == 1 or (len % 2 == 0 and left):
                step = 2 ** round
                head += step

            len = len // 2
            left = not left
            round += 1
        return head
```

2. 如何正确按照loc删除元素（删除元素后，列表长度会变化）？
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

- 如何更新leftMax 和 rightMax\
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
    时间复杂度：O(n)。\
    空间复杂度：O(n)。\


#### 解法 2  单调栈
**放弃这个方法了，栈不好理解**
除了计算并存储每个位置两边的最大高度以外，也可以用单调栈计算能接的雨水总量。

维护一个单调栈，单调栈存储的是下标，满足从栈底到栈顶的下标对应的数组 height中的元素递减。

从左到右遍历数组，遍历到下标 i 时，如果栈内至少有两个元素，记栈顶元素为 top 的下面一个元素是 left，则一定有 height[left]≥height[top]。如果 height[i]>height[top]，则得到一个可以接雨水的区域，该区域的宽度是 i−left−1，高度是 min⁡(height[left],height[i])−height[top]，根据宽度和高度即可计算得到该区域能接的雨水量。

为了得到 left，需要将 top 出栈。在对 top计算能接的雨水量之后，left 变成新的 top，重复上述操作，直到栈变为空，或者栈顶下标对应的 height 中的元素大于或等于 height[i]

在对下标 i 处计算能接的雨水量之后，将 i 入栈，继续遍历后面的下标，计算能接的雨水量。遍历结束之后即可得到能接的雨水总量。

- 复杂度分析\
    时间复杂度：O(n)\
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
- 复杂度分析\
    时间复杂度：O(n)\
    空间复杂度：O(1)
## 11 盛最多水的容器
### 1. 题目
给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。

找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

返回容器可以储存的最大水量。

示例 1：
!["示例图"](https://aliyun-lc-upload.oss-cn-hangzhou.aliyuncs.com/aliyun-lc-upload/uploads/2018/07/25/question_11.jpg)
输入：[1,8,6,2,5,4,8,3,7]\
输出：49 
### 2. 考点与优秀答案
#### 考点
如何避免 O(n^2) 的时间复杂度，在一次循环里得到答案

#### 优秀答案：双指针法
题目中的示例为：
```
[1, 8, 6, 2, 5, 4, 8, 3, 7]
 ^                       ^
```
在初始时，左右指针分别指向数组的左右两端，它们可以容纳的水量为 min(1, 7) * 8 = 8。

此时我们需要移动一个指针。由于容纳的水量的高度 h = min(height[l], height[r]) ，如果我们移动较高的那个指针，那么
「高度」不会增加，容器的宽度会减小，那么容积一定会减小。因此，我们移动 数字较小的那个指针。

所以，在本例中我们将左指针向右移动：
```
[1, 8, 6, 2, 5, 4, 8, 3, 7]
    ^                    ^
```
此时可以容纳的水量为 min(8, 7) * 7 = 49。由于右指针对应的数字较小，我们移动右指针：
```
[1, 8, 6, 2, 5, 4, 8, 3, 7]
    ^                 ^
```
此时可以容纳的水量为 min(8, 3) * 6 = 18。由于右指针对应的数字较小，我们移动右指针：

```
[1, 8, 6, 2, 5, 4, 8, 3, 7]
    ^              ^
```
此时可以容纳的水量为 min(8, 8) * 5 = 40。两指针对应的数字相同，我们可以任意移动一个.

以此类推，在我们移动指针的过程中，计算到的最多可以容纳的数量为 49，即为最终的答案。


- 复杂度分析：\
时间复杂度：O(N)\
空间复杂度：O(1)
```python
# 优秀答案
class Solution:
    def maxArea(self, height) -> int:
        l, r = 0, len(height) - 1
        ans = 0
        while l < r:
            area = min(height[l], height[r]) * (r - l)
            ans = max(ans, area)
            if height[l] <= height[r]:
                l += 1
            else:
                r -= 1
        return ans

# 我的答案
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        h = min(height[left], height[right])
        ans = h * (right - left)

        while left < right:
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
            h = min(height[left], height[right])
            ans = max(ans, h * (right - left))
        return ans
```
## 31 下一个排列
### 1. 题目
整数数组的一个 排列  就是将其所有成员以序列或线性顺序排列。

例如，arr = [1,2,3] ，以下这些都可以视作 arr 的排列：[1,2,3]、[1,3,2]、[3,1,2]、[2,3,1] 。
整数数组的 下一个排列 是指其整数的下一个字典序更大的排列。更正式地，如果数组的所有排列根据其字典顺序从小到大排列在一个容器中，那么数组的
下一个排列 就是在这个有序容器中排在它后面的那个排列。如果不存在下一个更大的排列，那么这个数组必须重排为字典序最小的排列（即，其元素按升序排列）。

例如，arr = [1,2,3] 的下一个排列是 [1,3,2] 。
类似地，arr = [2,3,1] 的下一个排列是 [3,1,2] 。
而 arr = [3,2,1] 的下一个排列是 [1,2,3] ，因为 [3,2,1] 不存在一个字典序更大的排列。
给你一个整数数组 nums ，找出 nums 的下一个排列。

必须 原地 修改，只允许使用额外常数空间。

示例 1：\
输入：nums = [1,2,3]\
输出：[1,3,2]

示例 2：\
输入：nums = [3,2,1]\
输出：[1,2,3]

示例 3：\
输入：nums = [1,1,5]\
输出：[1,5,1]

提示：\
1 <= nums.length <= 100\
0 <= nums[i] <= 100
### 2. 考点与优秀答案
#### 考点
字典序：类比英语字典里的单词排序，即先按照第一个字母、以 a、b、c……z 的顺序排列；如果第一个字母一样，那么比较第二个、第三个乃至后面的字母。
如果比到最后两个单词不一样长（比如，sigh 和 sight），那么把短者排在前。

本题即参考字典序 对数组进行排序。
#### 优秀答案
方法一：两遍扫描 & 双指针法

注意到下一个排列总是比当前排列要**大**（除非该排列已是最大），且是比它**大的幅度最小**的排列。

具体操作：\
举两个示例：\
```
[1,2,5,4,3] 的下一排列为：
[1,3,2,4,5]
   ^
```

```
[4,5,2,6,3,1] 的下一个排列是：
[4,5,3,1,2,6]
     ^
```
可以看出，若要找出下一排列，需要尽可能小地变动数列，即，只变动数列的右半部分，而这右半部分的边界在于，降序的**中断点**，即，
在该数的右边的排列为降序（只改变这部分没法让数列变大），而加上该数后，这个子数列不再是降序（改变这个数列能让原数列变大地最小）。

**找到中断点后，如何改变数列？**\

要让变大幅度最小，中断点需要被替换为，他右边的子序列里 比他大的数里最小的数。因为右边子序列为降序，因此从后往前循环查找到的
第一个大于中断点的数即为要被替换的数。
```
[4,5,2,6,3,1] 
     ^   ^
```
当我们完成交换后，排列变为 
```
[4,5,3,6,2,1]
     ^   ^
```
此时我们按升序重排中断点右边的序列（不含中断点），这样能使得新序列比原序列大，且增大的幅度最小。 
```
[4,5,3,1,2,6]
     ^
```
**如何重排中断点右边的序列？** \

可以发现，替换中断点后，右边的新的子序列依旧为降序，要将降序序列更改为升序序列，可以使用**双指针**法反转该子序列。
而无需遍历一次进行排序。

- 复杂度分析：\
时间复杂度：O(N)\
空间复杂度：O(1)

```python
# 优秀答案
class Solution:
    def nextPermutation(self, nums) -> None:
        i = len(nums) - 2  # 从倒数第二个数开始
        # 循环直到 nums[i:] 后面的数不是完全降序
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        # 如果 i 不是第一个数
        if i >= 0:
            j = len(nums) - 1
            # 从后往前（从小往大）循环，直到找到比 nums[i] 更大的数（一定的最小的 大于nums[i]的数）
            while j >= 0 and nums[i] >= nums[j]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i] # 更换两个数的位置
        # 将 nums[i+1:] 子列表的数的顺序完全倒过来：双指针法！！
        left, right = i + 1, len(nums) - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
# 我的答案
class Solution:
    def nextPermutation(self, nums) -> None:
        des = True  # 降序排列

        margin = len(nums) - 2
        while des and margin >= 0: 
            if nums[margin] >= nums[margin+1]:
                margin -= 1
            else:
                des = False
        
        head = len(nums) - 1
        if margin >= 0:
            while head > margin and nums[head] <= nums[margin]:
                head -= 1
            nums[head], nums[margin] = nums[margin], nums[head]
        
        left, right = margin + 1, len(nums) - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
```
## 8 字符串转换整数 (atoi)
### 1. 题目
请你来实现一个 myAtoi(string s) 函数，使其能将字符串转换成一个 32 位有符号整数（类似 C/C++ 中的 atoi 函数）。

函数 myAtoi(string s) 的算法如下：

    读入字符串并丢弃无用的前导空格\
    检查下一个字符（假设还未到字符末尾）为正还是负号，读取该字符（如果有）。 确定最终结果是负数还是正数。 如果两者都不存在，则假定结果为正。\
    读入下一个字符，直到到达下一个非数字字符或到达输入的结尾。字符串的其余部分将被忽略。\
    将前面步骤读入的这些数字转换为整数（即，"123" -> 123， "0032" -> 32）。如果没有读入数字，则整数为 0 。必要时更改符号（从步骤 2 开始）。\
    如果整数数超过 32 位有符号整数范围 [−231,  231 − 1] ，需要截断这个整数，使其保持在这个范围内。具体来说，小于 −231 的整数应该被固定为 −231 ，大于 231 − 1 的整数应该被固定为 231 − 1 。\
    返回整数作为最终结果。\

注意：\
    本题中的空白字符只包括空格字符 ' ' 。\
    除前导空格或数字后的其余字符串外，请勿忽略 任何其他字符。\


示例 1：\
```
输入：s = "42"
输出：42
解释：加粗的字符串为已经读入的字符，插入符号是当前读取的字符。
第 1 步："42"（当前没有读入字符，因为没有前导空格）
         ^
第 2 步："42"（当前没有读入字符，因为这里不存在 '-' 或者 '+'）
         ^
第 3 步："42"（读入 "42"）
           ^
解析得到整数 42 。
由于 "42" 在范围 [-2^31, 2^31 - 1] 内，最终结果为 42 。
```
示例 2：
```
输入：s = "   -42"
输出：-42
解释：
第 1 步："   -42"（读入前导空格，但忽视掉）
            ^
第 2 步："   -42"（读入 '-' 字符，所以结果应该是负数）
             ^
第 3 步："   -42"（读入 "42"）
               ^
解析得到整数 -42 。
由于 "-42" 在范围 [-2^31, 2^31 - 1] 内，最终结果为 -42 。
```
示例 3：
```
输入：s = "4193 with words"
输出：4193
解释：
第 1 步："4193 with words"（当前没有读入字符，因为没有前导空格）
         ^
第 2 步："4193 with words"（当前没有读入字符，因为这里不存在 '-' 或者 '+'）
         ^
第 3 步："4193 with words"（读入 "4193"；由于下一个字符不是一个数字，所以读入停止）
             ^
解析得到整数 4193 。
由于 "4193" 在范围 [-2^31, 2^31 - 1] 内，最终结果为 4193 。
```
提示：\
    0 <= s.length <= 200\
    s 由英文字母（大写和小写）、数字（0-9）、' '、'+'、'-' 和 '.' 组成\

### 2. 考点与优秀答案
#### 考点
溢出（主要考核 c 和 c++ 中的 int 溢出问题

#### 优秀答案
##### 自动机/确定有限状态机（deterministic finite automaton, DFA）
字符串处理往往涉及复杂的流程，如果直接if else，容易写出极其臃肿的代码。

因此，为了有条理地分析每个输入字符的处理方法，我们可以使用**自动机**这个概念。**DFA方法的普遍性和可维护性很高**。

!["自动机状态转移图"](https://assets.leetcode-cn.com/solution-static/8/fig1.png)

我们的程序在每个时刻有一个状态 s，每次从序列中输入一个字符 c，并根据字符 c 转移到下一个状态 s'。根据状态转移规则制定如下表格。
> 下表类似状态转移矩阵，第一列/index 为当前状态(s)，第一行/col (c)为输入的字符，表格内部为 下一个状态(s')。注意需要枚举，覆盖所有情况。

|          | ' '    |   +/-|   number|  other |
|-------   |:----:  |:----:|   :----:|-------:|
| start    |  start |signed| in_number| end |
| signed   |  end   |  end | in_number| end |
| in_number|  end   |  end | in_number| end |
| end      |  end   |  end | end      | end |

另外自动机也需要记录当前已经输入的数字，只要在 s' 为 in_number 时，更新我们输入的数字，即可最终得到输入的数字。

```python
INT_MAX = 2 ** 31 - 1
INT_MIN = -2 ** 31

class Automaton:
    def __init__(self):
        self.state = 'start'
        self.sign = 1
        self.ans = 0
        self.table = {
            'start': ['start', 'signed', 'in_number', 'end'],
            'signed': ['end', 'end', 'in_number', 'end'],
            'in_number': ['end', 'end', 'in_number', 'end'],
            'end': ['end', 'end', 'end', 'end'],
        }
        
    def get_col(self, c): # 判断输入为 c 时对应 self.table 的第几列
        if c.isspace():
            return 0
        if c == '+' or c == '-':
            return 1
        if c.isdigit():
            return 2
        return 3

    def get(self, c):
        self.state = self.table[self.state][self.get_col(c)]  # 获取输入为 c 时的 下一状态
        if self.state == 'in_number':
            self.ans = self.ans * 10 + int(c)
            self.ans = min(self.ans, INT_MAX) if self.sign == 1 else min(self.ans, -INT_MIN)
        elif self.state == 'signed':
            self.sign = 1 if c == '+' else -1

class Solution:
    def myAtoi(self, str: str) -> int:
        automaton = Automaton()
        for c in str:
            automaton.get(c)
        return automaton.sign * automaton.ans

```


##### python 正则（但违背出题本意）
```python
class Solution:
    def myAtoi(self, s: str) -> int:
        return max(min(int(*re.findall('^[\+\-]?\d+', s.lstrip())), 2**31 - 1), -2**31)
```

以上语句拆开：

```python
import re
class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX = 2**31 - 1    
        INT_MIN = -2**31
        s = s.lstrip()      # 清除左边多余的空格
        num_re = re.compile(r'^[\+\-]?\d+')   # 设置正则规则
        num = num_re.findall(s)   #查找匹配的内容，返回的是列表
        num = int(*num)   # 用*对列表解包并且转换成整数（int不支持列表）
        return max(min(num,INT_MAX),INT_MIN)    # 返回值
```
- 使用正则表达式
  - ^：匹配字符串开头，
  - []: 表示匹配括号内的任一字符
  - [\+\-]：表示匹配一个+字符或-字符，
  - ?：表示前面一个字符可有可无，
  - \d：表示一个数字，0-9的范围，
  - +：表示前面一个字符出现一次或多次，
  - \D：一个非数字字符
  - *：解包操作，如 *[1,2,3] 会输出 1 2 3
- max(min(数字, 2**31 - 1), -2**31) 用来防止结果越界
## 20 有效的括号
### 1. 题目
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。

有效字符串需满足：\
    左括号必须用相同类型的右括号闭合。
    左括号必须以正确的顺序闭合。

示例 1：\
输入：s = "()"\
输出：true

### 2. 考点与优秀答案
#### 考点
栈。\
#### 优秀答案
- 算法原理
    - **栈**先入后出特点恰好与本题括号排序特点一致。
    - 建立**哈希表 dic** 构建左右括号对应关系：key 左括号，valuevaluevalue 右括号；这样查询 2 个括号是否对应只需 **O(1)** 时间复杂度
【简单思路】
如果字符串为空/奇数，则true\
遍历字符串 (可以从前往后，或从后往前)
    - 如果是左括号，则直接入栈
    - 如果是右括号，则将其与栈顶元素进行匹配
        如果此时栈为空，则说明右括号多，false
        如果不匹配，false
        如果匹配，则出栈
    - 最后检查栈是否为空，若不为空，说明左括号多，false

- 复杂度分析
    时间复杂度 O(N)
    空间复杂度 O(N)：哈希表和栈使用线性的空间大小。

```python
# 优秀代码
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s)%2 == 1: 
            return False
        dic = {'{': '}',  '[': ']', '(': ')', '?': '?'}
        stack = ['?']
        for ch in s: # (从前往后遍历字符)
            if ch in dic:  # 即识别左括号（key）
                stack.append(ch)
            elif dic[stack.pop()] != ch:  # 若不是左括号，则和 栈中最后一个元素对应
                return False  # 不匹配则一定为 false
        return len(stack) == 1 # 最后 stack 里是个 '?'

# 我的代码
class Solution:
    def isValid(self, s: str) -> bool:
        l1 = list(s)
        l2 = []
        l2.append(l1.pop())
        while len(l1) > 0:  # (从后往前遍历字符)
            if len(l2) > 0 and self.isMatch(l1[-1], l2[-1]):
                l2.pop()
                l1.pop()
            else:
                l2.append(l1.pop())

        if len(l1) == 0 and len(l2) == 0:
            return True
        return False


    def isMatch(self, l, r):
        dic = {'(': ')', '[': ']', '{': '}'}
        if l in dic:
            return dic[l] == r
        return False
```
## 22 括号生成 TODO 没做完
### 1. 题目
数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。

示例 1：\
输入：n = 3\
输出：["((()))","(()())","(())()","()(())","()()()"]

示例 2：\
输入：n = 1\
输出：["()"]
### 2. 考点与优秀答案
#### 考点
#### 优秀答案
##### 动态规划

##### 递归/回溯算法
```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        if n == 1:
            return list({'()'})
        res = set()    # 去重
        for i in self.generateParenthesis(n - 1):
            for j in range(len(i) + 2):
                res.add(i[0:j] + '()' + i[j:])
        return list(res)
```
## 32 最长有效括号 TODO 没做完
### 1. 题目
给你一个只包含 '(' 和 ')' 的字符串，找出最长有效（格式正确且连续）括号子串的长度。


示例 1：

输入：s = "(()"
输出：2
解释：最长有效括号子串是 "()"

示例 2：

输入：s = ")()())"
输出：4
解释：最长有效括号子串是 "()()"

### 2. 考点与优秀答案
#### 考点
#### 优秀答案
##### 方法一：动态规划

##### 方法二：栈

##### 方法三：双指针+正向逆向结合
## 3 无重复字符的最长子串
### 1. 题目
给定一个字符串 s ，请你找出其中不含有重复字符的 最长子串 的长度。

示例 1:\
输入: s = "abcabcbb"\
输出: 3 

示例 2:
输入: s = "pwwkew"\
输出: 3




### 2. 考点与优秀答案
#### 考点
哈希表
#### 优秀答案
##### 字典（ 哈希表 ）
用字典（哈希表）储存某字符上一次出现的index，则可以只循环一次。

复杂度分析:
    - 时间复杂度：O(N)
    - 空间复杂度：$O(|\Sigma|)$，其中 $\Sigma$ 表示字符集（即字符串中可以出现的字符），$|\Sigma|$表示字符集的大小。在本题中没有明确说明字符集，因此可以默认为所有 ASCII 码在 [0, 128) 内的字符，即 $|\Sigma|$ = 128。

```python
class Solution:
    def lengthOfLongestSubstring(self, s):
        st = {}
        i, ans = 0, 0
        for j in range(len(s)):
            if s[j] in st:
                i = max(st[s[j]], i)
            ans = max(ans, j - i + 1)
            st[s[j]] = j + 1
        return ans

# 我的答案，两次循环
class Solution:
    def lengthOfLongestSubstring(self, s: str):
        if len(s) <= 1:
            return len(s)
        left = 0
        ans = 1
        
        for right in range(1, len(s)):
            repeat = False
            for j in range(right-1, left-1, -1):
                if s[right] == s[j]:
                    repeat = True
                    break
            if repeat:
                left = j + 1
            ans = max(ans, right - left + 1)
        return ans

```


## ？
### 1. 题目
### 2. 考点与优秀答案
#### 考点
#### 优秀答案