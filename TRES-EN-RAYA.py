import tkinter as tk
from tkinter import messagebox
import random

class TresEnRaya:
    def __init__(self, root):
        self.root = root
        self.root.geometry("750x550")
        self.root.configure(bg="#FDE2E4")

        self.tablero = [""] * 9
        self.jugador_actual = "X"
        self.victorias_jugador = 0
        self.victorias_ai = 0

        # Pantalla de bienvenida
        self.crear_pantalla_bienvenida()

        # Pantalla del juego
        self.crear_pantalla_juego()

    def crear_pantalla_bienvenida(self):
        self.frame_bienvenida = tk.Frame(self.root, bg="#FDE2E4")
        self.frame_bienvenida.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.frame_bienvenida, text="¡Bienvenido al juego Tres en Raya!", 
                font=("Helvetica", 16 , "bold" ), bg="#FDE2E4", fg="#FF8FAB").pack(pady=10)
        
        self.entry_nombre = tk.Entry(self.frame_bienvenida, font=("Helvetica", 14))
        self.entry_nombre.pack(pady=10)

        tk.Label(self.frame_bienvenida, text="Selecciona la dificultad:", 
                font=("Helvetica", 14 ), bg="#FDE2E4", fg="#FF8FAB").pack(pady=5)

        self.opciones_dificultad = tk.StringVar(value="Normal")
        for nivel in ["Fácil", "Normal", "Difícil"]:
            tk.Radiobutton(self.frame_bienvenida, text=nivel, variable=self.opciones_dificultad, 
                        value=nivel, bg="#FDE2E4", fg="#525453", font=("Helvetica", 14)).pack()

        tk.Button(self.frame_bienvenida, text="Iniciar juego", command=self.iniciar_juego, 
                font=("Helvetica", 14 ), bg="#FFCCCB" ,  fg="#525453").pack(pady=15)

    def crear_pantalla_juego(self):
        self.frame_juego = tk.Frame(self.root, bg="#FDE2E4")

        tk.Label(self.frame_juego, text="Juego Tres en Raya", 
                font=("Helvetica", 26, "bold"), bg="#FDE2E4", fg="#FF8FAB").grid(row=0, column=0, columnspan=3, pady=10)

        self.label_victorias = tk.Label(self.frame_juego, text="", font=("Helvetica", 14), bg="#FDE2E4", fg="#FF8FAB")
        self.label_victorias.grid(row=1, column=0, columnspan=3)

        self.botonera = [tk.Button(self.frame_juego, text="", font=("Helvetica", 25), width=5, height=2, bg="#FFFFFF", 
                                relief="flat", command=lambda i=i: self.movimiento_jugador(i)) for i in range(9)]
        for i, boton in enumerate(self.botonera):
            boton.grid(row=(i // 3) + 2, column=i % 3, padx=8, pady=8)

        tk.Button(self.frame_juego, text="Salir", command=self.root.quit, 
                font=("Helvetica", 14), bg="#FF8FAB", fg="#FFFFFF", relief="flat").grid(row=5, column=0, columnspan=3)

    def iniciar_juego(self):
        self.nombre_jugador = self.entry_nombre.get() or "Jugador"
        self.dificultad = self.opciones_dificultad.get()
        self.frame_bienvenida.pack_forget()  # Ocultar la pantalla de bienvenida
        self.frame_juego.place(relx=0.5, rely=0.5, anchor="center")
        self.reiniciar_juego()  
        self.actualizar_victorias()

    def movimiento_jugador(self, indice):
        if self.tablero[indice] == "":
            self.actualizar_movimiento(indice, "X", "#FF6B6B")
            if not self.fin_del_juego():
                self.jugador_actual = "O"
                self.root.after(200, self.movimiento_ai)

    def movimiento_ai(self):
        indice = self.seleccionar_movimiento_ai()
        self.actualizar_movimiento(indice, "O", "#b76bff")
        if not self.fin_del_juego():
            self.jugador_actual = "X"

    def actualizar_movimiento(self, indice, jugador, color):
        self.tablero[indice] = jugador
        self.botonera[indice].config(text=jugador, fg=color)

    def seleccionar_movimiento_ai(self):
        if self.dificultad == "Fácil":
            return random.choice([i for i, x in enumerate(self.tablero) if x == ""])
        return self.minimax(self.tablero, "O")["indice"]

    def minimax(self, tablero, jugador):
        ganador = self.verificar_ganador()
        if ganador == "X":
            return {"puntaje": -1}
        elif ganador == "O":
            return {"puntaje": 1}
        elif "" not in tablero:
            return {"puntaje": 0}

        movimientos = []
        for i in range(9):
            if tablero[i] == "":
                tablero[i] = jugador
                puntaje = self.minimax(tablero, "X" if jugador == "O" else "O")["puntaje"]
                movimientos.append({"indice": i, "puntaje": puntaje})
                tablero[i] = ""

        if jugador == "O":
            return max(movimientos, key=lambda x: x["puntaje"])
        return min(movimientos, key=lambda x: x["puntaje"])

    def verificar_ganador(self):
        combinaciones = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
                        (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                        (0, 4, 8), (2, 4, 6)]
        for a, b, c in combinaciones:
            if self.tablero[a] == self.tablero[b] == self.tablero[c] != "":
                return self.tablero[a]
        return None

    def fin_del_juego(self):
        ganador = self.verificar_ganador()
        if ganador:
            messagebox.showinfo("Juego terminado", f"¡{ganador} gana! 🎉")
            self.actualizar_victorias(ganador)
            self.reiniciar_juego()
            return True
        elif "" not in self.tablero:
            messagebox.showinfo("Juego terminado", "¡Empate! 😊")
            self.reiniciar_juego()
            return True
        return False

    def actualizar_victorias(self, ganador=None):
        if ganador == "X":
            self.victorias_jugador += 1
        elif ganador == "O":
            self.victorias_ai += 1
        self.label_victorias.config(text=f"{self.nombre_jugador} (X): {self.victorias_jugador}  | IA (O): {self.victorias_ai}")

    def reiniciar_juego(self):
        self.tablero = [""] * 9
        for boton in self.botonera:
            boton.config(text="", fg="#FFFFFF")
        self.jugador_actual = "X"

if __name__ == "__main__":
    root = tk.Tk()
    juego = TresEnRaya(root)
    root.mainloop()
