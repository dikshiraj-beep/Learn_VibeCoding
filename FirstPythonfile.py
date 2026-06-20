#I’m setting up a simple example now that shows how a `for` loop can grade students using A, B, and C criteria.

#Sure — here’s a simple Python example that uses a `for` loop to apply a grading system based on marks:

#```python
scores = [85, 72, 68, 91, 58, 77]

for mark in scores:
    if mark >= 85:
        grade = "A"
    elif mark >= 70:
        grade = "B"
    else:
        grade = "C"
    
    print(f"Mark: {mark} -> Grade: {grade}")


