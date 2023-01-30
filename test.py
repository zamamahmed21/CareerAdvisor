import sys

results = {'S': 2, 'M': 0, 'C': 4, 'P': 9}
t_type=''
greatest_no = 0
for letter in results:
    if results[letter]>greatest_no:
        print(f"{results[letter]}>{greatest_no}")
        greatest_no=results[letter]
        t_type = letter
print(t_type)