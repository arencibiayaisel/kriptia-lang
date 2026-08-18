#!/bin/bash

echo "[+] Instalando Kriptia Programming Language..."

# 1. Compilar el motor C++ con optimización máxima (-O3)
g++ kriptia_core.cpp -o kriptiac -O3

# 2. Verificar si la compilación fue exitosa
if [ -f "kriptiac" ]; then
    echo "[+] Compilación exitosa del núcleo nativo."
    
    # 3. Instalar globalmente según el entorno (Termux o Linux estándar)
    if [ -d "/data/data/com.termux/files/usr/bin" ]; then
        cp kriptiac /data/data/com.termux/files/usr/bin/kriptia
        chmod +x /data/data/com.termux/files/usr/bin/kriptia
        echo "[Éxito] Kriptia instalado globalmente en Termux."
    elif [ -d "/usr/local/bin" ]; then
        sudo cp kriptiac /usr/local/bin/kriptia
        sudo chmod +x /usr/local/bin/kriptia
        echo "[Éxito] Kriptia instalado globalmente en Linux."
    else
        echo "[Aviso] No se pudo mover a rutas globales, pero puedes usarlo localmente."
    fi
else
    echo "[Error] La compilación falló."
    exit 1
fi

echo "[+] ¡Kriptia está listo para usarse!"
