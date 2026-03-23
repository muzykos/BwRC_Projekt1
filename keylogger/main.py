import time
import argparse
import sys
import os
from pynput import keyboard
import termios

# Wyłączamy wszystkie sygnały sterujące terminala (Ctrl+C, Z, S, Q, V)
if os.name == 'posix':
    # -isig: wyłącza Ctrl+C, Ctrl+Z, Ctrl+\
    # -ixon: wyłącza Ctrl+S, Ctrl+Q
    # -iexten: wyłącza Ctrl+V i Ctrl+O
    os.system("stty -isig -ixon -iexten")

# Konfiguracja argumentów
parser = argparse.ArgumentParser(description="Biometryczny rejestrator zdarzeń klawiatury.")
parser.add_argument("--name", type=str, default="biometric_data", help="Nazwa użytkownika/sesji")
parser.add_argument("--file", type=str, default="sentences.txt", help="Plik tekstowy ze zdaniami")
args = parser.parse_args()

# --- LOGIKA TWORZENIA STRUKTURY PLIKÓW ---
user_dir = args.name

# 1. Tworzymy folder o nazwie użytkownika (jeśli nie istnieje)
if not os.path.exists(user_dir):
    os.makedirs(user_dir)

# 2. Szukamy kolejnego wolnego indeksu N
n = 1
while True:
    potential_name = f"{args.name}_{n}.csv"
    full_path = os.path.join(user_dir, potential_name)
    if not os.path.exists(full_path):
        LOG_FILE = full_path
        break
    n += 1

SENTENCES_FILE = args.file

# Wczytywanie zdań z pliku
try:
    with open(SENTENCES_FILE, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Błąd: Nie znaleziono pliku '{SENTENCES_FILE}'.")
    sys.exit(1)

if not sentences:
    print("Błąd: Plik ze zdaniami jest pusty.")
    sys.exit(1)

sentence_index = 0

def show_next_sentence():
    global sentence_index
    if sentence_index < len(sentences):
        print(f"\n[Zadanie {sentence_index + 1}/{len(sentences)}]")
        print(f"PROSZĘ WPISAĆ ZDANIE: \n{sentences[sentence_index]}")
        sentence_index += 1
    else:
        print("\n--- Koniec zdań. Naciśnij ESC, aby wyjść. ---")

def write_to_file(key_name, action):
    global_time = time.time()
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{global_time}; {key_name}; {action}\n")
    except Exception as e:
        print(f"Błąd zapisu: {e}")

def on_press(key):
    try:
        key_name = key.char if hasattr(key, 'char') else str(key)
    except AttributeError:
        key_name = str(key)
    write_to_file(key_name, "keydown")

def on_release(key):
    try:
        key_name = key.char if hasattr(key, 'char') else str(key)
    except AttributeError:
        key_name = str(key)
    
    write_to_file(key_name, "keyup")

    if key == keyboard.Key.enter:
        show_next_sentence()

    if key == keyboard.Key.esc:
        print(f"\nZakończono. Dane zapisane w: {LOG_FILE}")
        return False

# Start programu
print(f"Sesja dla: {args.name}")
print(f"Plik wyjściowy: {LOG_FILE}")
show_next_sentence()

# Listener z opcją suppress=True (opcjonalnie, jeśli chcesz blokować terminal)
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Czyszczenie bufora terminala po zakończeniu
try:
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
except:
    pass

# Przywracamy domyślne ustawienia terminala
if os.name == 'posix':
    os.system("stty isig ixon iexten")