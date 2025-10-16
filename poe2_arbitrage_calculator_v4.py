import tkinter as tk
from tkinter import ttk, messagebox
import json, os

SAVE_FILE = "poe2_data.json"
item_inputs = []
item_counter = 0

ITEM_CATEGORIES = {
    "Currency": [
        "Mirror of Kalandra", "Hinekora's Lock", "Perfect Chaos Orb", "Perfect Exalted Orb",
        "Divine Orb", "Orb of Annulment", "Fracturing Orb", "Greater Chaos Orb",
        "Chaos Orb", "Perfect Regal Orb", "Perfect Jeweller's Orb", "Orb of Chance",
        "Greater Exalted Orb", "Perfect Orb of Augmentation", "Artificer's Shard",
        "Exalted Orb", "Transmutation Shard", "Arcanist's Etcher", "Glassblower's Bauble",
        "Perfect Orb of Transmutation", "Gemcutter's Prism", "Vaal Orb", "Greater Regal Orb",
        "Artificer's Orb", "Greater Jeweller's Orb"
    ],
    "Splinters": [
        "Breach Splinters", "Ritual Splinters", "Simulacrum Splinters", "Expedition Splinters"
    ],
    "Ritual Omens": [
        "Omen of Sinistral Annulment", "Omen of Chance", "Omen of Sinistral Erasure",
        "Omen of Dextral Annulment", "Omen of Light", "Omen of Whittling",
        "Omen of Dextral Erasure", "Omen of Sanctification", "Omen of Sinistral Crystallisation",
        "Omen of Homogenising Exaltation", "Omen of Reinforcements", "Omen of Abyssal Echoes",
        "Omen of Dextral Crystallisation", "Omen of Secret Compartments", "Omen of Recombination",
        "Omen of the Blessed", "Omen of Sinistral Necromancy", "Omen of Chaotic Rarity",
        "Omen of Answered Prayers", "Omen of Corruption", "Omen of the Hunt",
        "Omen of Chaotic Quantity", "Omen of Bartering", "Omen of Catalysing Exaltation",
        "Omen of Amelioration"
    ]
}

def add_item(saved_data=None):
    global item_counter
    item_counter += 1

    frame = tk.LabelFrame(items_container, text="Divine Orb", padx=10, pady=5)
    frame.pack(fill="x", padx=5, pady=5)

    tk.Label(frame, text="Category:").grid(row=0, column=0, sticky="w")
    category = ttk.Combobox(frame, width=35, state="readonly")
    category['values'] = list(ITEM_CATEGORIES.keys())
    category.current(0)
    category.grid(row=0, column=1, pady=2)

    tk.Label(frame, text="Item Type:").grid(row=1, column=0, sticky="w")
    item_type = ttk.Combobox(frame, width=35, state="readonly")
    item_type['values'] = ITEM_CATEGORIES["Currency"]
    item_type.current(4)
    item_type.grid(row=1, column=1, pady=2)

    def update_item_options(event):
        selected_category = category.get()
        item_type['values'] = ITEM_CATEGORIES[selected_category]
        item_type.current(0)
        frame.config(text=item_type.get())

    def update_frame_title(event):
        frame.config(text=item_type.get())

    category.bind("<<ComboboxSelected>>", update_item_options)
    item_type.bind("<<ComboboxSelected>>", update_frame_title)

    tk.Label(frame, text="Items per chaos orb:").grid(row=2, column=0, sticky="w")
    items_per_chaos = tk.Entry(frame, width=20)
    items_per_chaos.grid(row=2, column=1, pady=2)

    tk.Label(frame, text="Current ratio (1 Divine = ? of this item):").grid(row=3, column=0, sticky="w")
    current_ratio = tk.Entry(frame, width=20)
    current_ratio.grid(row=3, column=1, pady=2)

    remove_btn = tk.Button(frame, text="Remove", command=lambda: remove_item(frame, item_data))
    remove_btn.grid(row=4, column=0, columnspan=2, pady=5)

    item_data = {
        "frame": frame,
        "category": category,
        "item_type": item_type,
        "items_per_chaos": items_per_chaos,
        "current_ratio": current_ratio
    }
    item_inputs.append(item_data)

    # Restore saved data if available
    if saved_data:
        category.set(saved_data.get("category", "Currency"))
        update_item_options(None)
        item_type.set(saved_data.get("item_type", "Divine Orb"))
        items_per_chaos.insert(0, saved_data.get("items_per_chaos", ""))
        current_ratio.insert(0, saved_data.get("current_ratio", ""))
        frame.config(text=item_type.get())

def remove_item(frame, item_data):
    frame.destroy()
    item_inputs.remove(item_data)

def calculate():
    try:
        if not item_inputs:
            messagebox.showwarning("No Items", "Please add at least one item.")
            return

        ratio_chaos_per_divine = float(entry_ratio.get())
        divines_invested = float(entry_invested.get())
        base_chaos_value = divines_invested * ratio_chaos_per_divine

        results = []
        for item_data in item_inputs:
            item_name = item_data["item_type"].get()
            items_per_chaos = float(item_data["items_per_chaos"].get())
            current_ratio = float(item_data["current_ratio"].get())
            buy_value = base_chaos_value * items_per_chaos
            sell_value = buy_value / current_ratio
            profit_ratio = sell_value / (base_chaos_value / ratio_chaos_per_divine)
            results.append((item_name, buy_value, sell_value, profit_ratio))

        result_text.delete("1.0", tk.END)
        total_profit = sum(r[3] for r in results)
        result_text.insert(tk.END, f"Total Profit Ratio: {total_profit*10:.3f}\n")
        result_text.insert(tk.END, f"{'='*40}\n\n")
        for name, buy, sell, profit in results:
            result_text.insert(tk.END,
                f"{name}:\n"
                f"  Buy Value (items): {buy:.2f}\n"
                f"  Sell Value (divines): {sell:.2f}\n"
                f"  Profit Ratio: {profit*10:.3f}\n"
                f"{'-'*40}\n"
            )
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def save_data():
    data = {
        "entry_ratio": entry_ratio.get(),
        "entry_invested": entry_invested.get(),
        "items": [],
        "results": result_text.get("1.0", tk.END)
    }
    for item_data in item_inputs:
        data["items"].append({
            "category": item_data["category"].get(),
            "item_type": item_data["item_type"].get(),
            "items_per_chaos": item_data["items_per_chaos"].get(),
            "current_ratio": item_data["current_ratio"].get()
        })
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        entry_ratio.insert(0, data.get("entry_ratio", ""))
        entry_invested.insert(0, data.get("entry_invested", ""))
        for item_info in data.get("items", []):
            add_item(saved_data=item_info)
        result_text.insert("1.0", data.get("results", ""))
    else:
        add_item()  # Add a default item

def on_close():
    save_data()
    root.destroy()

# --- UI SETUP ---
root = tk.Tk()
root.title("POE2 Arbitrage Calculator")
root.geometry("1080x720")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_close)

global_frame = tk.Frame(root, padx=10, pady=10)
global_frame.pack(fill="x")

tk.Label(global_frame, text="1 Divine = x amount of chaos").pack(pady=2)
entry_ratio = tk.Entry(global_frame)
entry_ratio.pack()
tk.Label(global_frame, text="Total Divine Orbs Invested:").pack(pady=2)
entry_invested = tk.Entry(global_frame)
entry_invested.pack()

ttk.Separator(root, orient="horizontal").pack(fill="x", pady=5)

items_label_frame = tk.Frame(root)
items_label_frame.pack(fill="x", padx=10)
tk.Label(items_label_frame, text="Items", font=("Arial", 10, "bold")).pack(side="left")
add_btn = tk.Button(items_label_frame, text="+ Add Item", command=add_item, bg="#4CAF50", fg="white")
add_btn.pack(side="left", padx=5)

canvas = tk.Canvas(root, height=250)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
items_container = tk.Frame(canvas)
items_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=items_container, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
scrollbar.pack(side="right", fill="y", padx=(0, 10))

tk.Button(root, text="Calculate", command=calculate, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
result_text = tk.Text(root, height=12, width=60)
result_text.pack(padx=10, pady=5)

# Load data on startup
load_data()
root.mainloop()
