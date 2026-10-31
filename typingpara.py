import tkinter as tk
import time
import random

# ==================== 词库 ====================
PRACTICE_WORDS = """dream cover beach drink happy light music phone table water chair green smile sweet black bread cloud dance earth fruit
glass heart house juice knife lemon money night ocean paper queen river sheep sugar tiger train voice watch young apple
brave catch clean close color early empty event field floor fresh front funny grand human ideal inner joint known large
lucky magic major minor model north offer order paint peace plant proud quick quiet radio ready right round share short
small sound space speak sport stand start stone story study thank think three today touch under visit white world write""".split()

COMPETITION_WORDS = """achieve balance capture declare effects factory general harvest improve journey kitchen library machine natural observe prepare
quality reserve service travel unusual village welcome yellow ability brother culture develop evening forward history include
justice knowing leading medical network outside private quickly respect science teacher uniform various western working ancient
benefit concern discuss economy feature improve library measure nothing operate project quality receive special tonight village
weather account brought central digital element freedom greater husband initial kingdom mention obvious promise request station
student thought usually welcome article between chapter disease evening further history include journey machine natural outside""".split()

# ==================== 全局变量 ====================
is_playing = False
timer_id = None

root = tk.Tk()
root.title("Typing competition")
root.geometry("1100x700")
root.configure(bg="#323437")

main_frame = tk.Frame(root, bg="#323437")
game_frame = tk.Frame(root, bg="#323437")
result_frame = tk.Frame(root, bg="#323437")

hidden_entry = tk.Entry(root, width=0, borderwidth=0, highlightthickness=0)
hidden_entry.place(x=-100, y=-100)

def clear_frames():
    main_frame.pack_forget()
    game_frame.pack_forget()
    result_frame.pack_forget()

# ==================== 界面 1：主菜单 ====================
def show_main_menu():
    global is_playing, timer_id
    is_playing = False
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
    
    clear_frames()
    main_frame.pack(fill="both", expand=True)
    
    for widget in main_frame.winfo_children():
        widget.destroy()
        
    tk.Label(main_frame, text="Typing competition", font=("Arial", 45, "bold"), bg="#323437", fg="#e2b714").pack(pady=(150, 50))
    
    tk.Button(main_frame, text="Practice mode", font=("Arial", 20), width=15, bg="#2c2e31", fg="#d1d0c5", borderwidth=0, command=lambda: start_game("practice")).pack(pady=20)
    tk.Button(main_frame, text="Competition mode", font=("Arial", 20), width=15, bg="#2c2e31", fg="#d1d0c5", borderwidth=0, command=lambda: start_game("competition")).pack(pady=20)

# ==================== 界面 2：游戏界面 ====================
def start_game(mode):
    global is_playing, timer_id
    clear_frames()
    game_frame.pack(fill="both", expand=True)
    
    for widget in game_frame.winfo_children():
        widget.destroy()

    timer_id = None
    is_playing = True

    time_left = 15 if mode == "practice" else 60
    base_words = PRACTICE_WORDS if mode == "practice" else COMPETITION_WORDS
    
    state = {
        "mode": mode,
        "page_index": 0,
        "target_text": "",
        "typed_text": "",
        "start_time": None,
        "base_green_chars": 0,
        "base_typed_chars": 0,
        "base_words_typed": 0,
        "final_green": 0,
        "final_typed": 0,
        "final_words": 0,
        "final_acc": 0.0
    }

    top_frame = tk.Frame(game_frame, bg="#323437")
    top_frame.pack(fill="x", pady=20, padx=40)

    timer_label = tk.Label(top_frame, text=str(time_left), font=("Arial", 28, "bold"), bg="#323437", fg="#e2b714")
    timer_label.pack(side="left")

    stats_label = tk.Label(top_frame, text="Words typed: 0\nAccuracy: 100%", font=("Arial", 16), bg="#323437", fg="#646669", justify="right")
    stats_label.pack(side="right")

    text_display = tk.Text(game_frame, font=("Courier New", 24), wrap="word", bg="#323437", fg="#646669", borderwidth=0, highlightthickness=0, spacing1=10, spacing3=10)
    text_display.pack(pady=40, padx=60, fill="both", expand=True)
    text_display.tag_config("correct", foreground="#d1d0c5")
    text_display.tag_config("wrong", foreground="#ca4754")
    text_display.tag_config("caret", background="#e2b714")
    text_display.config(state="disabled")

    btn_frame = tk.Frame(game_frame, bg="#323437")
    btn_frame.place(relx=0.95, rely=0.95, anchor="se")
    
    next_btn = tk.Button(btn_frame, text="Next page", font=("Arial", 14), bg="#2c2e31", fg="#d1d0c5", borderwidth=0, command=lambda: load_new_page())
    next_btn.pack(side="left", padx=10)
    
    end_btn = tk.Button(btn_frame, text="End now", font=("Arial", 14), bg="#ca4754", fg="white", borderwidth=0, command=lambda: end_game(state))
    end_btn.pack(side="left")

    hidden_entry.focus()

    def calculate_current_page_stats():
        typed = state["typed_text"]
        target = state["target_text"]
        
        page_green = 0
        page_typed = len(typed)
        for i in range(len(typed)):
            if i < len(target) and typed[i].lower() == target[i].lower():
                page_green += 1
                
        page_words = 0
        if len(typed) > 0:
            target_words = target.split(" ")
            current_idx = 0
            for w in target_words:
                if len(typed) >= current_idx + len(w):
                    page_words += 1
                else:
                    break
                current_idx += len(w) + 1

        total_green = state["base_green_chars"] + page_green
        total_typed = state["base_typed_chars"] + page_typed
        total_words = state["base_words_typed"] + page_words

        acc = (total_green / total_typed * 100) if total_typed > 0 else 100
        
        stats_label.config(text=f"Words typed: {total_words}\nAccuracy: {acc:.0f}%")
        
        state["final_green"] = total_green
        state["final_typed"] = total_typed
        state["final_words"] = total_words
        state["final_acc"] = (total_green / total_typed) if total_typed > 0 else 0

    def update_display():
        text_display.config(state="normal")
        text_display.delete("1.0", "end")
        
        target = state["target_text"]
        typed = state["typed_text"]
        cursor_pos = len(typed)

        for i, char in enumerate(target):
            if i < len(typed):
                if typed[i].lower() == char.lower():
                    text_display.insert("end", char, "correct")
                else:
                    text_display.insert("end", typed[i], "wrong")
            elif i == cursor_pos:
                text_display.insert("end", char, "caret")
            else:
                text_display.insert("end", char)
                
        text_display.config(state="disabled")

    def load_new_page():
        if state["page_index"] > 0:
            state["base_green_chars"] = state["final_green"]
            state["base_typed_chars"] = state["final_typed"]
            state["base_words_typed"] = state["final_words"]
        else:
            state["base_green_chars"] = 0
            state["base_typed_chars"] = 0
            state["base_words_typed"] = 0

        state["page_index"] += 1
        state["typed_text"] = ""
        
        words = base_words[:50] if state["page_index"] % 2 == 1 else base_words[50:]
        random.shuffle(words)
        state["target_text"] = " ".join(words)
        
        update_display()
        calculate_current_page_stats()

    def on_key_press(event):
        if not is_playing: return

        if state["start_time"] is None and len(state["typed_text"]) == 0 and event.char:
            state["start_time"] = time.time()
            countdown()

        if event.keysym == "BackSpace":
            state["typed_text"] = state["typed_text"][:-1]
            update_display()
            calculate_current_page_stats()
            return "break"
        
        if event.keysym == "Return":
            if len(state["typed_text"]) >= len(state["target_text"]):
                load_new_page()
            return "break"

        if len(event.char) > 0 and event.char.isprintable():
            idx = len(state["typed_text"])
            
            if idx < len(state["target_text"]):
                if event.char == " " and state["target_text"][idx] != " ":
                    return "break"
                
                state["typed_text"] += event.char
                update_display()
                calculate_current_page_stats()
            return "break"

    hidden_entry.bind("<KeyPress>", on_key_press)

    def countdown():
        nonlocal time_left
        if not is_playing: return
        if time_left > 0:
            timer_label.config(text=str(time_left))
            time_left -= 1
            timer_id = root.after(1000, countdown)
        else:
            end_game(state)

    def end_game(st):
        global is_playing, timer_id
        is_playing = False
        if timer_id:
            root.after_cancel(timer_id)
        show_result(st)

    load_new_page()

# ==================== 界面 3：结算界面 ====================
def show_result(st):
    clear_frames()
    result_frame.pack(fill="both", expand=True)
    
    for widget in result_frame.winfo_children():
        widget.destroy()

    words = st.get("final_words", 0)
    acc = st.get("final_acc", 0.0)
    
    raw_score = words * acc
    if raw_score.is_integer():
        score_str = str(int(raw_score))
    else:
        score_str = f"{raw_score:.1f}"

    mode = st["mode"]
    score_text = f"Score: {score_str} (Practice)" if mode == "practice" else f"Score: {score_str}"

    tk.Label(result_frame, text=score_text, font=("Arial", 50, "bold"), bg="#323437", fg="#e2b714").pack(pady=(200, 30))
    
    detail_text = f"Words typed: {words}       Accuracy: {acc*100:.0f}%"
    tk.Label(result_frame, text=detail_text, font=("Arial", 20), bg="#323437", fg="#646669").pack(pady=20)

    # ==================== 仅 Practice 有按钮 ====================
    if mode == "practice":
        tk.Button(result_frame, text="back", font=("Arial", 20), width=10, bg="#2c2e31", fg="#d1d0c5", borderwidth=0, command=show_main_menu).pack(pady=50)
    # 比赛模式什么都不给，连按钮都没了，用户只能结束进程

show_main_menu()
root.mainloop()