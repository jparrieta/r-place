import os, sys, time
Y = sys.argv[1]; A = sys.argv[2]; budget = float(sys.argv[3])
ref = os.path.join(Y, "_instrument", "v30")
files = {}
for dp, dn, fn in os.walk(ref):
    if "__pycache__" in dp: continue
    for f in fn:
        p = os.path.join(dp, f); files[os.path.relpath(p, ref)] = open(p, "rb").read()
def write_file(path, data):
    try:
        with open(path, "wb") as fh: fh.write(data); return 1
    except PermissionError:
        os.makedirs(A, exist_ok=True)
        os.replace(path, os.path.join(A, os.path.basename(path) + ".%d" % int(time.time()*1000)))
        with open(path, "wb") as fh: fh.write(data); return 1
t0 = time.time(); done = 0; left = 0
rooms = sorted(os.listdir(os.path.join(Y, "rooms")))
for r in rooms:
    inst = os.path.join(Y, "rooms", r, "instrument")
    if not os.path.isdir(inst): continue
    probe = os.path.join(inst, "emit.py")
    if os.path.exists(probe) and open(probe, "rb").read() == files["emit.py"] and \
       open(os.path.join(inst, "CONTRACT.v30.md"), "rb").read() == files["CONTRACT.v30.md"]:
        continue
    if time.time() - t0 > budget:
        left += 1; continue
    for rel, data in files.items():
        dst = os.path.join(inst, rel)
        if os.path.exists(dst) and open(dst, "rb").read() == data: continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        write_file(dst, data)
    done += 1
print("updated", done, "left", left, "of", len(rooms), "in %.0fs" % (time.time() - t0))
