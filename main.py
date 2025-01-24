
import customtkinter as ctk
from PIL import Image, ImageTk
import os


definitions = [
    {"definition": "Statystyka testowa dla dużej próby", "image_path": "testy_duza.jpg"},
    {"definition": "Statystyka testowa dla małej próby", "image_path": "testy_mala.jpg"},
    {"definition": "ok", "image_path": "me.jpg"}
]

class FlashcardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fiszki STATYSTYKA egzamin")
        self.geometry("500x500")

        self.current_card = 0
        self.image_label = None
        self.incorrect_cards = []  
        self.cards_to_show = definitions  

        self.definition_label = ctk.CTkLabel(self, text=self.cards_to_show[self.current_card]["definition"], 
                                             font=("Old English Text MT", 30), 
                                             wraplength=480)
        self.definition_label.pack(pady=10)

        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(side="bottom", pady=20, padx=20, fill="x")

        self.reveal_button = ctk.CTkButton(bottom_frame, text="ODKRYJ", 
                                           command=self.reveal_image, 
                                           corner_radius=50,
                                           fg_color="#502eb9",
                                           hover_color="#8b17c1"
                                           )
        self.reveal_button.pack(side="left", padx=10)

        self.know_button = ctk.CTkButton(bottom_frame, 
                                         text="ZNAM", 
                                         command=self.mark_as_known, 
                                         state="disabled", 
                                         corner_radius=50,
                                         fg_color="#502eb9",
                                         hover_color="#8b17c1")
        self.know_button.pack(side="left", padx=10)

        self.dont_know_button = ctk.CTkButton(bottom_frame, 
                                              text="NIE ZNAM", 
                                              command=self.mark_as_unknown, 
                                              state="disabled", 
                                              corner_radius=50,
                                              fg_color="#502eb9",
                                              hover_color="#8b17c1")
        self.dont_know_button.pack(side="left", padx=10)

        self.reset_button = None

    def reveal_image(self):
        if self.current_card >= len(self.cards_to_show):
            self.show_results()
            return
        
        self.definition_label.pack_forget()
        image_path = self.cards_to_show[self.current_card]["image_path"]

        try:
            image = Image.open(image_path)
            image = image.resize((600, 600))  
            photo = ImageTk.PhotoImage(image)
        except Exception:
            self.definition_label.configure(text="cos sie popsulo z obrazem")
            self.definition_label.pack(pady=20)
            return

        if self.image_label:
            self.image_label.destroy()

        self.image_label = ctk.CTkLabel(self, image=photo, text="")
        self.image_label.image = photo
        self.image_label.pack(pady=20)

        self.know_button.configure(state="normal")
        self.dont_know_button.configure(state="normal")
        self.reveal_button.configure(state="disabled")

    def mark_as_known(self):
        self.next_card()

    def mark_as_unknown(self):
        self.incorrect_cards.append(self.cards_to_show[self.current_card]["definition"])
        self.next_card()

    def next_card(self):
        self.current_card += 1
        
        if self.image_label:
            self.image_label.destroy()

        if self.current_card < len(self.cards_to_show):
            self.definition_label.configure(text=self.cards_to_show[self.current_card]["definition"])
            self.definition_label.pack(pady=20)
            self.reveal_button.configure(state="normal")
            self.know_button.configure(state="disabled")
            self.dont_know_button.configure(state="disabled")
        else:
            self.show_results()

    def show_results(self):
        if self.image_label:
            self.image_label.destroy()
        
        if self.incorrect_cards:
            result_text = "NIEZNANE FISZKI:\n\n" + "\n\n".join(self.incorrect_cards)
        else:
            result_text = "Wszystkie fiszki zapamiętane bez błędu:D"

        self.definition_label.configure(text=result_text)
        self.definition_label.pack(pady=20)
        self.reveal_button.configure(state="disabled")
        self.know_button.configure(state="disabled")
        self.dont_know_button.configure(state="disabled")

        self.reset_button = ctk.CTkButton(self, 
                                          text="RESET", 
                                          command=self.reset_app, 
                                          corner_radius=50,
                                          fg_color="#502eb9",
                                          hover_color="#8b17c1")
        self.reset_button.pack(pady=20)

    def reset_app(self):
        self.current_card = 0
        self.incorrect_cards = []
        self.cards_to_show = definitions
        
        if self.reset_button:
            self.reset_button.destroy()
        
        self.definition_label.configure(text=self.cards_to_show[self.current_card]["definition"])
        self.definition_label.pack(pady=20)

        self.reveal_button.configure(state="normal")
        self.know_button.configure(state="disabled")
        self.dont_know_button.configure(state="disabled")

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()