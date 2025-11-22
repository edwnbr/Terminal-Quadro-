#!/usr/bin/env python3
# karen_os_terminal.py
# Single-file Karen OS style terminal — large set of visual commands/output.
# NOTE: This file produces only local textual output and animations. No network / subprocess / external actions.

import sys, time, random, threading, os
from datetime import datetime

# ---------- CONFIG ----------
PROMPT = "karen@os:~$ "
KAREN = "Karen"
random.seed()

# ---------- UTILITIES ----------
def _flush(): sys.stdout.flush()
def slow_print(s, ch_delay=0.003, nl=True):
    for ch in str(s):
        sys.stdout.write(ch)
        _flush()
        time.sleep(ch_delay)
    if nl:
        sys.stdout.write("\n")
        _flush()

def instant(s=""):
    sys.stdout.write(str(s) + "\n"); _flush()

def bar(duration, width=30, prefix=None):
    if prefix:
        sys.stdout.write(prefix + " ")
    step = max(0.01, duration / width)
    for i in range(width + 1):
        hashes = "#" * i
        dots = "-" * (width - i)
        pct = int(i / width * 100)
        sys.stdout.write(f"\r[{hashes}{dots}] {pct}%")
        _flush()
        time.sleep(step)
    sys.stdout.write("\n"); _flush()

def spin(duration, prefix=None):
    if prefix:
        sys.stdout.write(prefix + " ")
    chars = "|/-\\"
    start = time.time()
    i = 0
    while time.time() - start < duration:
        sys.stdout.write("\r" + chars[i % 4])
        _flush(); i += 1; time.sleep(0.08)
    sys.stdout.write("\r \n"); _flush()

def hexstr(n=24):
    return "".join(random.choice("0123456789ABCDEF") for _ in range(n))

def ip_like():
    return f"{random.randint(10,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

# timed op: chooses duration in seconds, shows animation (bar or spinner) then returns duration
def timed_op(min_s=1.5, max_s=6.0, style="bar", title=None):
    dur = random.uniform(min_s, max_s)
    if title:
        instant(f"[{KAREN}] {title} — est {dur:.1f}s")
    if style == "bar":
        bar(dur, width=28)
    else:
        spin(dur, prefix="Processing")
    return dur

# ---------- KAREN PERSONA ----------
karen_state = {"mood": random.choice(["calm","focused","neutral"]), "start": time.time(), "notes": []}
def karen_say(msg):
    slow_print(f"[{KAREN}] {msg}", ch_delay=0.004)
def karen_status():
    uptime = int(time.time() - karen_state["start"])
    instant(f"[{KAREN}] mood={karen_state['mood']} uptime={uptime}s notes={len(karen_state['notes'])}")

# ---------- BACKGROUND EVENTS ----------
bg_events = []
def bg_worker():
    pool = [
        "[kernel] thermal drift corrected",
        "[net] packet jitter stabilized",
        "[fs] garbage collection complete",
        "[ai] latent index refreshed",
        "[monitor] load profile normalized"
    ]
    while True:
        time.sleep(random.uniform(12,35))
        ev = f"{datetime.now().strftime('%H:%M:%S')} {random.choice(pool)}"
        bg_events.append(ev)
        if len(bg_events) > 60:
            bg_events.pop(0)
threading.Thread(target=bg_worker, daemon=True).start()

# ---------- VIRTUAL FILE SYSTEM, PROCESSES, HOSTS ----------
VFS = {
    "/etc/karen.conf": "mode=full\nowner=edwin",
    "/etc/hosts": "127.0.0.1 localhost",
    "/var/log/boot.log": "boot ok\nservices started",
    "/home/edwin/readme.txt": "Karen OS demo content"
}
PROC = ["karen-daemon","sys-watch","logger"]
HOSTS = [ip_like() for _ in range(6)]

# ---------- INPUT NORMALIZATION ----------
def normalize(raw):
    raw = raw.strip()
    if not raw:
        return None, []
    parts = raw.split()
    # if first token is like "fs" and second token is a small word -> convert to dot-form
    if len(parts) > 1 and parts[0].isalpha() and len(parts[1]) <= 12 and '.' not in parts[0]:
        candidate = f"{parts[0]}.{parts[1]}".lower()
        # treat common patterns: fs, proc, hack, render, net, ai
        if parts[0].lower() in ["fs","proc","hack","render","net","ai","scan","port","deep"]:
            return candidate, parts[2:]
    # otherwise return first token normalized
    return parts[0].lower(), parts[1:]

# ---------- CORE HANDLERS ----------
def h_help(args):
    instant("Categories: system, fs, proc, net, hack, ai, render, loops")
    instant("Type 'help all' for extended command list.")

def h_help_all(args):
    instant("System: help, exit, clear, time, uptime, karen.status, karen.note <text>")
    instant("FS: fs.list [path], fs.read <path>, fs.write <path> <text>, fs.delete <path>")
    instant("PROC: proc.list, proc.run <name>, proc.kill <name>")
    instant("NET: ping <host>, dns <domain>, trace <host>, net.map, net.scan <range>")
    instant("HACK: hack.wifi <ssid>, port.scan <ip>, deep.trace <ip>, breach.sim <target>, payload.deploy <name>")
    instant("AI: ai.ask <text>, ai.scan <target>, karen.note <text>")
    instant("Render: render.noise, render.grid, render.glitch")
    instant("Loops: loop.scan, loop.attack, loop.random")
    instant("Plus many generated aliases. Type 'commands' to list total commands count.")

def h_exit(args):
    instant("shutting down shell...")
    sys.exit(0)

def h_clear(args):
    os.system("cls" if os.name == "nt" else "clear")

def h_time(args):
    instant(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def h_uptime(args):
    instant(f"uptime: {int(time.time()-karen_state['start'])}s")

def h_karen_status(args):
    karen_status()

def h_karen_note(args):
    if not args:
        karen_say("No note provided.")
        return
    note = " ".join(args)
    karen_state["notes"].append((datetime.now().isoformat(), note))
    karen_say("Note stored.")

# ---------- FS HANDLERS ----------
def h_fs_list(args):
    path = args[0] if args else "/"
    timed_op(0.5, 1.8, style=random.choice(["bar","spin"]), title=f"Listing {path}")
    found = False
    for p in sorted(VFS.keys()):
        if p.startswith(path):
            instant("  " + p)
            found = True
    if not found:
        instant("  <no files>")

def h_fs_read(args):
    if not args:
        instant("Usage: fs.read <path>"); return
    p = args[0]
    timed_op(0.5,1.6, style="bar", title=f"Reading {p}")
    if p in VFS:
        slow_print(VFS[p], ch_delay=0.002)
    else:
        instant("ERROR: not found")

def h_fs_write(args):
    if len(args) < 2:
        instant("Usage: fs.write <path> <text>"); return
    p = args[0]; txt = " ".join(args[1:])
    timed_op(0.6,2.4, style="bar", title=f"Writing {p}")
    VFS[p] = txt
    instant("OK")

def h_fs_delete(args):
    if not args:
        instant("Usage: fs.delete <path>"); return
    p = args[0]
    timed_op(0.4,1.6, style="spin", title=f"Deleting {p}")
    if p in VFS:
        del VFS[p]; instant("Deleted")
    else:
        instant("Not found")

# ---------- PROCESS HANDLERS ----------
def h_proc_list(args):
    timed_op(0.5,1.6, style="spin", title="Listing processes")
    for p in PROC:
        instant(f" {p}  pid:{random.randint(1000,9999)} mem:{random.randint(10,800)}MB")

def h_proc_run(args):
    if not args:
        instant("Usage: proc.run <name>"); return
    name = " ".join(args)
    timed_op(0.6,2.4, style="bar", title=f"Launching {name}")
    PROC.append(name); instant(f"{name} started")

def h_proc_kill(args):
    if not args:
        instant("Usage: proc.kill <name>"); return
    name = " ".join(args)
    timed_op(0.4,1.8, style="spin", title=f"Killing {name}")
    if name in PROC:
        PROC.remove(name); instant(f"{name} terminated")
    else:
        instant("Process not found")

# ---------- NETWORK HANDLERS (NO REAL NETWORK) ----------
def h_ping(args):
    if not args:
        instant("Usage: ping <host>"); return
    host = args[0]
    timed_op(1.2,3.6, style="bar", title=f"Pinging {host}")
    for i in range(4):
        instant(f"Reply from {host}: time={random.randint(4,120)}ms")
    instant("Ping complete")

def h_dns(args):
    if not args:
        instant("Usage: dns <domain>"); return
    dom = args[0]
    timed_op(0.5,1.8, style="spin", title=f"Resolving {dom}")
    instant(f"{dom} -> {ip_like()}")

def h_trace(args):
    if not args:
        instant("Usage: trace <host>"); return
    h = args[0]
    timed_op(1.6,4.5, style="bar", title=f"Tracing {h}")
    hops = random.randint(3,8)
    for i in range(1, hops+1):
        instant(f"{i:02d}  10.0.{i}.{random.randint(1,254)}  {random.randint(10,200)}ms")
    instant("Trace complete")

def h_net_map(args):
    timed_op(1.0,2.8, style="spin", title="Mapping network")
    for i in range(random.randint(3,8)):
        instant(f"Node {i} - 10.0.{i}.{random.randint(2,254)} - up")

def h_net_scan(args):
    rng = args[0] if args else "10.0.0.0/24"
    timed_op(2.0,7.0, style="bar", title=f"Scanning {rng}")
    found = random.randint(1,7)
    for i in range(found):
        instant(f"Found host: 10.0.{i+1}.{random.randint(2,250)} ports:{random.sample([22,80,443,8080,3306], k=random.randint(1,4))}")

# ---------- HACK-LIKE VISUAL HANDLERS (LOCAL TEXT OUTPUT ONLY) ----------
def h_hack_wifi(args):
    if not args:
        instant("Usage: hack.wifi <ssid>"); return
    ssid = args[0]
    timed_op(3.0,9.0, style="bar", title=f"Brute-forcing WiFi '{ssid}'")
    outcome = random.choice(["key found","weak key pattern","no key"])
    if outcome == "key found":
        instant(f"Key: {ssid}_!{random.randint(1000,9999)}")
    elif outcome == "weak key pattern":
        instant("Weak key pattern: KEY-XXXX")
    else:
        instant("No key recovered")

def h_port_scan(args):
    if not args:
        instant("Usage: port.scan <ip>"); return
    ip = args[0]
    timed_op(3.0,8.0, style="bar", title=f"Port scan {ip}")
    ports = random.sample([21,22,23,25,53,80,110,135,443,3306,8080], k=random.randint(3,8))
    for p in ports:
        instant(f"Port {p}/tcp - {'open' if random.random()>0.3 else 'filtered'}")

def h_deep_trace(args):
    if not args:
        instant("Usage: deep.trace <ip>"); return
    ip = args[0]
    timed_op(4.0,12.0, style="spin", title=f"Deep tracing {ip}")
    instant("Deep trace complete. route stable")

def h_breach_sim(args):
    target = args[0] if args else "unknown"
    timed_op(6.0,16.0, style="bar", title=f"Simulated breach {target}")
    instant(random.choice(["ACCESS GRANTED","ACCESS DENIED","ESCALATION REQUIRED"]))

def h_payload_deploy(args):
    name = args[0] if args else "payload"
    timed_op(2.5,8.0, style="bar", title=f"Preparing payload {name}")
    instant(f"Payload staged: id={hexstr(12)}")

# ---------- AI / KAREN HANDLERS ----------
def h_ai_ask(args):
    if not args:
        instant("Usage: ai.ask <text>"); return
    q = " ".join(args)
    timed_op(1.2,3.0, style="spin", title="AI analyzing")
    karen_say(random.choice([
        f"Check logs regarding '{q}'.",
        f"Probability estimate: {random.randint(10,98)}%",
        f"Anomalies detected near '{q}'.",
        f"No critical findings for '{q}'."
    ]))

def h_ai_scan(args):
    target = args[0] if args else "unknown"
    timed_op(2.0,6.0, style="bar", title=f"AI deep scan {target}")
    karen_say(f"Report: entropy nominal; anomalies {random.randint(0,4)}")

# ---------- RENDER EFFECTS ----------
def h_render_noise(args):
    timed_op(0.6,2.4, style="spin", title="Injecting noise")
    for _ in range(6):
        instant("".join(random.choice("01<>#%@&*") for _ in range(70)))

def h_render_grid(args):
    timed_op(0.8,2.8, style="bar", title="Rendering grid")
    for r in range(8):
        instant(" ".join(f"{random.randint(0,99):02d}" for _ in range(12)))

def h_render_glitch(args):
    timed_op(0.8,3.0, style="spin", title="Glitching")
    for _ in range(10):
        instant("".join(random.choice("█▓▒░<>/\\|#%@") for _ in range(60)))

# ---------- LOOP MODES ----------
def h_loop_scan(args):
    instant("Starting continuous scan (Ctrl+C to stop)")
    try:
        while True:
            h_net_scan([])
            time.sleep(random.uniform(1.0,3.0))
    except KeyboardInterrupt:
        instant("\nLoop stopped.")

def h_loop_attack(args):
    instant("Starting continuous attack mode (Ctrl+C to stop)")
    try:
        while True:
            tgt = random.choice(HOSTS)
            h_port_scan([tgt])
            time.sleep(random.uniform(1.2,3.5))
    except KeyboardInterrupt:
        instant("\nLoop stopped.")

def h_loop_random(args):
    instant("Starting mixed loop (Ctrl+C to stop)")
    try:
        while True:
            cmd = random.choice(list(COMMANDS.values()))
            try:
                cmd([])
            except:
                pass
            time.sleep(random.uniform(0.7,2.0))
    except KeyboardInterrupt:
        instant("\nLoop stopped.")

# ---------- DYNAMIC ALIASES GENERATION (fills up commands to 200+) ----------
def make_sim(name, complexity=1.0):
    def handler(args):
        timed_op(0.6*complexity, 2.2*complexity, style=random.choice(["bar","spin"]), title=f"{name} " + (" ".join(args) if args else ""))
        instant(f"[{name}] digest: {hexstr(18)}")
        for i in range(random.randint(2,5)):
            instant(f"  metric{i:>2}: {random.randint(0,99999)}")
    return handler

# base registry
COMMANDS = {
    "help": h_help,
    "help all": h_help_all,
    "exit": h_exit,
    "clear": h_clear,
    "time": h_time,
    "uptime": h_uptime,
    "karen.status": h_karen_status,
    "karen.note": h_karen_note,
    "fs.list": h_fs_list,
    "fs.read": h_fs_read,
    "fs.write": h_fs_write,
    "fs.delete": h_fs_delete,
    "proc.list": h_proc_list,
    "proc.run": h_proc_run,
    "proc.kill": h_proc_kill,
    "ping": h_ping,
    "dns": h_dns,
    "trace": h_trace,
    "net.map": h_net_map,
    "net.scan": h_net_scan,
    "hack.wifi": h_hack_wifi,
    "port.scan": h_port_scan,
    "deep.trace": h_deep_trace,
    "breach.sim": h_breach_sim,
    "payload.deploy": h_payload_deploy,
    "ai.ask": h_ai_ask,
    "ai.scan": h_ai_scan,
    "render.noise": h_render_noise,
    "render.grid": h_render_grid,
    "render.glitch": h_render_glitch,
    "loop.scan": h_loop_scan,
    "loop.attack": h_loop_attack,
    "loop.random": h_loop_random
}

# generate many aliases
prefixes = ["scan","probe","audit","inspect","recon","map","seek","analyze","check","query"]
targets = ["core","kernel","net","cloud","node","cluster","gateway","service","process","sector","vault","engine"]
modes = ["fast","deep","full","lite","secure","stealth","burst","delta"]
for p in prefixes:
    for t in targets:
        base = f"{p}.{t}"
        COMMANDS[base] = make_sim(base, complexity=random.uniform(0.7,3.2))
        for m in modes:
            COMMANDS[f"{base}.{m}"] = make_sim(f"{base}.{m}", complexity=random.uniform(0.6,4.2))

# extra ops
for i in range(40):
    name = f"ops.{i}"
    COMMANDS[name] = make_sim(name, complexity=1.0 + (i % 4) * 0.5)

# finalize total count
TOTAL_CMDS = len(COMMANDS)

# ---------- DISPATCH ----------
def dispatch(raw):
    cmd, args = normalize(raw)
    if not cmd:
        return
    # direct address to karen
    if cmd == "karen":
        if args:
            karen_say(" ".join(args))
        else:
            karen_status()
        return
    # allow "help full" as special
    if cmd in ["help", "help.all", "help all"] and (not args or args == ["all"]):
        if args and args[0] == "all":
            h_help_all(args)
            return
    # lookup command
    if cmd in COMMANDS:
        try:
            COMMANDS[cmd](args)
        except Exception as e:
            instant(f"[error] handler exception: {e}")
    else:
        instant("Unknown command. Type 'help'.")

# ---------- BANNER & REPL ----------
def banner():
    instant("=== KarenOS Terminal ===")
    instant(f"Loaded commands: {TOTAL_CMDS}")
    instant("Type 'help' or 'help all'. Type 'exit' to quit.\n")

def repl():
    banner()
    while True:
        try:
            raw = input(PROMPT)
            dispatch(raw)
            # show occasional hidden events
            if random.random() < 0.06 and bg_events:
                t, ev = bg_events[-1], bg_events[-1]
                instant(f"[event] {ev}")
        except KeyboardInterrupt:
            instant("\n(Interrupted) use 'exit' to quit.")
        except EOFError:
            instant("\nEOF received. Exiting."); break

if __name__ == "__main__":
    repl()
