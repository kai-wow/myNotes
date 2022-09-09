# linux
## 常见操作命令
1. pwd: print working dir
2. open
3. cd
    ```
    ~ 代表宿主目录，即 /users/用户名
    . 当前目录
    .. 父级目录
    - 上一次所在目录
    ```
4. touch 新建空文件
5. mkdir 创建一个目录
    mkdir -p 创建递归/多层目录
6. ls 列出当前目录的所有文件（含文件夹
    ls -a 列出包含隐藏文件/目录的所有文件
    ls -l 列出所有文件的详细信息。
        其中第一列信息，第一个字母 -表示为普通文件，d表示为目录；后面三位一组，r可读，w可写，x可执行

7. grep 字符串搜索
    grep '字符串' 被检索文件  == cat 被检索文件 | '字符串'               
    ls | grep ‘字符串’ 检索文件名中包含某字符的文件    
    > 其中 | 为管道，将左边的输出作为右边的输入，可迭代使用

## 文件
### 解压增删查看
1. unzip 解压
unzip "目录/文件.zip" -d "目录/"
2. cp 复制
cp "目录/文件" "目录/"
3. rm 删除文件（且无法恢复，不会在回收站里）
    rm -r 删除文件夹
4. mv 剪切移动; 重命名
    - 剪切移动
        mv 待移动目录/文件 移动位置
    - 重命名
        Mv 原文件名 新文件名
5. cat 查看文件
    查看文件前几行
    cat "目录/文件" | head -n 10
6. more 查看文件内容，但一屏一屏查看，enter键/下方向键可执行下一行查看操作；空格执行下一屏操作；q退出

### 文件权限码
实例：-rwxrwxr-x 
1. 第一字段是文件和目录权限的编码：
    -代表文件，d代表目录，l代表链接，c代表字符型设备，b代表块设备，n代表网络设备

2. 之后的三组字符编码，每一种定义了三种访问权限：
    r 代表对象是可读的，w 代表对象是可写的，x 代表对象是可执行的
    i. 前三位rwx：文件的属主(设为登录名root)
    ii. 中三位rwx：文件的属组(设为组名root)
    iii. 后三位r-x：系统上其他人

### 移动文件
1. 本地移动 mv
```shell
ourfilenames=`ls -p /mnt/Data/shaokai/factors/haitong/factor/ | grep -v /` # 只显示 filename，不显示目录
for eachfile in $yourfilenames
do
   if [[ "$eachfile" =~ "inday" ]] # 包含 inday
   then
      echo $eachfile
      mv /mnt/Data/shaokai/factors/haitong/factor/$eachfile /mnt/Data/shaokai/factors/haitong/intermediate/
   fi
done
```
2. 不同远程服务器间移动 rsync
```shell 
dirs = "15min 30min"  # 空格即可
for dir in $dirs
do
    echo $dir
    sshpass -p "sk001732" rsync -r /mnt/Data/shaokai/stock_order/$dir/ shaokai@172.16.30.34:/mnt/Data/shaokai/stock_order/$dir/
done
```

## screen
后台跑代码，即使关闭窗口/服务器断了，代码进程也不会断

### 新建 screen
screen -S <your_screen_name>

### 进入 screen/恢复离线的 screen 作业
screen -r <your_screen_name>　恢复离线的screen作业
screen -R 　先试图恢复离线的作业。若找不到离线的作业，即建立新的screen作业。

Ctrl+D  # 在当前screen下，输入Ctrl+D，删除该screen
Ctrl+A，Ctrl+D  # 在当前screen下，输入先后Ctrl+A，Ctrl+D，退出该screen

###  显示screen list
​​​​​​​screen -ls

### 连接状态为【Attached】的screen
screen -D -r your_screen_name  # 解释：-D -r 先踢掉前一用户，再登陆

### 判断当前是否在screen中断下, Ubuntu系统,可以这样:
sudo vim /etc/screenrc
### 文件末尾追加一行即可允许设置screen标题
caption always "%{.bW}%-w%{.rW}%n %t%{-}%+w %=%H %Y/%m/%d "

### 删除指定screen, your_screen_name为待删除的screen name
​​​​​​​screen -S your_screen_name -X quit

## linux shell 语法
### .sh 文件
运行linux命令文件
bash xx.sh
### 字符串运算符
1. 字符串A 包含 字符串B
```shell
strA="helloworld"
strB="low"
if [[ $strA =~ $strB ]] # [[ "$eachfile" =~ "inday" ]] 
then
    echo "包含"
else
    echo "不包含"
fi
```

## 进程
### 查看进程
1. top
> 若只看某一用户的进程，则 `top -u user`
2. glances
3. ps -ef
> 若只看某一用户或某一进程，则 `ps -ef|grep <pid/usr>`
    更多： https://juejin.cn/post/6844904104410480653
### kill进程
1. kill 某一个进程
`kill <pid>`
2. kill 某一用户的所有进程
`pkill -u <user>`