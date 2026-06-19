import tkinter as tk
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from datetime import datetime

# ==========================================
# 1. CORE CHATBOT LOGIC & DATA STORAGE
# ==========================================
rule_counts = {
    "Greetings": 0,
    "Status Query": 0,
    "Positive Vibes": 0,
    "Identity": 0,
    "Jokes": 0,
    "Time Stuff": 0,
    "Weather": 0,
    "Farewell": 0,
    "Small Talk": 0
}

def process_message(user_input):
    user_input = user_input.lower().strip()
    
    # GREETINGS
    if user_input in ["hello", "hi", "hey", "sup", "yo", "hey there"]:
        return random.choice([
            "Hey! What's up?",
            "Oh hi! Good to hear from you.",
            "Hey there."
        ]), "Greetings"
        
    # STATUS QUERY
    elif user_input in ["how are you", "how's it going", "how do you do", "you good", "how you doing"]:
        return random.choice([
            "I'm good, thanks! How are you holding up?",
            "Pretty good. Just chilling in the code. You?",
            "Not too bad! What's news with you?"
        ]), "Status Query"
        
    # POSITIVE VIBES / AGREEMENT
    elif user_input in ["good", "fine", "i am good", "great", "awesome", "doing well", "cool"]:
        return random.choice([
            "Awesome, love to hear that.",
            "Nice! Glad things are good.",
            "Sweet."
        ]), "Positive Vibes"
        
    # IDENTITY
    elif any(x in user_input for x in ["who are you", "what is your name", "your name", "what are you"]):
        return random.choice([
            "I'm ChatBot. Just a basic chat setup.",
            "Names ChatBot. I talk and track our topics on that graph over there."
        ]), "Identity"
        
    # JOKES
    elif any(x in user_input for x in ["joke", "funny", "laugh"]):
        return random.choice([
            "Why do programmers wear glasses? Because they can't C#!",
            "Why did the programmer quit his job? Because he didn't get arrays.",
            "There are 10 types of people: those who get binary, and those who don't."
        ]), "Jokes"
        
    # TIME & DATE STUFF
    elif any(x in user_input for x in ["time", "date", "day is it", "clock", "today"]):
        now = datetime.now()
        if "date" in user_input or "day" in user_input or "today" in user_input:
            return f"Today is {now.strftime('%A, %B %d, %Y')}.", "Time Stuff"
        else:
            return f"It's {now.strftime('%I:%M %p')} right now.", "Time Stuff"
        
    # WEATHER
    elif "weather" in user_input:
        return random.choice([
            "No clue, I don't have windows. Hope it's nice out though!",
            "It's always room temperature inside a server container.",
            "Hopefully it's good enough to go outside."
        ]), "Weather"
        
    # FAREWELL
    elif user_input in ["bye", "goodbye", "exit", "quit", "see ya", "later"]:
        return random.choice([
            "Catch you later!",
            "Bye! Take care.",
            "See ya."
        ]), "Farewell"
        
    # SMALL TALK / FALLBACK
    else:
        return random.choice([
            "Huh, interesting. Tell me more?",
            "Yeah? What else is on your mind?",
            "Fair enough. What's next?",
            "Gotcha. Makes sense."
        ]), "Small Talk"

# ==========================================
# 2. UI AND VISUALIZATION MANAGEMENT
# ==========================================
def send_message():
    user_text = user_entry.get().strip()
    if not user_text:
        return
        
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_text}\n")
    
    reply, category = process_message(user_text)
    
    chat_history.insert(tk.END, f"Bot: {reply}\n\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.yview(tk.END)
    
    user_entry.delete(0, tk.END)
    
    rule_counts[category] += 1
    update_chart()

def update_chart():
    ax.clear()
    
    fig.patch.set_facecolor('#1e1e24')
    ax.set_facecolor('#1e1e24')
    
    categories = list(rule_counts.keys())
    counts = list(rule_counts.values())
    
    # Refreshed the color palette here to complement the new theme
    colors = ['#00F5D4', '#00BBF9', '#9B5DE5', '#F15BB5', '#FFD97D', '#FF9966', '#FF5E62', '#60EFFE', '#00FF87']
    
    bars = ax.bar(categories, counts, color=colors[:len(categories)], edgecolor='none', width=0.6)
    
    ax.set_title("What We're Talking About", fontsize=12, fontweight='bold', pad=15, color='#ffffff')
    ax.set_ylabel("Messages Sent", fontsize=10, color='#a0a0aa')
    
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, rotation=35, ha='right', fontsize=8, color='#c0c0c8')
    
    ax.tick_params(colors='#a0a0aa')
    ax.spines['bottom'].set_color('#3a3a44')
    ax.spines['left'].set_color('#3a3a44')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.set_ylim(0, max(counts) + 3 if max(counts) > 0 else 5)
    
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 4),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='#ffffff')
    
    plt.tight_layout()
    canvas.draw()

# ==========================================
# 3. TKINTER WINDOW CONFIGURATION
# ==========================================
root = tk.Tk()
root.title("Chat & Stats")
root.geometry("1100x600")
root.configure(bg="#121214")

main_frame = tk.Frame(root, bg="#121214")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

left_panel = tk.Frame(main_frame, bg="#1e1e24", bd=0)
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

right_panel = tk.Frame(main_frame, bg="#1e1e24", bd=0)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))

# Changed header text color to match the theme accent
header_label = tk.Label(left_panel, text="Chat Room", font=("Segoe UI", 14, "bold"), bg="#1e1e24", fg="#00f5d4", anchor="w", padx=15, pady=10)
header_label.pack(fill=tk.X)

divider = tk.Frame(left_panel, height=1, bg="#2d2d38")
divider.pack(fill=tk.X, padx=15)

chat_history = scrolledtext.ScrolledText(left_panel, wrap=tk.WORD, font=("Segoe UI", 11), bg="#1e1e24", fg="#e2e2e8", bd=0, insertbackground="white")
chat_history.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
chat_history.insert(tk.END, "Bot: Hey! What's up?\n\n")
chat_history.config(state=tk.DISABLED)

input_frame = tk.Frame(left_panel, bg="#1e1e24")
input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

user_entry = tk.Entry(input_frame, font=("Segoe UI", 11), bg="#2d2d38", fg="#ffffff", bd=0, insertbackground="white")
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
user_entry.bind("<Return>", lambda event: send_message())
user_entry.focus_set()

# Changed button color to hex #00f5d4 (Teal/Cyan) and active background to #33f7dc
send_button = tk.Button(input_frame, text="Send", font=("Segoe UI", 10, "bold"), bg="#00f5d4", fg="#121214", bd=0, command=send_message, cursor="hand2", padx=20, activebackground="#33f7dc", activeforeground="#121214")
send_button.pack(side=tk.RIGHT, ipady=4)

fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=right_panel)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

update_chart()
root.mainloop()