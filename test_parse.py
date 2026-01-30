from functions import parse_greetings_log

sample = """Alice's multiplication table for 3:
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
------------------------------
Bob's multiplication table for 2:
2 x 1 = 2
2 x 2 = 4
------------------------------
"""

with open('greetings_log.txt', 'w') as f:
    f.write(sample)

print(parse_greetings_log())
