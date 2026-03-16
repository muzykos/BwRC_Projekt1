import time
from pynput import keyboard

# Nazwa pliku do zapisu danych
LOG_FILE = "biometric_data.csv"

def write_to_file(key_name, action):
    """Zapisuje dane w formacie: Globaltime; Key; action"""
    global_time = time.time()  # Precyzyjny czas UNIX (w sekundach)
    
    try:
        # Próba otwarcia pliku i dopisania linii
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            log_entry = f"{global_time}; {key_name}; {action}\n"
            f.write(log_entry)
            # Opcjonalnie: wypisywanie w konsoli dla podglądu
            print(log_entry.strip())
    except Exception as e:
        print(f"Błąd zapisu: {e}")

def on_press(key):
    try:
        # Obsługa zwykłych znaków
        key_name = key.char if hasattr(key, 'char') else str(key)
    except AttributeError:
        # Obsługa klawiszy specjalnych (Shift, Ctrl itp.)
        key_name = str(key)
        
    write_to_file(key_name, "keydown")

def on_release(key):
    try:
        key_name = key.char if hasattr(key, 'char') else str(key)
    except AttributeError:
        key_name = str(key)
        
    write_to_file(key_name, "keyup")

    # Zatrzymanie skryptu po naciśnięciu Esc (ułatwia testy)
    if key == keyboard.Key.esc:
        print("\nZakończono zbieranie danych.")
        return False

# Inicjalizacja nasłuchiwania
print(f"Rozpoczęto zbieranie danych do pliku: {LOG_FILE}")
print("Naciśnij ESC, aby zakończyć...")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()