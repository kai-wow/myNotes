Mac 终端操作命令
1.pwd -print working dir
2.open
3.cd

～ 代表宿主目录，即 /users/用户名
. 当前目录
.. 父级目录
- 上一次所在目录

4.touch 新建空文件
5.mkdir 创建一个目录
  mkdir -p 创建递归/多层目录
6.ls 列出当前目录的所有文件（含文件夹
  ls -a 列出包含隐藏文件/目录的所有文件
  ls -l 列出所有文件的详细信息。
	其中第一列信息，第一个字母 -表示为普通文件，d表示为目录；后面三位一组，r可读，w可写，x可执行
7.rm 删除文件（且无法恢复，不会在回收站里）
  rm -r 删除文件夹‘
8.cp 拷贝文件copy
  cp -r 拷贝目录（注意最后不要/）
  cp 被拷贝文件目录 目标目录
9.mv 剪切移动move；重命名
  mv 待移动目录/文件 移动位置
  Mv 原文件名 新文件名
10.cat 查看文件内容，全部输出到控制台上
11.more 查看文件内容，但一屏一屏查看，enter键/下方向键可执行下一行查看操作；空格执行下一屏操作；q退出
12.grep 字符串搜索
   grep ‘字符串’ 被检索文件  == cat 被检索文件 | ‘字符串’                 
   ls | grep ‘字符串’ 检索文件名中包含某字符的文件    
# 其中 | 为管道，将左边的输出作为右边的输入，可迭代使用
   

tips：
自动补全键 tab，例如，可补全当前目录下的文件名
