import tkinter as tk
from tkinter import messagebox
import random

# Cartes simplifiées (valeurs uniquement)
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

def deal_card():
return random.choice(deck)

class BlackjackGame:
def __init__(self, root):
self.root = root
self.root.title("Blackjack - Tkinter")

self.balance = 100
self.player_cards = []
self.dealer_cards = []

self.setup_ui()

def setup_ui(self):
# Argent
self.balance_label = tk.Label(self.root, text=f"Balance: ${self.balance}", font=('Arial', 14))
self.balance_label.pack(pady=5)

# Zone du croupier
self.dealer_frame = tk.LabelFrame(self.root, text="BANQUIER", padx=10, pady=10)
self.dealer_frame.pack(pady=10)
self.dealer_cards_label = tk.Label(self.dealer_frame, text="")
self.dealer_cards_label.pack()

# Zone du joueur
self.player_frame = tk.LabelFrame(self.root, text="Joueur", padx=10, pady=10)
self.player_frame.pack(pady=10)
self.player_cards_label = tk.Label(self.player_frame, text="")
self.player_cards_label.pack()

# Boutons
self.controls_frame = tk.Frame(self.root)
self.controls_frame.pack(pady=10)
tk.Button(self.controls_frame, text="Hit", command=self.hit).pack(side='left', padx=5)
tk.Button(self.controls_frame, text="Stand", command=self.stand).pack(side='left', padx=5)
tk.Button(self.controls_frame, text="Restart", command=self.restart_game).pack(side='left', padx=5)

self.restart_game()

def restart_game(self):
self.player_cards = [deal_card(), deal_card()]
self.dealer_cards = [deal_card(), deal_card()]
self.update_ui()

def update_ui(self):
self.player_cards_label.config(text=f"Vos cartes: {self.player_cards} = {sum(self.player_cards)}")
self.dealer_cards_label.config(text=f"Croupier: {self.dealer_cards[0]} + ?")

def hit(self):
self.player_cards.append(deal_card())
total = sum(self.player_cards)
self.player_cards_label.config(text=f"Vos cartes: {self.player_cards} = {total}")
if total > 21:
messagebox.showinfo("Perdu", "Vous avez dépassé 21 !")
self.balance -= 10
self.balance_label.config(text=f"Balance: ${self.balance}")
self.restart_game()

def stand(self):
dealer_total = sum(self.dealer_cards)
while dealer_total < 17:
self.dealer_cards.append(deal_card())
dealer_total = sum(self.dealer_cards)

player_total = sum(self.player_cards)
result = ""
if dealer_total > 21 or player_total > dealer_total:
result = "Gagné"
self.balance += 10
elif player_total == dealer_total:
result = "Égalité"
else:
result = "Perdu"
self.balance -= 10

messagebox.showinfo(result, f"Dealer: {self.dealer_cards} ({dealer_total})\nVous: {self.player_cards} ({player_total})")
self.balance_label.config(text=f"Balance: ${self.balance}")
self.restart_game()

# Lancer l'app
root = tk.Tk()
game = BlackjackGame(root)
root.mainloop()