# colorized output
```python
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)
for idx in range(len(c)-1):
    print(c[idx + 1] + f"Initiated makerandom({idx}).")
print(c[0] + "finished.")
```