import sys

class InterpretadorKriptia:
    def __init__(self):
        self.variables = {}
        self.funciones = {}

    def ejecutar_archivo(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
                self.ejecutar_bloque(lineas)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{ruta_archivo}'")

    def ejecutar_bloque(self, lineas):
        i = 0
        while i < len(lineas):
            linea = lineas[i].strip()
            
            # Ignorar comentarios o líneas vacías
            if not linea or linea.startswith("//"):
                i += 1
                continue

            # Comando MOSTRAR (Ej: mostrar("Hola"))
            if linea.startswith("mostrar("):
                contenido = linea[8:-1].strip()
                resultado = self.evaluar_expresion(contenido)
                print(resultado)

            # Comando LEER (Ej: variable nombre = leer("¿Cómo te llamas? "))
            elif "=" in linea and "leer(" in linea:
                partes = linea.split("=", 1)
                nombre_var = partes[0].replace("variable", "").strip()
                llamada_leer = partes[1].strip()
                
                # Extraer el texto del prompt de leer(...)
                prompt = ""
                if llamada_leer.startswith("leer(") and llamada_leer.endswith(")"):
                    prompt_expr = llamada_leer[5:-1].strip()
                    prompt = str(self.evaluar_expresion(prompt_expr))
                
                # Capturar input del usuario
                valor_ingresado = input(prompt)
                
                # Intentar convertir a número si es posible
                try:
                    if "." in valor_ingresado:
                        valor_ingresado = float(valor_ingresado)
                    else:
                        valor_ingresado = int(valor_ingresado)
                except ValueError:
                    pass
                
                self.variables[nombre_var] = valor_ingresado

            # Declaración de VARIABLE normal (Ej: variable x = 5)
            elif linea.startswith("variable "):
                partes = linea[9:].split("=", 1)
                nombre_var = partes[0].strip()
                valor_var = self.evaluar_expresion(partes[1].strip())
                self.variables[nombre_var] = valor_var

            # Reasignación de VARIABLE (Ej: contador = contador + 1)
            elif "=" in linea and not linea.startswith("funcion "):
                partes = linea.split("=", 1)
                nombre_var = partes[0].strip()
                if nombre_var in self.variables or not " " in nombre_var:
                    valor_var = self.evaluar_expresion(partes[1].strip())
                    self.variables[nombre_var] = valor_var

            # Definición de FUNCION (Ej: funcion saludar(nombre))
            elif linea.startswith("funcion "):
                cabecera = linea[8:].strip()
                nombre_func = cabecera.split("(")[0].strip()
                
                # Extraer argumentos
                args_str = cabecera[cabecera.find("(")+1 : cabecera.find(")")]
                argumentos = [arg.strip() for arg in args_str.split(",") if arg.strip()]
                
                # Capturar cuerpo de la función hasta "fin"
                cuerpo_func = []
                i += 1
                while i < len(lineas):
                    sub_linea = lineas[i].strip()
                    if sub_linea == "fin":
                        break
                    cuerpo_func.append(lineas[i])
                    i += 1
                
                self.funciones[nombre_func] = {"args": argumentos, "cuerpo": cuerpo_func}

            # Estructura CONDICIONAL (Ej: si x > 5 entonces)
            elif linea.startswith("si "):
                condicion_texto = linea[3:].replace("entonces", "").strip()
                
                bloque_verdadero = []
                bloque_falso = []
                i += 1
                en_falso = False
                
                while i < len(lineas):
                    sub_linea = lineas[i].strip()
                    if sub_linea == "fin":
                        break
                    elif sub_linea == "sino":
                        en_falso = True
                        i += 1
                        continue
                    
                    if en_falso:
                        bloque_falso.append(lineas[i])
                    else:
                        bloque_verdadero.append(lineas[i])
                    i += 1

                if self.evaluar_condicion(condicion_texto):
                    self.ejecutar_bloque(bloque_verdadero)
                elif bloque_falso:
                    self.ejecutar_bloque(bloque_falso)

            # Estructura BUCLE MIENTRAS (Ej: mientras x < 5 repetir)
            elif linea.startswith("mientras "):
                condicion_texto = linea[8:].replace("repetir", "").strip()
                
                cuerpo_bucle = []
                i += 1
                while i < len(lineas):
                    sub_linea = lineas[i].strip()
                    if sub_linea == "fin":
                        break
                    cuerpo_bucle.append(lineas[i])
                    i += 1
                
                while self.evaluar_condicion(condicion_texto):
                    self.ejecutar_bloque(cuerpo_bucle)

            # Llamada a función suelta en el código
            elif "(" in linea and ")" in linea and not linea.startswith("mostrar("):
                self.evaluar_expresion(linea)

            i += 1

    def evaluar_expresion(self, expr):
        expr = expr.strip()
        
        # Llamada a función dentro de una expresión (Ej: saludar("Yaisel"))
        if "(" in expr and expr.endswith(")"):
            nombre_func = expr.split("(")[0].strip()
            args_str = expr[expr.find("(")+1 : expr.rfind(")")]
            args_vals = [self.evaluar_expresion(arg.strip()) for arg in args_str.split(",") if arg.strip()]
            
            if nombre_func in self.funciones:
                func_data = self.funciones[nombre_func]
                # Guardar variables locales / contexto temporal
                variables_antiguas = self.variables.copy()
                
                # Asignar argumentos a parámetros locales
                for idx, arg_name in enumerate(func_data["args"]):
                    if idx < len(args_vals):
                        self.variables[arg_name] = args_vals[idx]
                
                # Ejecutar cuerpo de la función
                # (Nota: soporta impresión directa o lógica interna)
                self.ejecutar_bloque(func_data["cuerpo"])
                
                # Restaurar variables
                self.variables = variables_antiguas
                return None

        # Si es un texto entre comillas
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # Si contiene operaciones matemáticas básicas (Ej: contador + 1)
        for op in ["+", "-", "*", "/"]:
            if op in expr and not expr.startswith('"'):
                partes = expr.split(op)
                izq = self.evaluar_expresion(partes[0])
                der = self.evaluar_expresion(partes[1])
                try:
                    if op == "+": return izq + der
                    if op == "-": return izq - der
                    if op == "*": return izq * der
                    if op == "/": return izq / der
                except:
                    pass

        # Si es un número decimal o entero
        try:
            if "." in expr:
                return float(expr)
            return int(expr)
        except ValueError:
            pass

        # Si es una variable guardada
        if expr in self.variables:
            return self.variables[expr]

        return expr

    def evaluar_condicion(self, condicion):
        for operador in [">=", "<=", ">", "<", "=="]:
            if operador in condicion:
                partes = condicion.split(operador)
                izq = self.evaluar_expresion(partes[0].strip())
                der = self.evaluar_expresion(partes[1].strip())
                
                if operador == ">": return izq > der
                if operador == "<": return izq < der
                if operador == ">=": return izq >= der
                if operador == "<=": return izq <= der
                if operador == "==": return izq == der
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python kriptia.py archivo.kriptia")
    else:
        interpretador = InterpretadorKriptia()
        interpretador.ejecutar_archivo(sys.argv[1])
