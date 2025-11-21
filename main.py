import os
import time
import random
import platform

# =====================================================
#  АНРИАЛИСТИЧНЫЕ, НО КРАСИВЫЕ И БЕЗОПАСНЫЕ АНИМАЦИИ
# =====================================================

def slow(text, a=0.02, b=0.06):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(random.uniform(a, b))
    print()

def loader(text="Загрузка", sec=2):
    print(text, end="", flush=True)
    for _ in range(sec * 5):
        print(".", end="", flush=True)
        time.sleep(0.2)
    print()

def scan_anim(title="Сканирование", sec=3):
    slow(f"{title}:")
    bars = ["▖","▘","▝","▗"]
    end = time.time() + sec
    while time.time() < end:
        print(" [" + random.choice(bars) * 20 + "]", end="\r", flush=True)
        time.sleep(0.07)
    print(" [####################]")

def hack_anim(title="Взлом", sec=5):
    slow(f"{title}...")
    end = time.time() + sec
    charset = "01<>*#@%$&"
    while time.time() < end:
        line = "".join(random.choice(charset) for _ in range(60))
        print(line)
        time.sleep(0.03)
    print("[Доступ получен]")

def progress(title="Обработка", sec=3):
    slow(f"{title}:")
    total = 35
    for i in range(total + 1):
        bar = "#" * i + "-" * (total - i)
        print(f"[{bar}] {int((i/total)*100)}%", end="\r")
        time.sleep(sec / total)
    print()


# =====================================================
#  ПСЕВДО-ХАКЕРСКИЕ МОДУЛИ (БЕЗОПАСНЫЕ)
# =====================================================

def cmd_hackwifi(args):
    if not args:
        print("Используй: hack.wifi SSID")
        return
    ssid = args[0]
    hack_anim(f"Перебор ключей Wi‑Fi '{ssid}'", sec=random.randint(4,9))
    print(f"Ключ найден: {ssid}_key_{random.randint(1000,9999)}")

def cmd_portscan(args):
    if not args:
        print("Используй: port.scan IP")
        return
    ip = args[0]
    scan_anim(f"Сканирование портов {ip}", 4)
    for p in random.sample([22,80,443,3306,8080,21,25,3389,9001], random.randint(3,8)):
        print(f"Порт {p}/TCP — открыт")
    print("Готово.")

def cmd_deeptrace(args):
    if not args:
        print("Используй: deep.trace IP")
        return
    ip = args[0]
    slow("Инициализация глубокого трассирования…")
    hack_anim("Анализ пакетов", 4)
    print(f"Узел найден: {ip}\nМаршрут стабилен.\n")


# =====================================================
#  СИСТЕМА ФАЙЛОВ
# =====================================================

FILES = {
    "/system/info": "System Kernel v4.8.1 / OK",
    "/logs/boot": "Boot sequence log...",
    "/user/notes.txt": "Пусто."
}

def fs_list(args):
    path = args[0] if args else "/"
    scan_anim("Чтение диска", 1)
    print("Файлы:")
    for f in FILES:
        if f.startswith(path):
            print(" ", f)

def fs_read(args):
    if not args:
        print("Используй: fs.read путь")
        return
    p = args[0]
    scan_anim("Чтение файла", 1)
    print(FILES.get(p, "Нет файла."))

def fs_write(args):
    if len(args) < 2:
        print("Используй: fs.write путь текст")
        return
    p = args[0]
    t = " ".join(args[1:])
    progress("Запись", 1)
    FILES[p] = t
    print("Готово.")


# =====================================================
#  СЕТЬ
# =====================================================

def net_ping(args):
    if not args:
        print("Используй: ping HOST")
        return
    host = args[0]
    scan_anim(f"PING {host}", 2)
    for i in range(4):
        print(f"Ответ от {host}: время={random.randint(12,80)}мс")

def net_dns(args):
    if not args:
        print("Используй: dns домен")
        return
    d = args[0]
    loader("DNS запрос", 2)
    print(f"{d} -> 192.168.{random.randint(0,255)}.{random.randint(1,254)}")

def net_trace(args):
    if not args:
        print("Используй: trace host")
        return
    h = args[0]
    slow("Маршрут:")
    for i in range(1, random.randint(5,11)):
        print(f"{i:2d}   10.0.{i}.{random.randint(1,254)}   OK")
    print("Готово.")


# =====================================================
#  СИСТЕМА
# =====================================================

def sys_info(args):
    scan_anim("Сбор системы", 1)
    print(platform.system(), platform.version(), platform.machine())

def sys_time(args):
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

def sys_clear(args):
    os.system("clear")

def sys_reboot(args):
    progress("Перезапуск", 2)
    loader("Загрузка", 2)
    print("Старт.")


# =====================================================
#  ПРОЦЕССЫ
# =====================================================

processes = []

def proc_list(args):
    scan_anim("Получение процессов", 1)
    if not processes:
        print("Нет процессов.")
    for p in processes:
        print("-", p)

def proc_run(args):
    if not args:
        print("Имя процесса?")
        return
    n = " ".join(args)
    loader("Запуск", 1)
    processes.append(n)
    print("Запущено.")

def proc_kill(args):
    if not args:
        print("Имя?")
        return
    n = " ".join(args)
    if n in processes:
        progress("Остановка", 1)
        processes.remove(n)
        print("Убито.")
    else:
        print("Нет такого.")


# =====================================================
#  ПРОЧИЕ
# =====================================================

def cmd_help(args):
    print("Команды:")
    for c in COMMANDS:
        print(" ", c)

def cmd_exit(args):
    print("Выход…")
    exit()

def cmd_echo(args):
    print(" ".join(args))

def cmd_random(args):
    print("Случай:", random.randint(0,999999))

def cmd_scan(args):
    scan_anim("Сканирование системы", 3)
    print("Статус OK.")

def cmd_load(args):
    progress("Загрузка", 3)
    print("Готово.")


# =====================================================
#  РЕЕСТР ВСЕХ КОМАНД (40+)
# =====================================================

COMMANDS = {
    # системные
    "help": cmd_help,
    "exit": cmd_exit,
    "clear": sys_clear,
    "time": sys_time,
    "sysinfo": sys_info,
    "reboot": sys_reboot,

    # прочее
    "echo": cmd_echo,
    "random": cmd_random,
    "scan": cmd_scan,
    "load": cmd_load,

    # сеть
    "ping": net_ping,
    "dns": net_dns,
    "trace": net_trace,

    # псевдо-взлом
    "hack.wifi": cmd_hackwifi,
    "port.scan": cmd_portscan,
    "deep.trace": cmd_deeptrace,

    # файлы
    "fs.list": fs_list,
    "fs.read": fs_read,
    "fs.write": fs_write,

    # процессы
    "proc.list": proc_list,
    "proc.run": proc_run,
    "proc.kill": proc_kill,
}

# =====================================================
#  ОСНОВНОЙ ЦИКЛ
# =====================================================

def main():
    loader("Инициализация", 2)
    slow("Готово.")
    while True:
        try:
            raw = input("> ").strip()
            if not raw:
                continue
            parts = raw.split()
            name = parts[0]
            args = parts[1:]
            if name in COMMANDS:
                COMMANDS[name](args)
            else:
                print("Неизвестная команда.")
        except KeyboardInterrupt:
            print("\nВыход.")
            break

main()
