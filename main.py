import os
import time
import random
import platform

# ==============================
#  АНИМАЦИИ
# ==============================

def anim_delay(text, min_t=0.02, max_t=0.05):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(random.uniform(min_t, max_t))
    print()

def anim_loader(text="Загрузка", duration=2):
    print(text, end="", flush=True)
    for _ in range(duration * 5):
        print(".", end="", flush=True)
        time.sleep(0.2)
    print()

def anim_scan(title="Сканирование", duration=2):
    anim_delay(f"{title}:")
    bars = ["▖","▘","▝","▗"]
    end_time = time.time() + duration
    while time.time() < end_time:
        print("  [" + random.choice(bars) * 10 + "]", end="\r", flush=True)
        time.sleep(0.1)
    print("  [##########]")

def anim_progress(title="Обработка", duration=3):
    anim_delay(f"{title}:")
    total = 30
    for i in range(total + 1):
        bar = "#" * i + "-" * (total - i)
        print(f"[{bar}] {int((i/total)*100)}%", end="\r")
        time.sleep(duration / total)
    print()


# ==============================
#  ВНУТРЕННЯЯ ФАЙЛОВАЯ СИСТЕМА
# ==============================

FILES = {
    "/system/info": "System Kernel v2.4.1\nCopyright (c)",
    "/logs/boot": "System boot log...\nEverything OK.",
    "/user/readme.txt": "Тестовый файл."
}

def fs_list(args):
    path = args[0] if args else "/"
    anim_scan("Чтение диска", 1)
    print("Файлы:")
    for f in FILES:
        if f.startswith(path):
            print(" ", f)

def fs_read(args):
    if not args:
        print("Укажи путь.")
        return
    path = args[0]
    anim_scan("Чтение файла", 1)
    if path in FILES:
        print(FILES[path])
    else:
        print("Файл не найден.")

def fs_write(args):
    if len(args) < 2:
        print("Используй: write путь текст")
        return
    path = args[0]
    text = " ".join(args[1:])
    anim_progress("Запись", 1)
    FILES[path] = text
    print("Файл записан.")

def fs_delete(args):
    if not args:
        print("Укажи путь.")
        return
    path = args[0]
    if path in FILES:
        anim_progress("Удаление", 1)
        del FILES[path]
        print("Файл удалён.")
    else:
        print("Файла нет.")


# ==============================
#  СЕТЕВЫЕ ФЕЙК-ОПЕРАЦИИ (БЕЗОПАСНЫЕ)
# ==============================

def net_ping(args):
    if not args:
        print("Используй: ping HOST")
        return
    host = args[0]
    anim_scan(f"PING {host}", 2)
    print("Ответов: 4 пакета OK")

def net_dns(args):
    if not args:
        print("Используй: dns имя")
        return
    domain = args[0]
    anim_loader("DNS запрос", 2)
    print(f"{domain} -> 192.168.{random.randint(0,255)}.{random.randint(1,254)}")

def net_trace(args):
    if not args:
        print("Используй: trace host")
        return
    host = args[0]
    anim_delay("Трассировка маршрута:")
    for i in range(1, random.randint(4,10)):
        time.sleep(0.2)
        print(f"{i:2d}   10.0.{i}.{random.randint(1,254)}   OK")
    print("Готово.")


# ==============================
#  СИСТЕМА
# ==============================

def sys_info(args):
    anim_scan("Сбор системы", 1)
    print(f"OS: {platform.system()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")

def sys_time(args):
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

def sys_clear(args):
    os.system("clear" if os.name != "nt" else "cls")

def sys_reboot(args):
    anim_progress("Выключение", 2)
    anim_loader("Загрузка", 3)
    print("Готово.")


# ==============================
#  ПРОЦЕССЫ
# ==============================

process_list = []

def proc_list(args):
    anim_scan("Получение процессов", 1)
    if not process_list:
        print("Нет процессов.")
    for p in process_list:
        print(f"- {p}")

def proc_run(args):
    if not args:
        print("Имя процесса?")
        return
    name = " ".join(args)
    anim_loader("Запуск процесса", 1)
    process_list.append(name)
    print("Процесс запущен.")

def proc_kill(args):
    if not args:
        print("Имя процесса?")
        return
    name = " ".join(args)
    if name in process_list:
        anim_progress("Завершение", 1)
        process_list.remove(name)
        print("Убит.")
    else:
        print("Такого процесса нет.")


# ==============================
#  ПРОЧИЕ КОМАНДЫ
# ==============================

def cmd_help(args):
    print("Команды:")
    for c in COMMANDS:
        print(" ", c)

def cmd_echo(args):
    print(" ".join(args))

def cmd_exit(args):
    print("Выход...")
    exit()

def cmd_random(args):
    n = random.randint(0, 999999)
    print("Случайное число:", n)

def cmd_scan(args):
    anim_scan("Сканирование системы", 2)
    print("Состояние стабильное.")

def cmd_load(args):
    anim_progress("Загрузка ресурсов", 3)
    print("Завершено.")


# ==============================
#  РЕЕСТР ВСЕХ КОМАНД (45+)
# ==============================

COMMANDS = {
    "help": cmd_help,
    "clear": sys_clear,
    "exit": cmd_exit,
    "echo": cmd_echo,
    "random": cmd_random,
    "time": sys_time,
    "sysinfo": sys_info,
    "reboot": sys_reboot,
    "scan": cmd_scan,
    "load": cmd_load,
    "ping": net_ping,
    "dns": net_dns,
    "trace": net_trace,
    "fs.list": fs_list,
    "fs.read": fs_read,
    "fs.write": fs_write,
    "fs.delete": fs_delete,
    "proc.list": proc_list,
    "proc.run": proc_run,
    "proc.kill": proc_kill,
}

# ==============================
#  ОСНОВНОЙ ЦИКЛ
# ==============================

def main():
    anim_loader("Инициализация", 2)
    anim_delay("Система готова.")
    while True:
        try:
            cmd = input("> ").strip()
            if not cmd:
                continue
            parts = cmd.split()
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
