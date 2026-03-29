#!/bin/bash

# --- KONFIGURACJA ---
BASE_DIR="biometric_data"
MAPPING_FILE="mapping.txt"

# Sprawdzenie czy folder istnieje
if [ ! -d "$BASE_DIR" ]; then
    echo "Błąd: Katalog '$BASE_DIR' nie istnieje!"
    exit 1
fi

# Czyszczenie starego pliku mapowania
> "$MAPPING_FILE"

echo "Rozpoczynam proces anonimizacji..."

# Licznik dla użytkowników
user_count=1

# Iteracja po podfolderach w biometric_data
# Sortujemy, aby zachować stałą kolejność przy każdym uruchomieniu
find "$BASE_DIR" -mindepth 1 -maxdepth 1 -type d | sort | while read -r user_path; do
    
    old_user_name=$(basename "$user_path")
    new_user_name=$(printf "user_%02d" $user_count)
    new_user_path="$BASE_DIR/$new_user_name"

    echo "Przetwarzanie: $old_user_name -> $new_user_name"
    echo "$old_user_name = $new_user_name" >> "$MAPPING_FILE"

    # 1. Najpierw zmieniamy nazwy plików wewnątrz folderu
    for file in "$user_path"/*.csv; do
        if [ -f "$file" ]; then
            # Wyciągamy numer z końca nazwy pliku (np. z 'Adam_5.csv' wyciąga '5')
            # Używamy prostej operacji na stringach, żeby działało na każdym systemie
            filename=$(basename "$file")
            # Usuwamy wszystko co nie jest cyfrą przed rozszerzeniem .csv
            num=$(echo "$filename" | sed 's/[^0-9]//g')
            
            # Jeśli nie udało się znaleźć numeru, używamy domyślnego "X"
            [ -z "$num" ] && num="raw"

            mv "$file" "$user_path/${new_user_name}_${num}.csv"
        fi
    done

    # 2. Zmieniamy nazwę samego folderu użytkownika
    mv "$user_path" "$new_user_path"

    ((user_count++))
done

echo "--------------------------------------"
echo "Gotowe! Dane zostały zanonimizowane."
echo "Mapowanie znajdziesz w pliku: $MAPPING_FILE"
