import random
import subprocess
import sys


def check(commands):
    students = []
    expected = []
    for command in commands:
        fields = command.split()
        operation = int(fields[0])
        if operation == 1:
            student = (fields[1], fields[2], int(fields[3]))
            if any(s[0] == student[0] for s in students):
                expected.append("FAILED")
            else:
                students.append(student)
                expected.append("SUCCESS")
        elif operation == 7:
            expected.append("END")
            break
        else:
            if operation == 2:
                result = students
            elif operation == 3:
                result = [s for s in students if s[0] == fields[1]]
            elif operation == 4:
                result = [s for s in students if s[1] == fields[1]]
            elif operation == 5:
                result = sorted(students)
            else:
                result = sorted(students, key=lambda s: -s[2])
            expected.extend(f"{sid} {name} {grade}" for sid, name, grade in result)
    actual = subprocess.run(
        [sys.argv[1]], input="\n".join(commands) + "\n",
        text=True, capture_output=True, check=True
    ).stdout
    assert actual == "".join(line + "\n" for line in expected)


check(["2", "5", "6", "7", "1 123456789 Ignored 1"])
check([
    "1 100000003 First 0", "1 000000001 Second 100",
    "1 100000002 Third 0", "1 100000003 Rejected 100",
    "5", "6", "2", "3 100000003", "4 Second",
    "1 000000002 Fourth 0", "6", "5", "2", "7",
])
rng = random.Random(57)
for trial in range(100):
    commands = []
    accepted = {}
    for step in range(300):
        operation = rng.choice([1, 1, 1, 2, 3, 4, 5, 6])
        if operation == 1 or not accepted:
            sid = f"{rng.randrange(100):09d}"
            name = f"Student{step}"
            commands.append(f"1 {sid} {name} {rng.randrange(101)}")
            accepted.setdefault(sid, name)
        elif operation in (3, 4):
            sid = rng.choice(list(accepted))
            commands.append(f"{operation} {sid if operation == 3 else accepted[sid]}")
        else:
            commands.append(str(operation))
    check(commands + ["7"])
print("Passed edge cases and 100 randomized command sequences.")
