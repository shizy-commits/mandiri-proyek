import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import winsound  # Library standar Windows (Gak perlu install apa-apa)

class SweepXMath:
    def __init__(self, root):
        self.root = root
        self.root.title("Sweep x Math")
        self.root.configure(bg="#121212")
        
        self.username = ""
        self.size = 10
        self.bomb_count = 12
        self.time_limit = 300
        self.max_targets = 3
        
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        menu_frame = tk.Frame(self.root, bg="#121212", padx=40, pady=40)
        menu_frame.pack()

        tk.Label(menu_frame, text="🧩 SWEEP x MATH", font=("Segoe UI", 28, "bold"), fg="#00d2ff", bg="#121212").pack(pady=10)
        
        tk.Label(menu_frame, text="Masukkan Nama Player:", font=("Segoe UI", 10), fg="white", bg="#121212").pack()
        self.name_entry = tk.Entry(menu_frame, font=("Segoe UI", 14), justify="center", bg="#2c2c3e", fg="white", insertbackground="white")
        self.name_entry.focus_set() 
        self.name_entry.pack(pady=15)

        btn_style = {"font": ("Segoe UI", 11, "bold"), "width": 25, "pady": 8, "cursor": "hand2"}
        
        tk.Button(menu_frame, text="🟢 EASY (300s | 3 Target)", bg="#2ecc71", **btn_style, 
                  command=lambda: self.show_rules(8, 8, 300, 3)).pack(pady=5)
        
        tk.Button(menu_frame, text="🟡 NORMAL (300s | 4 Target)", bg="#f1c40f", **btn_style, 
                  command=lambda: self.show_rules(10, 15, 300, 4)).pack(pady=5)
        
        tk.Button(menu_frame, text="🔴 HARD (150s | 5 Target)", bg="#e74c3c", **btn_style, 
                  command=lambda: self.show_rules(12, 25, 150, 5)).pack(pady=5)

    def show_rules(self, size, bombs, time, target_limit):
        self.username = self.name_entry.get().strip() or "Guest"
        for widget in self.root.winfo_children():
            widget.destroy()

        rules_frame = tk.Frame(self.root, bg="#1e1e2f", padx=30, pady=30, highlightbackground="#00d2ff", highlightthickness=2)
        rules_frame.pack(padx=20, pady=20)

        tk.Label(rules_frame, text="📜 ATURAN MAIN", font=("Segoe UI", 18, "bold"), fg="#00d2ff", bg="#1e1e2f").pack(pady=10)
        
        rules_text = (
            "1. TUJUAN: Buka semua kotak yang bukan bom untuk menang.\n"
            "2. KLIK KIRI: Membuka kotak. Jika kena bom, jawab kuis matematika!\n"
            "3. KLIK KANAN (TARGET 🎯): Gunakan untuk membidik lokasi bom.\n"
            "4. SNIPER BONUS: Jika bidikan 🎯 benar, kamu dapat +10 POIN!\n"
            "5. NO PENALTY: Salah bidik 🎯 tidak kurang poin, tapi jatah target berkurang.\n"
            f"6. LIMIT TARGET: Jatah target kamu adalah {target_limit}.\n"
            "7. EMOJI RADAR: Cek emoji (🍀, 🍃, 🟡, 🟠, 🔴, 💀) untuk info bom sekitar."
        )

        tk.Label(rules_frame, text=rules_text, font=("Segoe UI", 11), fg="white", bg="#1e1e2f", justify="left", wraplength=400).pack(pady=10)
        tk.Button(rules_frame, text="SAYA MENGERTI, MULAI!", font=("Segoe UI", 12, "bold"), bg="#00d2ff", command=lambda: self.start_game(size, bombs, time, target_limit)).pack(pady=20)

    def start_game(self, size, bombs, time, target_limit):
        self.size = size
        self.bomb_count = bombs
        self.time_limit = time
        self.max_targets = target_limit
        self.setup_game_board()

    def setup_game_board(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.frame = tk.Frame(self.root, bg="#121212", padx=20, pady=20)
        self.frame.pack()

        self.buttons = {}
        self.bombs = set()
        self.opened = set()
        self.flags = set()
        self.score = 0
        self.time_left = self.time_limit
        self.game_active = True

        self.info_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.info_frame.pack(fill="x", padx=20)

        self.info = tk.Label(self.info_frame, text=f"👤 {self.username} | ⏳ {self.time_left}s | 🏆 {self.score} | 🎯 Sisa: {self.max_targets}",
                             font=("Segoe UI", 11, "bold"), fg="#00d2ff", bg="#1e1e2f", pady=10)
        self.info.pack()

        self.create_board()
        self.place_bombs()
        self.update_timer()

    def create_board(self):
        for r in range(self.size):
            for c in range(self.size):
                btn = tk.Button(self.frame, text="", width=3, height=1, font=("Segoe UI Emoji", 14), bg="#2c2c3e", fg="white", relief="flat", bd=0)
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.click(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[(r, c)] = btn

    def place_bombs(self):
        while len(self.bombs) < self.bomb_count:
            r, c = random.randint(0, self.size-1), random.randint(0, self.size-1)
            self.bombs.add((r, c))

    def toggle_flag(self, r, c):
        if (r, c) in self.opened or not self.game_active or (r, c) in self.flags:
            return
        
        if len(self.flags) >= self.max_targets:
            winsound.MessageBeep(winsound.MB_ICONERROR) # Suara Error
            messagebox.showwarning("Limit Target", f"Jatah Target 🎯 sudah habis ({self.max_targets})!")
            return

        self.flags.add((r, c))
        self.buttons[(r, c)].config(text="🎯", bg="#ff4757")

        if (r, c) in self.bombs:
            self.score += 10
            winsound.MessageBeep(winsound.MB_OK) # Suara Ding (Benar)
            messagebox.showinfo("Bidikan Jitu!", "Hebat! Kamu membidik bom dengan tepat.\nBonus +10 Poin!")
            self.reveal_cell(r, c, is_bomb=True)
        else:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION) # Suara Peringatan
            messagebox.showwarning("Meleset", "Itu bukan bom, tapi jatah targetmu terpakai 1.")
            self.opened.add((r, c))
        
        self.update_info()
        self.check_win()

    def click(self, r, c):
        if (r, c) in self.opened or (r, c) in self.flags or not self.game_active:
            return

        if (r, c) in self.bombs:
            winsound.MessageBeep(winsound.MB_ICONHAND) # Suara Stop (Bahaya)
            if self.ask_math():
                self.score += 50
                winsound.MessageBeep(winsound.MB_OK) # Suara Ding (Benar)
                self.reveal_cell(r, c, is_bomb=True)
                messagebox.showinfo("Berhasil", "Bom dijinakkan lewat Matematika! +50 Poin")
            else:
                self.game_over(False)
                return
        else:
            n = self.count_near(r, c)
            self.reveal_cell(r, c)
            if n == 0:
                self.auto_open(r, c)
        
        self.update_info()
        self.check_win()

    def auto_open(self, r, c):
        for i in range(max(0, r-1), min(self.size, r+2)):
            for j in range(max(0, c-1), min(self.size, c+2)):
                if (i, j) not in self.opened:
                    self.click(i, j)

    def ask_math(self):
        a, b = random.randint(2, 12), random.randint(2, 12)
        ans = simpledialog.askinteger("DEFUSE BOMB!", f"Selesaikan soal ini:\n\n{a} x {b} = ?")
        return ans == (a * b)

    def reveal_cell(self, r, c, is_bomb=False):
        btn = self.buttons[(r, c)]
        if is_bomb:
            btn.config(text="⚡", bg="#6c5ce7", state="disabled")
        else:
            n = self.count_near(r, c)
            themes = {0:("🍀","#1b5e20"), 1:("🍃","#2e7d32"), 2:("🟡","#f9a825"), 
                      3:("🟠","#ef6c00"), 4:("🔴","#c62828"), 5:("💀","#8e0000")}
            emoji, color = themes.get(n, themes[5])
            btn.config(text=emoji, bg=color, state="disabled")
        self.opened.add((r, c))

    def count_near(self, r, c):
        count = 0
        for i in range(max(0, r-1), min(self.size, r+2)):
            for j in range(max(0, c-1), min(self.size, c+2)):
                if (i, j) in self.bombs: count += 1
        return count

    def update_info(self):
        t_left = self.max_targets - len(self.flags)
        self.info.config(text=f"👤 {self.username} | ⏳ {self.time_left}s | 🏆 {self.score} | 🎯 Sisa: {t_left}")

    def update_timer(self):
        if not self.game_active: return
        if self.time_left <= 0:
            self.game_over(False, "Waktu Habis!")
            return
        self.time_left -= 1
        self.update_info()
        self.root.after(1000, self.update_timer)

    def check_win(self):
        if len(self.opened) == self.size ** 2:
            winsound.MessageBeep(winsound.MB_OK)
            self.game_over(True)

    def game_over(self, won, msg=""):
        self.game_active = False
        if not won:
            winsound.Beep(400, 500) # Suara Beep rendah (Kalah)
        
        for (r, c) in self.bombs:
            if (r, c) not in self.opened:
                self.buttons[(r, c)].config(text="💥" if not won else "✅", bg="black" if not won else "green")
        
        status = "MENANG 🏆" if won else "GAME OVER 💥"
        messagebox.showinfo(status, f"Player: {self.username}\nSkor Akhir: {self.score}")
        self.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    game = SweepXMath(root)
    root.mainloop()