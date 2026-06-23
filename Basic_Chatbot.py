import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import random

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ====================================================
# CHATBOT DATA
# ====================================================

rule_counts = {
    "Greetings": 0,
    "Status": 0,
    "Identity": 0,
    "Jokes": 0,
    "Time": 0,
    "Weather": 0,
    "Positive": 0,
    "Farewell": 0,
    "Other": 0
}

total_messages = 0

# ====================================================
# CHATBOT LOGIC
# ====================================================

def process_message(user_input):

    text = user_input.lower().strip()

    greetings = ["hi", "hello", "hey", "yo", "sup"]
    status = ["how are you", "how's it going", "how do you do"]
    positive = ["good", "great", "awesome", "fine"]
    farewell = ["bye", "goodbye", "see ya", "later"]

    if text in greetings:
        return random.choice([
            "Hey! What's up?",
            "Hello there!",
            "Good to see you."
        ]), "Greetings"

    elif any(x in text for x in status):
        return random.choice([
            "Doing great. How about you?",
            "Pretty good today.",
            "I'm running smoothly."
        ]), "Status"

    elif any(x in text for x in ["who are you", "your name"]):
        return "I'm your Python ChatBot Assistant.", "Identity"

    elif any(x in text for x in ["joke", "funny"]):
        return random.choice([
            "Why do programmers hate nature? Too many bugs.",
            "Why was the computer cold? It left its Windows open.",
            "There are 10 types of people: those who understand binary and those who don't."
        ]), "Jokes"

    elif "weather" in text:
        return "I don't have live weather access, but I hope it's sunny!", "Weather"

    elif any(x in text for x in ["time", "clock"]):
        return datetime.now().strftime("Current Time: %I:%M:%S %p"), "Time"

    elif any(x in text for x in ["date", "today"]):
        return datetime.now().strftime("Today is %A, %d %B %Y"), "Time"

    elif text in positive:
        return "Nice! Glad to hear that.", "Positive"

    elif text in farewell:
        return "Goodbye. Have a great day!", "Farewell"

    else:
        return random.choice([
            "Interesting. Tell me more.",
            "I see.",
            "That's cool.",
            "Can you explain further?"
        ]), "Other"


# ====================================================
# SEND MESSAGE
# ====================================================

def send_message():

    global total_messages

    user_text = user_entry.get().strip()

    if not user_text:
        return

    if user_text == PLACEHOLDER:
        return

    current_time = datetime.now().strftime("%H:%M")

    chat_history.config(state=tk.NORMAL)

    chat_history.insert(
        tk.END,
        f"\n🧑 You [{current_time}]\n{user_text}\n",
        "user"
    )

    reply, category = process_message(user_text)

    chat_history.insert(
        tk.END,
        f"🤖 Bot [{current_time}]\n{reply}\n",
        "bot"
    )

    chat_history.config(state=tk.DISABLED)
    chat_history.yview(tk.END)

    user_entry.delete(0, tk.END)

    rule_counts[category] += 1
    total_messages += 1

    counter_label.config(
        text=f"Messages Sent: {total_messages}"
    )

    update_chart()


# ====================================================
# PLACEHOLDER
# ====================================================

PLACEHOLDER = "Type your message here..."

def clear_placeholder(event):
    if user_entry.get() == PLACEHOLDER:
        user_entry.delete(0, tk.END)

def restore_placeholder(event):
    if not user_entry.get():
        user_entry.insert(0, PLACEHOLDER)


# ====================================================
# GRAPH
# ====================================================

def update_chart():

    ax.clear()

    fig.patch.set_facecolor("#1e1e24")
    ax.set_facecolor("#1e1e24")

    categories = list(rule_counts.keys())
    values = list(rule_counts.values())

    colors = [
        "#00F5D4",
        "#00BBF9",
        "#9B5DE5",
        "#F15BB5",
        "#FFD166",
        "#FF6B6B",
        "#06D6A0",
        "#4D96FF",
        "#F72585"
    ]

    bars = ax.barh(categories, values, color=colors)

    ax.set_title(
        "Conversation Analytics",
        color="white",
        fontsize=14,
        fontweight="bold"
    )

    ax.tick_params(colors="white")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#444")
    ax.spines["bottom"].set_color("#444")

    for bar in bars:
        width = bar.get_width()

        if width > 0:
            ax.text(
                width + 0.1,
                bar.get_y() + bar.get_height()/2,
                str(int(width)),
                va="center",
                color="white"
            )

    canvas.draw()


# ====================================================
# WINDOW
# ====================================================

root = tk.Tk()

root.title("AI Chat Dashboard")
root.geometry("1300x700")
root.configure(bg="#121214")

# ====================================================
# MAIN FRAME
# ====================================================

main_frame = tk.Frame(root, bg="#121214")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ====================================================
# LEFT PANEL
# ====================================================

left_panel = tk.Frame(
    main_frame,
    bg="#1e1e24"
)

left_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 15)
)

# ====================================================
# RIGHT PANEL
# ====================================================

right_panel = tk.Frame(
    main_frame,
    bg="#1e1e24",
    width=400
)

right_panel.pack(
    side="right",
    fill="both"
)

# ====================================================
# HEADER
# ====================================================

header = tk.Label(
    left_panel,
    text="💬 Chat Room",
    bg="#1e1e24",
    fg="#00F5D4",
    font=("Segoe UI", 16, "bold")
)

header.pack(anchor="w", padx=15, pady=15)

# ====================================================
# CHAT HISTORY
# ====================================================

chat_history = scrolledtext.ScrolledText(
    left_panel,
    bg="#1e1e24",
    fg="white",
    font=("Segoe UI", 11),
    bd=0,
    wrap=tk.WORD,
    insertbackground="white"
)

chat_history.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

chat_history.tag_config(
    "user",
    foreground="#00F5D4"
)

chat_history.tag_config(
    "bot",
    foreground="#FFFFFF"
)

chat_history.insert(
    tk.END,
    "🤖 Bot [Start]\nHey! What's up?\n\n"
)

chat_history.config(state=tk.DISABLED)

# ====================================================
# INPUT SECTION
# ====================================================

input_container = tk.Frame(
    left_panel,
    bg="#2b2b35",
    highlightbackground="#00F5D4",
    highlightthickness=1
)

input_container.pack(
    fill="x",
    padx=15,
    pady=15
)

user_entry = tk.Entry(
    input_container,
    bg="#2b2b35",
    fg="white",
    font=("Segoe UI", 12),
    relief="flat",
    insertbackground="white"
)

user_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10,
    pady=12
)

user_entry.insert(0, PLACEHOLDER)

user_entry.bind("<FocusIn>", clear_placeholder)
user_entry.bind("<FocusOut>", restore_placeholder)
user_entry.bind("<Return>", lambda e: send_message())

send_button = tk.Button(
    input_container,
    text="➤",
    bg="#00F5D4",
    fg="#121214",
    font=("Segoe UI", 14, "bold"),
    relief="flat",
    cursor="hand2",
    command=send_message
)

send_button.pack(
    side="right",
    padx=10,
    pady=6
)

# ====================================================
# ANALYTICS HEADER
# ====================================================

analytics_label = tk.Label(
    right_panel,
    text="📊 Live Analytics",
    bg="#1e1e24",
    fg="#00F5D4",
    font=("Segoe UI", 16, "bold")
)

analytics_label.pack(pady=15)

counter_label = tk.Label(
    right_panel,
    text="Messages Sent: 0",
    bg="#1e1e24",
    fg="white",
    font=("Segoe UI", 11)
)

counter_label.pack()

# ====================================================
# CHART
# ====================================================

fig, ax = plt.subplots(
    figsize=(5, 5),
    dpi=100
)

canvas = FigureCanvasTkAgg(
    fig,
    master=right_panel
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

update_chart()

# ====================================================
# START
# ====================================================

root.mainloop()
