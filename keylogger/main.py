import time
import argparse
import sys
import os
from pynput import keyboard
import termios

# --- USTAWIENIA TERMINALA (Blokada Ctrl+C, S, itp.) ---
if os.name == 'posix':
    os.system("stty -isig -ixon -iexten")

# Konfiguracja argumentów
parser = argparse.ArgumentParser(description="Biometryczny rejestrator zdarzeń klawiatury.")
parser.add_argument("--name", type=str, default="biometric_data", help="Nazwa użytkownika/sesji")
parser.add_argument("--file", type=str, default="sentences.txt", help="Plik tekstowy ze zdaniami")
args = parser.parse_args()

# Tworzymy folder użytkownika
user_dir = args.name
if not os.path.exists(user_dir):
    os.makedirs(user_dir)

# Wczytywanie zdań z pliku
try:
    with open(args.file, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Błąd: Nie znaleziono pliku '{args.file}'.")
    os.system("stty isig ixon iexten") # Przywrócenie terminala przed wyjściem
    sys.exit(1)

# Zmienne globalne sterujące stanem
sentence_index = 0
current_log_file = ""
should_exit_total = False # Czy użytkownik wcisnął ESC (całkowite wyjście)

def show_next_sentence():
    global sentence_index
    if sentence_index < len(sentences):
        print(f"\n[Zadanie {sentence_index + 1}/{len(sentences)}]")
        print(f"PROSZĘ WPISAĆ ZDANIE: \n{sentences[sentence_index]}")
        sentence_index += 1
    else:
        print("\n--- Seria zakończona. Przygotowanie kolejnej... ---")

def write_to_file(key_name, action):
    global_time = time.time()
    try:
        with open(current_log_file, "a", encoding="utf-8") as f:
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
    global sentence_index, should_exit_total
    try:
        key_name = key.char if hasattr(key, 'char') else str(key)
    except AttributeError:
        key_name = str(key)
    
    write_to_file(key_name, "keyup")

    if key == keyboard.Key.enter:
        # Jeśli to był ostatni Enter w serii, kończymy ten Listener
        if sentence_index >= len(sentences):
            return False 
        show_next_sentence()

    if key == keyboard.Key.esc:
        should_exit_total = True
        return False

# --- GŁÓWNA PĘTLA 5 TESTÓW ---
# Znajdujemy bazowy numer sesji, żeby nie nadpisywać starych folderów
base_n = 1
while os.path.exists(os.path.join(user_dir, f"{args.name}_{base_n}.csv")):
    base_n += 1

print(f"Rozpoczynam badanie dla: {args.name}")

for test_num in range(1, 6):
    if should_exit_total:
        break
        
    # Ustalenie nazwy pliku dla tej konkretnej iteracji
    current_log_file = os.path.join(user_dir, f"{args.name}_{base_n + test_num - 1}.csv")
    sentence_index = 0
    
    print(f"\n" + "="*30)
    print(f" TEST {test_num}/5 ")
    print(f" Zapis do: {current_log_file}")
    print("="*30)
    
    show_next_sentence()

    # Uruchomienie nasłuchiwania dla jednego pliku
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    if not should_exit_total and test_num < 5:
        print("\nGotowy do kolejnego testu? Naciśnij dowolny klawisz (lub poczekaj)...")
        time.sleep(1)

# --- ZAKOŃCZENIE ---
print(f"\nBadanie zakończone. Wszystkie pliki w folderze: {user_dir}")

# Przywracamy terminal
if os.name == 'posix':
    os.system("stty isig ixon iexten")

try:
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
except:
    pass