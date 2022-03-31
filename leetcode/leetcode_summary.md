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

(1) **做数学题**\


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