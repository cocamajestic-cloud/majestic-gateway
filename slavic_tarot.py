import tkinter as tk
import random
from PIL import Image, ImageTk

class TarotDeckSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Slavic Tarot Prototype")
        
        # Define 3:5 Aspect Ratio
        self.card_width = 300
        self.card_height = 500
        
        # Deck Array (Expand this with your full deck)
        self.deck = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor"]
        
        # UI Setup
        self.label = tk.Label(root, text="Click the card to draw", font=("Helvetica", 16))
        self.label.pack(pady=10)
        
        # Card Canvas
        self.canvas = tk.Canvas(root, width=self.card_width, height=self.card_height, bg="grey")
        self.canvas.pack(pady=20)
        
        # Initial State: Card Back
        self.is_flipped = False
        self.draw_card_back()
        
        # Bind Click Event
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_card_back(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(10, 10, self.card_width-10, self.card_height-10, fill="#2c3e50", outline="#ecf0f1", width=5)
        self.canvas.create_text(self.card_width//2, self.card_height//2, text="SLAVIC TAROT", fill="white", angle=45)

    def handle_click(self, event):
        if not self.is_flipped:
            self.reveal_card()
        else:
            self.is_flipped = False
            self.draw_card_back()

    def reveal_card(self):
        # 1. Generate random orientation (1=Upright, 2=Reversed)
        orientation = random.randint(1, 2)
        
        # 2. Select random card
        card_name = random.choice(self.deck)
        
        self.canvas.delete("all")
        
        # Determine Rotation/Visual State
        display_text = card_name
        rotation = 0
        bg_color = "#f39c12" # Upright Gold
        
        if orientation == 2:
            rotation = 180
            display_text = f"{card_name}\n(REVERSED)"
            bg_color = "#8e44ad" # Reversed Purple
            
        # 3. Transition to Front
        self.canvas.create_rectangle(10, 10, self.card_width-10, self.card_height-10, fill=bg_color, outline="black", width=5)
        self.canvas.create_text(self.card_width//2, self.card_height//2, 
                               text=display_text, font=("Helvetica", 20, "bold"), 
                               angle=rotation, justify="center")
        
        self.is_flipped = True

if __name__ == "__main__":
    root = tk.Tk()
    app = TarotDeckSystem(root)
    root.mainloop()