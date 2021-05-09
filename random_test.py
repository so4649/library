from random import randint
import subprocess

TESTCASE_FILE = "random.in"
MAIN_PROC = "a.py"
GREEDY_PROC = "b.py"


def read_random_case():
    with open(TESTCASE_FILE, "r", encoding="utf-8") as f:
        return " ".join(map(str, f.readlines()))


def write_random_case():
    with open(TESTCASE_FILE, "w", encoding="utf-8") as f:
        N = randint(1, 100)
        f.write(f"{N}")


def solve(proc_name):
    with open(TESTCASE_FILE, "r", encoding="utf-8") as f:
        res = subprocess.run(
            ["python", proc_name], stdin=f, stdout=subprocess.PIPE, encoding="utf-8")
        return res.stdout.rstrip()


def main():
    count = 0
    while count <= 100:
        write_random_case()
        A = solve(MAIN_PROC)
        B = solve(GREEDY_PROC)
        if A != B:
            print("----------------------------------------")
            print("Wrong Answer")
            print("[test case] ")
            print(read_random_case())
            print(MAIN_PROC)
            print(A)
            print(GREEDY_PROC)
            print(B)
            print("----------------------------------------")
            break
        count += 1


if __name__ == "__main__":
    main()