#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <sstream>

// Definición de los Tipos de Tokens para el Analizador Léxico
enum class TipoToken {
    PALABRA_CLAVE,
    IDENTIFICADOR,
    NUMERO,
    TEXTO,
    OPERADOR,
    SIMBOLO,
    DESCONOCIDO
};

struct Token {
    TipoToken tipo;
    std::string valor;
};

// Clase principal del motor de Kriptia
class KriptiaEngine {
private:
    std::unordered_map<std::string, std::string> variables;

    // Analizador Léxico (Lexer): Rompe el código fuente en tokens comprensibles
    std::vector<Token> analizarLexico(const std::string& codigo) {
        std::vector<Token> tokens;
        size_t i = 0;
        while (i < codigo.length()) {
            char c = codigo[i];

            // Ignorar espacios en blanco
            if (isspace(c)) {
                i++;
                continue;
            }

            // Identificar cadenas de texto entre comillas
            if (c == '"') {
                std::string literal = "";
                i++;
                while (i < codigo.length() && codigo[i] != '"') {
                    literal += codigo[i];
                    i++;
                }
                i++; // Saltar la comilla de cierre
                tokens.push_back({TipoToken::TEXTO, literal});
                continue;
            }

            // Identificar números
            if (isdigit(c)) {
                std::string num = "";
                while (i < codigo.length() && (isdigit(codigo[i]) || codigo[i] == '.')) {
                    num += codigo[i];
                    i++;
                }
                tokens.push_back({TipoToken::NUMERO, num});
                continue;
            }

            // Identificar palabras clave o identificadores (variables/funciones)
            if (isalpha(c) || c == '_') {
                std::string palabra = "";
                while (i < codigo.length() && (isalnum(codigo[i]) || codigo[i] == '_')) {
                    palabra += codigo[i];
                    i++;
                }
                tokens.push_back({TipoToken::PALABRA_CLAVE, palabra});
                continue;
            }

            // Operadores y símbolos
            if (c == '=' || c == '+' || c == '-' || c == '*' || c == '/' || c == '>' || c == '<') {
                tokens.push_back({TipoToken::OPERADOR, std::string(1, c)});
                i++;
                continue;
            }

            if (c == '(' || c == ')' || c == ',') {
                tokens.push_back({TipoToken::SIMBOLO, std::string(1, c)});
                i++;
                continue;
            }

            i++;
        }
        return tokens;
    }

public:
    // Método para ejecutar archivos fuente de Kriptia
    void ejecutarArchivo(const std::string& rutaArchivo) {
        std::ifstream archivo(rutaArchivo);
        if (!archivo.is_open()) {
            std::cerr << "Error crítico: No se pudo abrir el archivo fuente '" << rutaArchivo << "'" << std::endl;
            return;
        }

        std::string linea;
        std::cout << "\n[Kriptia Engine v1.0 - Compilando y Ejecutando Nativamente]\n" << std::endl;

        while (std::getline(archivo, linea)) {
            // Limpiar espacios de la línea
            size_t inicio = linea.find_first_not_of(" \t\r\n");
            if (inicio == std::string::npos) continue; // Línea vacía
            linea = linea.substr(inicio);

            if (linea.rfind("//", 0) == 0) continue; // Comentario

            // Procesar comando mostrar(...)
            if (linea.rfind("mostrar(", 0) == 0) {
                size_t fin = linea.rfind(')');
                if (fin != std::string::npos) {
                    std::string contenido = linea.substr(8, fin - 8);
                    // Evaluar si es texto plano entre comillas
                    if (contenido.front() == '"' && contenido.back() == '"') {
                        std::cout << contenido.substr(1, contenido.length() - 2) << std::endl;
                    } else if (variables.find(contenido) != variables.end()) {
                        std::cout << variables[contenido] << std::endl;
                    }
                }
            }
            // Procesar declaración de variables (Ej: variable x = 10)
            else if (linea.rfind("variable ", 0) == 0) {
                size_t posIgual = linea.find('=');
                if (posIgual != std::string::npos) {
                    std::string nombreVar = linea.substr(9, posIgual - 9);
                    // Limpiar espacios del nombre de la variable
                    nombreVar.erase(nombreVar.find_last_not_of(" \t\n\r") + 1);
                    
                    std::string valorVar = linea.substr(posIgual + 1);
                    // Limpiar espacios del valor
                    size_t noEspacio = valorVar.find_first_not_of(" \t");
                    valorVar = (noEspacio == std::string::npos) ? "" : valorVar.substr(noEspacio);
                    valorVar.erase(valorVar.find_last_not_of(" \t\n\r") + 1);

                    if (valorVar.front() == '"' && valorVar.back() == '"') {
                        valorVar = valorVar.substr(1, valorVar.length() - 2);
                    }
                    variables[nombreVar] = valorVar;
                }
            }
        }
        archivo.close();
    }
};

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Uso profesional: ./kriptiac <archivo.kriptia>" << std::endl;
        return 1;
    }

    KriptiaEngine motor;
    motor.ejecutarArchivo(argv[1]);
    return 0;
}
