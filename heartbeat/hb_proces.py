from pathlib import Path

filename = Path(__file__).parent / "hblog"
print(filename)
with open(filename, mode="r") as f:
    lines = f.readline()
