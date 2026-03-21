import fitz
import re

balance_pdf = fitz.open('media/players/AKPC S22 AFTER TRANSFER WINDOW BALANCE LIST.pdf')
balance_text = ""
for page in balance_pdf:
    balance_text += page.get_text() + "\n"

print("--- 10 HEAD LINES OF BALANCE ---")
lines = balance_text.split('\n')
for i, line in enumerate(lines[:30]):
    print(f"{i}: {line}")

player_pdf = fitz.open('media/players/AKPC S22 AFTER TRANSFER WINDOW PLAYERS LIST.pdf')
player_text = ""
for page in player_pdf:
    player_text += page.get_text() + "\n"

print("\n--- 20 HEAD LINES OF PLAYERS ---")
plines = player_text.split('\n')
for i, line in enumerate(plines[10:50]):
    print(f"{i}: {line}")
