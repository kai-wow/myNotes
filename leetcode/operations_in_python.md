# 位运算
https://leetcode.cn/problems/power-of-two/solution/5chong-jie-fa-ni-ying-gai-bei-xia-de-wei-6x9m/

常用位操作

1. 判断奇偶
(x & 1) == 1 ---等价---> (x % 2 == 1)
(x & 1) == 0 ---等价---> (x % 2 == 0)

2. x / 2 ---等价---> x >> 1
3. x &= (x - 1) ------> 把x最低位的二进制1给去掉
4. x & -x -----> 得到最低位的1
5. x & ~x -----> 0


## & 与
只有两个值对应位置都取1时，结果取1，否则取0
eg. (101) & (110) = (100) 右边两位对应的值不全为1，因而取0，第一位都为1，因而取1.

拓展：
- n & (n-1): 将n中最低位的1变为0
- n & (1<<i): 看n的二进制数中第i位是否为1
    因为n此处为二进制数，因而 (2^i) 也要用 二进制表示，否则结果报错
- lowbit = x & (-x) 得到最低位的1
    -x 为取反操作，01取反

python 运算符号 &
```
class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and (n & (n-1) == 0)

class SSolution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and (n & -n) == n 
```
## | 或
## ~ 非
## ^ 异或
异或运算有以下三个性质。
1. 任何数和 0 做异或运算，结果仍然是原来的数，即 a⊕0=a。
2. 任何数和其自身做异或运算，结果是 0，即 a⊕a=0。
3. 异或运算满足交换律和结合律，即a⊕b⊕a=b⊕a⊕a=b⊕(a⊕a)=b⊕0=b。

python 运算符号 ^
```
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        ans = 0
        for n in nums:
            ans = ans ^ n  # 异或
        return ans		
```	

## 二进制操作符 << 左移 和 >> 右移
```
<< 二进制左移符号
>> 二进制右移符号
```
1 << 1 = 2   表示 (二进制下) 1  整体左位移1位 = 10  = (十进制)2\
1 << 2 = 4   表示 (二进制下) 1  整体左位移2位 = 100 = (十进制)4\
1 << 3 = 8   表示 (二进制下) 1  整体左位移3位 = 1000 = (十进制)8\
同理：\
3 << 1 = 6   表示 (二进制下) 11  整体左位移1位 = 110  = (十进制)6\
3 << 2 = 12   表示 (二进制下) 11  整体左位移2位 = 1100 = (十进制)12\
3 << 3 = 24   表示 (二进制下) 11  整体左位移3位 = 11000 = (十进制)24\

因此可以看出：\
n >> a = n * 2^a\
n >> 1 = n * 2\
n << 1 = n / 2

```python
# 见 LeetCode 390
step = 1
n = 8
for i in range(3):
    step <<= 1
    n >>= 1
    print(step, n)
```
最后得出结果为\
2 4\
4 2\
8 1\

# 数据结构 collection 库
## 哈希表 Counter
`frequency = collections.Counter(s)` 本质为字典, 统计字符串中每个字符出现的次数 
> 可进行字典加减操作：key相同的，value值加减（会忽略掉value为零或者小于零的计数）
> 
## 队列 deque
`q = collections.deque()`

常见操作：
```python
queue = collections.deque([q])
# 右边的操作同list
queue.append(item)  
queue.pop()             
# 左边
node = queue.popleft()  #弹出最左边的项目
queue.appendleft(item)  #在左边添加 item 中的所有项目
queue.clear()              #清空队列
queue.extend(iterable)     #在右边(末尾)添加 iterable 中的所有项目
queue.extendleft(item)   #在左边(开始)添加 item 中的所有项目
```