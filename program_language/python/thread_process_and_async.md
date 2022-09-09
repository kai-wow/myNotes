# 线程、进程 与 协程（异步）
## 协程/异步
async IO is a single-threaded, single-process design: it uses cooperative multitasking. 
Async IO gives a feeling of concurrency despite using a single thread in a single process. Coroutines (a central feature of async IO) can be scheduled concurrently, but they are not inherently concurrent.

异步意味着任务不会阻塞，比如，如果我要下载一个比较忙的网络资源，我的程序不需要一直等待下载完成，它可以在等待下载时继续做其他事情。这与并行执行多个操作不同。

when you use `await f()`, it’s required that `f()` be an object that is awaitable. 

```python
import asyncio

async def count():
    print("One")
    await asyncio.sleep(1)  # a non-blocking call, 不能用 time.sleep() 因为它 blocking 会堵塞 
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
```
输出：
```
One
One
One
Two
Two
Two
code/test.py executed in 1.02 seconds.
```
遇到await asyncio.sleep(1) 后，会直接进入下一个循环，先运行别的任务

> ref: https://realpython.com/async-io-python/

## 线程 vs 进程 / Process vs Thread
### 二者都属于 concurrency 
concurrency encompasses both multiprocessing (ideal for CPU-bound tasks) and threading (suited for IO-bound tasks). 
Multiprocessing is a form of parallelism, with parallelism being a specific type (subset) of concurrency. 
>  concurrency vs parallelism / 并发 vs 并行
    concurrency 并发：不要求**同时**进行（看起来像多任务）
    parallelism 并行： 要求**同时**进行（真正的多任务）

             |- threading, async io
concurrency -
             |- parallelism: multiprocessing
### 二者关系
A process is an instance of program (e.g. Jupyter notebook, Python interpreter). Processes spawn threads (sub-processes) to handle subtasks like reading keystrokes, loading HTML pages, saving files. 
**Threads live inside processes and share the same memory space.**

- Example: Microsoft Word
    When you open Word, you create a process. When you start typing, the process spawns threads: one to read keystrokes, another to display text, one to autosave your file, and yet another to highlight spelling mistakes. 
    By spawning multiple threads, Microsoft takes advantage of idle CPU time (waiting for keystrokes or files to load) and makes you more productive.

> ref: https://medium.com/@bfortuner/python-multithreading-vs-multiprocessing-73072ce5600b

## 线程 vs 协程

线程: 操作系统内核执行任务切换。（即，当多个线程正在运行时，内核可能停止当前进程，使其进入休眠状态，并选择不同的线程继续执行。这被称作抢占式多任务处理【Preemption】）

协程: 我们自己控制任务的切换，它被称作非抢占式或合作型多任务式。
因为是自己处理切换，所以我们需要一个调度程序，也叫做『事件循环』。此事件循环只循环遍历等待中的调度，并运行它的所有事件。每当我们产生操作时，当前任务会被添加到队列中，且第一个任务（优先级而非顺序）从队列中弹出并开始执行。

> ref: https://www.jb51.net/article/147511.htm

### 多线程
```python
from joblib import Parallel, delayed

Parallel(n_jobs=30)(delayed(func)(para1, para2) 
                            for para2 in range(100)
                            if int(para2) % 5 > 2)
```
