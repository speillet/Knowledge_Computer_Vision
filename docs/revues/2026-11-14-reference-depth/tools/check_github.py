import re, sys, urllib.request, urllib.error, concurrent.futures as cf, json
urls = [u.strip() for u in open(sys.argv[1]) if u.startswith('https://github.com/')]
files = {}; other = set()
for u in urls:
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/([^#?]+)(?:#L(\d+)(?:-L(\d+))?)?", u)
    if m:
        k = m.group(1,2,3,4); files.setdefault(k, []).append((u, int(m[5]) if m[5] else None, int(m[6]) if m[6] else (int(m[5]) if m[5] else None)))
    else:
        other.add(u.split('#')[0])
def get(url, head=False):
    req = urllib.request.Request(url, method='HEAD' if head else 'GET', headers={'User-Agent': 'link-check'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, (None if head else r.read())
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return str(e)[:60], None
def check_file(k):
    o, r, ref, path = k
    st, body = get(f"https://raw.githubusercontent.com/{o}/{r}/{ref}/{path}")
    res = []
    if st != 200:
        return [(u, f"raw {st}") for u, a, b in files[k]]
    n = body.count(b'\n') + (0 if body.endswith(b'\n') else 1)
    for u, a, b in files[k]:
        if b and b > n: res.append((u, f"line {b} > {n} lines"))
    return res
bad = []
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(check_file, files): bad += r
    for u, (st, _) in zip(sorted(other), ex.map(lambda u: get(u), sorted(other))):
        if st != 200: bad.append((u, f"page {st}"))
print(json.dumps({"blob_files": len(files), "blob_urls": sum(len(v) for v in files.values()), "other": len(other), "bad": bad}, indent=1))
