# Git 使用指南
## 1. 一些常用操作
### 1.1	添加和删除（暂存区）
- 初始化文件夹\
    git init

- 添加修改后文件/新建文件 到暂存区\
    git add <file>

- 添加所有文件\
    git add .

- 删除指定的暂存文件（本地仓库和远程仓库都会删除，但本地文件不会删除）\
    git rm --cached <file>
    或
    git rm -r --cached <file>
    > 删除单个文件不用加上（-r），删除文件夹需要（-r），即递归删除该文件夹。

- 仓库 和 本地文件都删除\
    git rm <file>

### 1.2	提交和撤回
- 将暂存文件提交，其中"description" 是提交描述\
    git commit -m "description"

- 撤回，退回到以提交过的任意版本：\
    git reset --hard \<xxx>
    > 其中\<xxx>为某次提交的哈希值，可以使用git log或git reflog查看

### 1.3	远程仓库
#### 1.3.1 添加远程仓库
- 添加远程仓库\
    git remote add <origin> <addr>
    > 添加远程仓库, 默认的就是origin, addr就是仓库地址,比如输入：\
    git remote add origin git@github.com:<>/<>.git

- 转换远程分支url（eg.从http到ssh）\
    git remote set-url <origin> git@github.com:<用户名>/<仓库名>.git

- 将本地仓库同步到远程仓库\
  - 若 **本地分支名** 与 **远程仓库分支名** 相同
      git push -u <origin master>\
  - 若 **本地分支名** 与 **远程仓库分支名** 不同
      git push <origin远程仓库名> <localBranchName>:<remoteBranchName>
      如 git push gitlab gitlab:main

#### 1.3.2 查看、重命名
- 获取远程仓库名\
    git remote

- 查看远程分支url\
    git remote -v

- 重命名远程仓库名\
    git remote rename origin destination

#### 1.3.3 拉取远程分支
- 克隆项目（完全克隆，包括远程仓库的版本变化）\
    git clone url\
    或 git clone url [本地路径（为新建文件夹/空文件夹）]

- 拉取远程分支最新版本，即 FETCH_HEAD
    git fetch origin master  \
    git fetch origin master:temp

- 拉取远程仓库，并与本地某分支合并，即：git pull = git fetch + git merge(**可实现多台电脑同一账户的本地仓库更新**)\
    git pull <origin master>\
    git pull <远程主机名> [远程分支名]:[本地分支名]

  
**三者区别**：
1. 是否需要本地初始化仓库\
git clone 不需要，git pull 和 git fetch 需要。

2. 是否可以指定分支推送到远程\
git clone下来的项目可以直接推送到远程，git pull 和 git fetch 需要先执行 git remote add 添加远程仓库后才能 push。


#### 1.3.4 删除远程仓库
- 方法一
   `git remote rm origin`

- 方法二
   删除项目本地文件夹下的.git 文件夹即可

### 1.4	分支
- 新建分支\
    git branch <分支名>

- 删除本地分支\
    git branch -d <分支名> //删除本地分支，无法删除 main（master)
    git branch -D <分支名> //强制删除本地分支

- 切换到某分支\
    git checkout <分支名>

- 查看所有分支名\
    git branch -a

- 查看远程分支名\
    git branch -r

- 修改分支名\
    git branch -m <旧分支名> <新分支名>

### 1.5	查看分支状态、日志
- 查看当前分支中的文件状态\
    git status

- 提交完成之后，查看提交日志\
    git log
    或
    git reflog
    > 这两个命令的输出中都有一个HEAD，它是一个指针，指向当前分支中的某个提交

### 1.6	查看、修改文件内容
- 查看文件内容\
    cat <file>

- 修改文件内容\
    vim <file>
    > 修改完后按 esc 键退出编辑模式后，输入”:wq”，保存修改并退出

## 2. 案例
### 2.1 创建新仓库
```
git init 
git remote add 仓库名 url
git add .
# 如果有多个 github账号，可能需要先设置
    git config --global user.email 221040010@link.cuhk.edu.cn  "you@example.com"
    git config --global user.name algo21-221040010  "Your Name"
git commit -m "first commit"
git push -u 仓库名 分支名
```
### 2.2 案例：多个git账号SSH管理
https://blog.csdn.net/u010250240/article/details/101627640

#### 1. 配备 config 文件
在电脑的.ssh文件夹下(比如我的路径是C:\Users\shao\.ssh)新建一个名为config的文件，没有后缀。
在其中写入：\

```
#Host: 服务器(自己的辨识标识，可以随便写)
#HostName: 主机名或域名，建议使用域名(仓库的host地址)
#User: 仓库的用户名或者邮箱
#IdentityFile: rsa文件路径(对应的秘钥存储路径)
#PreferredAuthentications publickey: 让ssh只使用publickey方式去验证,若失败就直接跳过密码登录

#github
Host github.com
HostName github.com
User a
IdentityFile ~/.ssh/github_id_rsa
PreferredAuthentications publickey

#gitee
Host gitee.com
HostName gitee.com
User b
IdentityFile ~/.ssh/gitee_id_rsa

#gitlab
Host gitlab.com
HostName gitlab.com
User c
IdentityFile ~/.ssh/gitlab_id_rsa
```
#### 2. git 设置
打开Git Bash\
1、清除 git 的全局设置（新安装git可以跳过）\
```
git  config --global --unset user.name 
git  config  --global --unset user.email 
```
2、为每一个账号都生成一对秘钥（私钥和公钥）\
为账号 a 生成秘钥(上面config里的邮箱)：

ssh-keygen -t rsa -C "邮箱"

注意：弹出的路径要写 绝对路径

3、将后缀的.pub的公钥分别添加到不同平台的ssh公钥里面。

4、最后是测试\
ssh -T git@对应的服务器地址 （即config里填的Host后面的内容）\
**若一个网站上有多个账号，则host后很可能不是地址**
eg.如果你是Host host_name，那么测试的时候就这样：ssh -T git@host_name

5、在不同git 账户下新增仓库\
**eg.如果你是Host host_name，那么：**\
git remote add 远程主机名 git@host_name:用户名/仓库名.git
### 2.3 案例：一个git账户多设备同步
假设有设备 A 和 B。\
首先在设备 A 上创建了项目并推送远程。\
 ```
 git init
 git remote add 仓库名 url
 git add .
 git commit -m ""
 git push -u 仓库名 main
 ```
此时要在设备 B 上从无到有获取这个项目
 ```
 git clone url [本地目录]
 ```
在设备 B 上对该仓库做了更改后，同步到远程仓库
 ```
 git add .
 git commit -m ""
 git push -u 仓库名 main
 ```
第二天，要在设备 A 上拉去远程仓库并合并到本地仓库上
 ```
 git pull 仓库名 main
 ```
在设备 A 上对该仓库做了更改后，同步到远程仓库（代码同 B）


#### 3. 新建仓库
git remote add 远程仓库名 git@host_name:<>/<>.git
> 正常情况下是 git remote add origin git@github.com:<>/<>.git 
> 这是因为默认 host_name 是 网址，但若同一 git 平台下有多个账号，则需要区分，重新命名


## 3. 常见报错
### 3.1	error: failed to push some refs to '.......'
错误原因1：远程仓库和本地库不一致
解决:
1. 取消刚才的commit（提交）并同步远程的仓库\
    git pull --rebase <origin master>

    git push
    或者
    git push -u <origin master>\
    其中<>中为远程仓库名

2. 合并本地和远程仓库，并同步远程仓库
    git merge <origin master>\
    git push -u <origin master>

### 3.2 unable to access ‘https://github.com/…/’: OpenSSL SSL_read: Connection was reset, errno 10054

原因1：一般是因为服务器的SSL证书没有经过第三方机构的签署，所以才报错。

解决办法：解除SSL验证\
git config --global http.sslVerify false\
再次 git push 即可


### 3.3 使用git时将部分文件写入.gitignore依旧上传的问题

本地有缓存，需要清理掉

执行前记得先把所有需要的东西先push到git，否则可能被删除
```
git rm -r --cached .
 
git add .
 
git commit -m 'update .gitignore'
```
or
```
git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch root/bigfile.csv'
```