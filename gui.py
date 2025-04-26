import customtkinter as ctk 

# Tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Glavni prozor
root = ctk.CTk()
root.title("Simulacija")

# Dohvati veličinu ekrana
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Postavi veličinu prozora na celu veličinu ekrana
root.geometry(f"{screen_width}x{screen_height}")

upper_height = int(screen_height * 3 / 5)
lower_height = screen_height - upper_height  # ostatak

# 3/5 visine
upper_frame = ctk.CTkFrame(root, fg_color="lightblue", height=upper_height)
upper_frame.pack(fill="x")

# 2/5 visine
lower_frame = ctk.CTkFrame(root, fg_color="white", height=lower_height)
lower_frame.pack(fill="both", expand=True)

# donji deo i 5 kolona
columns = []
for i in range(5):
    col = ctk.CTkFrame(lower_frame, fg_color="white")
    col.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    columns.append(col)

# Funkcija za skalu
def create_slider_with_label(parent, text, from_, to, steps):
    frame = ctk.CTkFrame(parent, fg_color="white")
    frame.pack(fill="x", pady=(10, 25))

    label = ctk.CTkLabel(
        frame,
        text=text,
        fg_color="white",
        bg_color="white",
        font=ctk.CTkFont(size=14, weight="bold")  
    )
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

# kolona 1 
težina_var = create_slider_with_label(columns[1], "Težina lopte", 0.1, 10.0, 99)
otpor_var = create_slider_with_label(columns[1], "Otpor vazduha", 0.0, 2.0, 20)

# kolona 2 
gravitacija_var = create_slider_with_label(columns[2], "Gravitacija", 0.1, 20.0, 199)
brzina_var = create_slider_with_label(columns[2], "Brzina simulacije", 0.1, 3.0, 29)

# kolona 3 
podloga_var = ctk.CTkLabel(
    columns[3],
    text="Vrsta podloge",
    fg_color="white",
    bg_color="white",
    font=ctk.CTkFont(size=14, weight="bold")  
).pack(pady=(0, 5))


# Svetliji izgled za dropdown dok se ne klikne
surface_option = ctk.CTkOptionMenu(
    columns[3],
    values=["Normalna", "Trambolina", "Pesak", "Led"],
    fg_color="#6c9ceb",       
    button_color="#0762f5",   
    text_color="black"
)
surface_option.pack(fill="x", pady=(0, 30))

pokreni_simulaciju = ctk.CTkButton(
    columns[3],
    text="Pokreni simulaciju",
    fg_color="#5bde62",
    text_color="black",
    corner_radius=10,
    height=50,
    font=ctk.CTkFont(size=14, weight="bold")
)
pokreni_simulaciju.pack(fill="x", pady=10)

restart_simulacije = ctk.CTkButton(
    columns[3],
    text="Restart",
    fg_color="#e4ed51",
    text_color="black",
    corner_radius=10,
    height=50, 
    font=ctk.CTkFont(size=14, weight="bold")
)
restart_simulacije.pack(fill="x", pady=10)

root.mainloop()

