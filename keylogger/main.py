import time
import argparse
import sys
from pynput import keyboard
import termios

# Konfiguracja argumentów
parser = argparse.ArgumentParser(description="Biometryczny rejestrator zdarzeń klawiatury.")
parser.add_argument("--name", type=str, default="biometric_data", help="Nazwa pliku wyjściowego (bez .csv)")
parser.add_argument("--file", type=str, default="sentences.txt", help="Plik tekstowy ze zdaniami do przepisania")
args = parser.parse_args()

LOG_FILE = f"{args.name}.csv"
SENTENCES_FILE = args.file

# Wczytywanie zdań z pliku
try:
    with open(SENTENCES_FILE, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Błąd: Nie znaleziono pliku '{SENTENCES_FILE}'. Utwórz go i dodaj zdania.")
    sys.exit(1)

if not sentences:
    print("Błąd: Plik ze zdaniami jest pusty.")
    sys.exit(1)

# Globalny licznik zdań
sentence_index = 0

def show_next_sentence():
    global sentence_index
    if sentence_index < len(sentences):
        print(f"\n[Zadanie {sentence_index + 1}/{len(sentences)}]")
        print(f"PROSZĘ WPISAĆ ZDANIE: \n{sentences[sentence_index]}")
        sentence_index += 1
    else:
        print("\n--- Koniec zdań w pliku. Naciśnij ESC, aby wyjść. ---")

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

    # Logika zmiany zdania po Enterze
    if key == keyboard.Key.enter:
        show_next_sentence()

    # Wyjście ze skryptu
    if key == keyboard.Key.esc:
        print(f"\nZakończono. Dane zapisane w: {LOG_FILE}")
        return False

# Start programu
print(f"Rejestracja dla użytkownika: {args.name}")
show_next_sentence()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

termios.tcflush(sys.stdin, termios.TCIFLUSH)
