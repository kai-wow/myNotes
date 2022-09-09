# 知识点
## join 合并
`A join B on A.id = B.id`

```sql
select e.id from 
    Employees e left join Salaries s on e.id = s.id 
where e.name is null or s.salary is null
```

## union
leetcode sql 1965

## 日期
1. 可以用 min max 函数。
比较、匹配日期时直接用字符串 min(sale_date) >= '2019-01-01'
2. 日期差 DATEDIFF 函数
3. 时间戳的年月日获取
year(time_stamp)
## 比较 （排除null）
使用 <> (!=) 会直接排除 null 值的情况。

MySQL 使用三值逻辑 —— TRUE, FALSE 和 UNKNOWN。任何与 NULL 值进行的比较都会与第三种值 UNKNOWN 做比较。这个“任何值”包括 NULL 本身！这就是为什么 MySQL 提供 IS NULL 和 IS NOT NULL 两种操作来对 NULL 特殊判断。

因此，在 WHERE 语句中我们需要做一个额外的条件判断 `x IS NULL'。

## 改变表单的attr名字
`select name as 'name2' from table`

注意：
    - as 和 from 不可调换顺序
    - 'name2' 要用引号括起来

## 字符处理
### 1. 截取子字符串
i. 任意位置截取
`SUBSTRING(name, 2, length(name))` 含头、尾
ii. 截取尾部
`SUBSTRING(name, 2)` 截取除了第一个字母以外的字符串
iii. 截取头部
`left(name, 1)` 截取第一个字符

### 2. 融合字符串
1. `concat(sub1, sub2)`
2. 跨行合并
groupby后各小组内部合并字符串： group_concat(distinct product)
    例如：
```sql
select sell_date, 
       count(distinct product) as num_sold, 
       group_concat(distinct product) as products from Activities
group by sell_date
order by sell_date asc
```
### 3. 全部大写、全部小写： `upper(), lower()`

### 4. 字符文本匹配
- name不以M开头：
    1.用内置的匹配方法： name not like 'M%'
    2.用正则表达式判断： name not rlike '^M' (^ 匹配输入字符串的开始位置)

- name中包含 M（任何位置）
    1.用内置的匹配方法： name like '%M%'
    2.用正则表达式判断： name rlike 'DIAB1' 或 name regexp 'DIAB1'

- 多规则匹配
    eg. name 以 M 开头，或 name 中包含 ‘空格M’
    name rlike '^M| M'
    name regexp '^M| M'

## 分组排序
eg. leetcode SQL 1851
```sql
SELECT DENSE_RANK() OVER (
partition by DepartmentId
order by Salary desc) AS ranking, Name, Salary
FROM Employee)
```

其中
`DENSE_RANK() OVER (PARTITION BY DepartmentId ORDER BY Salary DESC)`
指的先根据DepartmentId分组，然后再根据Salary倒叙排列，再对分组后的表格生成Rank序列

1. 排序
    i. DENSE RANK() OVER() 排名，遇到并列不会跳号，如 1,2,2,3
    ii. RANK() OVER() 遇到并列会跳号，如 1,2,2,4
    iii. ROW_NUMBER() 遇到并列依然会给新序号，如 1,2,3,4

2. over (partition by column order by column) 是分组和排序.
    也就是说 rank 并不是基于 当下的表, 而是基于分组排序后的表.

## 排序选取
### limit语句
1、当 limit后面跟**一个参数**的时候，该参数表示要取的数据的数量

例如 `select* from user limit 3` 表示直接取前三条数据

2、当limit后面跟**两个参数**的时候，第一个数表示要跳过的数量，后一位表示要取的数量,例如

`select * from user limit 1,3`;

就是跳过1条数据,从第2条数据开始取，取3条数据，也就是取2,3,4三条数据

3、当 **limit和offset组合**使用的时候，limit后面只能有一个参数，表示要取的的数量,offset表示要跳过的数量 。

例如 `select * from user limit 3 offset 1`; 表示跳过1条数据, 从第2条数据开始取，取3条数据，也就是取2,3,4三条数据

## case when 语句
```
CASE WHEN (判断语句)
THEN ()
ELSE ()
END;
```
或 
```
CASE (attr) WHEN (value)
THEN ()
ELSE ()
END;
```

```sql
select id,
sum(case month when 'Jan' then revenue end) as 'Jan_Revenue'
from Department
group by id
```

## if 语句
`if(判断语句, true 时取值, false 时取值) `

select name, sum(amount) balance from Transactions t left join users u 
on t.account = u.account
group by t.account
having balance >= 1000

## 更新
### 更新现存表格 UPDATE (TableName) SET ()
```sql
UPDATE Salary
SET sex = CASE sex
WHEN 'm' THEN 'f' ELSE 'm'
END;
```

## 删除

把需要删除的数据用 select 写出来，再把 select 改为 delect 即可


# leetcode
## 196 删除重复保留最小 (技巧：自己和克隆的自己比)
```sql
DELETE p1 FROM Person p1, Person p2
WHERE p1.Email = p2.Email AND p1.Id > p2.Id
```

## 1667 修复表格中的名字为首字母大写
```sql
select user_id,
concat (upper(left(name, 1)), lower(substring(name, 2))) as name
from users
order by user_i
```

## 1484 按日期分组合并销售产品 (字符的跨行分组合并group_concat)
```sql
select sell_date, count(distinct product) num_sold, group_concat(distinct product) products from Activities
group by sell_date
order by sell_date asc
```
## 1965 丢失信息的雇员 join+union
丢失 name 或 salary 信息的雇员 (分别存于两个table)

```sql
SELECT A.employee_id
FROM employees A LEFT JOIN salaries B ON A.employee_id = B.employee_id
WHERE B.salary IS NULL

union 

SELECT A.employee_id
FROM salaries A LEFT JOIN employees B ON A.employee_id = B.employee_id
WHERE B.name IS NULL

ORDER BY employee_id
```
## 1795 每个产品在不同商店的价格 (列变行，stack/unstack)
```sql
SELECT product_id, 'store1' as store, store1 as price
FROM Products
WHERE store1 IS NOT NULL  # 筛选在 store1 中存在价格的产品

UNION ALL

SELECT product_id, 'store2' as store, store2 as price
FROM Products
WHERE store2 IS NOT NULL  # 筛选在 store2 中存在价格的产品

UNION ALL

SELECT product_id, 'store3' as store, store3 as price
FROM Products
WHERE store3 IS NOT NULL;  # 筛选在 store3 中存在价格的产品
```
## 176 第二高的薪水 
### 法一： limit+set
```sql
SELECT (SELECT DISTINCT Salary
        FROM Employee
        ORDER BY Salary DESC
        LIMIT 1 OFFSET 1) AS SecondHighestSalary
```
### 法二： 和 max比较
```sql
select max(Salary) SecondHighestSalary 
from Employee
where Salary < (select max(Salary) from Employee)
```
# 安装和配置 mysql

cmd 命令下生成的初始密码
dHqB+B((z5aK
已修改为
123456