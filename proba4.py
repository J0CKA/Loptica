import customtkinter as ctk
import time

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Simulacija")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")

upper_height = int(screen_height * 3 / 5)
lower_height = screen_height - upper_height

upper_frame = ctk.CTkFrame(root, fg_color="lightblue", height=upper_height)
upper_frame.pack(fill="x")

canvas = ctk.CTkCanvas(upper_frame, width=screen_width, height=upper_height, bg="lightblue", highlightthickness=0)
canvas.pack(fill="both", expand=True)

lower_frame = ctk.CTkFrame(root, fg_color="white", height=lower_height)
lower_frame.pack(fill="both", expand=True)

columns = []
for i in range(5):
    col = ctk.CTkFrame(lower_frame, fg_color="white")
    col.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    columns.append(col)

def create_slider_with_label(parent, text, from_, to, steps):
    frame = ctk.CTkFrame(parent, fg_color="white")
    frame.pack(fill="x", pady=(10, 25))

    label = ctk.CTkLabel(frame, text=text, fg_color="white", bg_color="white", font=ctk.CTkFont(size=14, weight="bold"))
    label.pack(anchor="w", pady=(0, 5))

    value_var = ctk.StringVar(value=f"{from_:.1f}")
    value_label = ctk.CTkLabel(frame, textvariable=value_var, width=40, fg_color="white", bg_color="white")
    value_label.pack(side="right", padx=(5, 0))

    slider = ctk.CTkSlider(frame, from_=from_, to=to, number_of_steps=steps)
    slider.set(from_)
    slider.pack(fill="x", expand=True)

    def update_value(val):
        value_var.set(f"{float(val):.1f}")
    slider.configure(command=update_value)
    return slider

težina_var = create_slider_with_label(columns[1], "Težina lopte", 0.1, 10.0, 99)
otpor_var = create_slider_with_label(columns[1], "Otpor vazduha", 0.0, 2.0, 20)
gravitacija_var = create_slider_with_label(columns[2], "Gravitacija", 0.1, 20.0, 199)
brzina_var = create_slider_with_label(columns[2], "Brzina simulacije", 0.1, 3.0, 29)

ctk.CTkLabel(columns[3], text="Vrsta podloge", fg_color="white", bg_color="white", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(0, 5))
podloga_var = ctk.CTkOptionMenu(columns[3], values=["Normalna", "Trambolina", "Pesak", "Led"], fg_color="#6c9ceb", button_color="#0762f5", text_color="black")
podloga_var.pack(fill="x", pady=(0, 30))

pokreni_simulaciju_btn = ctk.CTkButton(columns[3], text="Pokreni simulaciju", fg_color="#5bde62", text_color="black", corner_radius=10, height=30, font=ctk.CTkFont(size=14, weight="bold"))
pokreni_simulaciju_btn.pack(fill="x", pady=10)

restart_simulacije_btn = ctk.CTkButton(columns[3], text="Restart", fg_color="#e4ed51", text_color="black", corner_radius=10, height=30, font=ctk.CTkFont(size=14, weight="bold"))
restart_simulacije_btn.pack(fill="x", pady=10)

pauza_simulacije_btn = ctk.CTkButton(columns[3], text="Pauza", fg_color="#6c9ceb", text_color="black", corner_radius=10, height=30, font=ctk.CTkFont(size=14, weight="bold"))
pauza_simulacije_btn.pack(fill="x", pady=10)

ŠIRINA = screen_width
VISINA = upper_height
ODBIJANJE = 0.7
R = 0.1

simulacija_aktivna = False
pauzirano = False

# Diskretan label za prikaz tipa lopte
tip_lopte_label = ctk.CTkLabel(upper_frame, text="", font=ctk.CTkFont(size=16), text_color="lightblue", bg_color="lightblue")
tip_lopte_label.place(x=20, y=20)

def karakteristike_lopte(masa):
    if masa < 0.5:
        return "Ping pong", "white", 0.9
    elif masa < 2:
        return "Teniska", "green", 0.8
    elif masa < 4:
        return "Odbojkaška", "white", 0.7
    elif masa < 7:
        return "Fudbalska", "black", 0.65
    else:
        return "Košarkaška", "orange", 0.6

def pokreni_simulaciju():
    global simulacija_aktivna, pauzirano
    if simulacija_aktivna:
        return
    canvas.delete("all")
    simulacija_aktivna = True
    pauzirano = False
    run_simulacija()

def restart_simulacije():
    global simulacija_aktivna, pauzirano
    simulacija_aktivna = False
    pauzirano = False
    canvas.delete("all")
    tip_lopte_label.configure(text="")

def pauza_simulacije():
    global pauzirano
    if simulacija_aktivna:
        pauzirano = not pauzirano
        if pauzirano:
            pauza_simulacije_btn.configure(text="Nastavi")
        else:
            pauza_simulacije_btn.configure(text="Pauza")

def run_simulacija():
    canvas.delete("all")

    x = 50
    y = VISINA - 50
    brzina_x = 100
    brzina_y = -200

    masa = težina_var.get()
    otpor = otpor_var.get()
    gravitacija = gravitacija_var.get()
    brzina_simulacije = brzina_var.get()

    tip_lopte, boja_lopte, odbijanje_lopte = karakteristike_lopte(masa)
    tip_lopte_label.configure(text=f"Lopta: {tip_lopte}")

    vrsta_podloge = podloga_var.get()
    if vrsta_podloge == "Normalna":
        odbijanje_podloge = 1.0
    elif vrsta_podloge == "Trambolina":
        odbijanje_podloge = 1.4
    elif vrsta_podloge == "Pesak":
        odbijanje_podloge = 0.5
    elif vrsta_podloge == "Led":
        odbijanje_podloge = 1.2
    else:
        odbijanje_podloge = 1.0

    odbijanje = odbijanje_lopte * odbijanje_podloge

    dt_osnovni = 0.02
    dt = dt_osnovni * brzina_simulacije
    r = masa * 3 + 10

    vreme_poslednjeg = time.time()

    trag = []
    prvi_udarac = True

    def simulacija_petlja():
        nonlocal x, y, brzina_x, brzina_y, vreme_poslednjeg, prvi_udarac
        if not simulacija_aktivna:
            return

        if pauzirano:
            root.after(10, simulacija_petlja)
            return

        sada = time.time()
        proteklo = sada - vreme_poslednjeg
        if proteklo < dt_osnovni:
            root.after(10, simulacija_petlja)
            return
        vreme_poslednjeg = sada

        brzina_simulacije = brzina_var.get()
        dt = dt_osnovni * brzina_simulacije

        ax = -otpor * brzina_x / masa
        ay = gravitacija - otpor * brzina_y / masa

        if y + r > VISINA:
            y = VISINA - r
            if prvi_udarac:
                brzina_y = -brzina_y * 0.7
                prvi_udarac = False
            else:
                brzina_y = -brzina_y * odbijanje

            if abs(brzina_y) < 10:
                return

        brzina_x += ax * dt
        brzina_y += ay * dt

        x += brzina_x * dt
        y += brzina_y * dt

        trag.append((x, y))

        canvas.delete("lopta")
        for i in range(1, len(trag)):
            x1, y1 = trag[i-1]
            x2, y2 = trag[i]
            canvas.create_line(x1, y1, x2, y2, fill="blue", tags="lopta", width=1)
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=boja_lopte, tags="lopta")

        root.after(10, simulacija_petlja)

    simulacija_petlja()

pokreni_simulaciju_btn.configure(command=pokreni_simulaciju)
restart_simulacije_btn.configure(command=restart_simulacije)
pauza_simulacije_btn.configure(command=pauza_simulacije)

root.mainloop()
