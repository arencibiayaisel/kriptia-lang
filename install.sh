#!/bin/bash
echo "========================================="
echo "   Instalando Kriptia Programming Language"
echo "========================================="

# 1. Verificar si g++ está instalado
if ! command -v g++ &> /dev/null; then
    echo "[!] Error: Se necesita un compilador de C++ (g++). Instálalo con: pkg install build-essential"
    exit 1
fi

# 2. Descargar o clonar el código fuente temporalmente
echo "[+] Descargando Kriptia..."
git clone https://github.com/tu-usuario/kriptia-lang.git ~/.kriptia-src

# 3. Compilar de forma nativa
echo "[+] Compilando motor nativo..."
cd ~/.kriptia-src
g++ kriptia_core.cpp -o kriptia -O3

# 4. Mover a la ruta global del sistema (compatible con Termux y Linux)
if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    mv kriptia /data/data/com.termux/files/usr/bin/kriptia
else
    sudo mv kriptia /usr/local/bin/kriptia
fi

# 5. Limpieza
cd ~
rm -rf ~/.kriptia-src

echo "========================================="
echo " ¡Kriptia se ha instalado con éxito!"
echo " Ejecuta tus programas usando: kriptia archivo.kriptia"
echo "========================================="
