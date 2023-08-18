import tkinter as tk
from tkinter import messagebox, simpledialog
import configparser
import random
import pygame
import sys
import math
import functools

# 對話框
class CustomDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, message="", result_choice="", **options):
        self.message = message
        self.result_choice = result_choice
        super().__init__(parent, **options)

    def body(self, master):
        self.result = None
        master.config(bg="#FFFFFF")  # 設定對話框主體的背景顏色（純白色）
        
        # 顯示訊息
        tk.Label(master, text=self.message, bg="#FFFFFF", font=("Arial", 12)).grid(row=0, sticky=tk.W) 
        
        # 顯示結果選項
        self.result_label = tk.Label(master, text=self.result_choice, bg="#FFFFFF", font=("Arial", 14, "bold"))
        self.result_label.grid(row=1, pady=10, sticky=tk.W)

        self.configure(bg="#FFFFFF") 
        self.geometry_center(self.master.winfo_toplevel())

        return None

    # 將對話框位置設置在視窗中央
    def geometry_center(self, win):
        win.update_idletasks() 

        x = (win.winfo_screenwidth() // 2) - (win.winfo_width() // 2)
        y = (win.winfo_screenheight() // 2) - (win.winfo_height() // 2)
        win.geometry('{}x{}+{}+{}'.format(win.winfo_width(), win.winfo_height(), x, y))

    # 定義對話框中的按鈕框
    def buttonbox(self):
        box = tk.Frame(self, bg="#FFFFFF")  # 設定按鈕框的背景顏色（純白色）
    
        ok_btn = tk.Button(box, text="確定", width=10, command=lambda: self.ok("確定"), bg="#F7CAC9", fg="#000000", font=("Arial", 12))  
        ok_btn.grid(row=0, column=0, padx=5, pady=5)
    
        retry_btn = tk.Button(box, text="再選一次", width=10, command=lambda: self.ok("再選一次"), bg="#C4D8E2", fg="#000000", font=("Arial", 12))  
        retry_btn.grid(row=0, column=1, padx=5, pady=5)
    
        rechoose_btn = tk.Button(box, text="重新選擇", width=10, command=lambda: self.ok("重新選擇"), bg="#C4D8E2", fg="#000000", font=("Arial", 12))  
        rechoose_btn.grid(row=0, column=2, padx=5, pady=5)
    
        self.bind("<Escape>", self.cancel)
        box.pack(fill=tk.BOTH, expand=True)

    # 按下「確定」按鈕時觸發的動作
    def ok(self, result_value, event=None):
        self.result = result_value
        self.destroy()

    # 按下「取消」按鈕時觸發的動作
    def cancel(self, event=None):
        self.result = "取消"
        self.destroy()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("選擇器")  # 設定視窗標題
        self.create_widgets()

    # 創建應用程式界面的小工具
    def create_widgets(self):
        self.categories = ['吃', '喝', '玩', '樂']
        for category in self.categories:
            btn = tk.Button(self.root, text=category, command=functools.partial(self.show_roulette, category))
            btn.pack(pady=10)

    # 顯示轉盤對話框
    def show_roulette(self, category):
        self.root.withdraw() 
        result = "再選一次"
        while result == "再選一次":
            picked_option = Roulette(category).run_roulette()  # 執行轉盤選項選擇
            dialog = CustomDialog(self.root, f"選擇: {picked_option}") 
            result = dialog.result

            if result == "再選一次":
                continue
            elif result == "重新選擇":
                self.root.deiconify()  # 重新顯示主視窗
                pygame.quit()  # 終止pygame
                break
            elif result == "確定":
                pygame.quit()  # 終止pygame
                self.root.quit()  # 關閉tkinter應用程式
                sys.exit(0)

# 轉盤類別
class Roulette:
    def __init__(self, category):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))  # 設定pygame視窗大小
        pygame.display.set_caption(f"轉盤 - {category}")  # 設定視窗標題

        self.initial_rotations = 3  # 轉盤的啟動旋轉次數
        self.options = self.read_choices(category)
        self.rotation_speed = 10  # 每幀旋轉的角度
        self.angle = random.randint(0, 359)  # 初始角度
        self.COLORS = [(247, 202, 201), (146, 171, 209)]
        self.result = None

    # 從設定檔中讀取選項
    def read_choices(self, category):
        config = configparser.ConfigParser()
        config.read('choices.ini', encoding='utf-8')
        options = [option for key, option in config[category].items()]
        return options

    # 繪製轉盤選項
    def draw_options(self, selected_index=None):
        num_options = len(self.options)
        for idx, option in enumerate(self.options):
            start_angle = idx * (360 / num_options) + self.angle
            stop_angle = (idx + 1) * (360 / num_options) + self.angle

            # 計算扇形的邊界點
            slice_points = [(250, 250)]
        
            for angle in range(int(start_angle*10), int(stop_angle*10), 10):  # 使用10倍精確度的角度
                x = 250 + 200 * math.cos(math.radians(angle/10))
                y = 250 + 200 * math.sin(math.radians(angle/10))
                slice_points.append((x, y))
        
            slice_points.append((250 + 200 * math.cos(math.radians(stop_angle)), 250 + 200 * math.sin(math.radians(stop_angle))))  # 確保終點被添加
            slice_points.append((250, 250))

            # 繪製扇形
            pygame.draw.polygon(self.screen, self.COLORS[idx % 2], slice_points)

            # 扇形的中心
            angle_center = (start_angle + stop_angle) / 2
            x = 250 + 180 * math.cos(math.radians(angle_center))
            y = 250 + 180 * math.sin(math.radians(angle_center))

            font_path = "C:\Windows\Fonts\mingliu.ttc"  # 指定字體文件的路徑和名稱
            text = pygame.font.Font(font_path, 24).render(option, True, (0, 0, 0))
            self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    
        # 若有指定被選擇的選項，計算中心角度
        if selected_index is not None:
            segment_angle = 360 / num_options
            pointer_angle = 360 - (self.angle + (selected_index * segment_angle) + (segment_angle / 2)) % 360
        else:
            pointer_angle = 90 

        # 使用中心角度繪製指針
        tip = (250 + 20 * math.cos(math.radians(pointer_angle)), 250 - 20 * math.sin(math.radians(pointer_angle)))
        left_base = (250 + 10 * math.cos(math.radians(pointer_angle + 150)), 250 - 10 * math.sin(math.radians(pointer_angle + 150)))
        right_base = (250 + 10 * math.cos(math.radians(pointer_angle - 150)), 250 - 10 * math.sin(math.radians(pointer_angle - 150)))

        pygame.draw.polygon(self.screen, (255, 0, 0), [tip, left_base, right_base])

    # 運行轉盤動畫
    def run_roulette(self):
        clock = pygame.time.Clock()

        selected_index = random.randint(0, len(self.options) - 1)
        target_angle = selected_index * (360 / len(self.options)) + (360 / (2 * len(self.options)))

        while self.rotation_speed > 0.1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            delta_angle = target_angle - self.angle
            if delta_angle > 180:
                delta_angle -= 360
            elif delta_angle < -180:
                delta_angle += 360

            if abs(delta_angle) < self.rotation_speed:
                self.rotation_speed = abs(delta_angle)

            if delta_angle > 0:
                self.angle += self.rotation_speed
            else:
                self.angle -= self.rotation_speed

            self.angle %= 360
            self.rotation_speed -= 0.1  # 減緩旋轉速度

            self.screen.fill((255, 255, 255))  # 清空畫面
            pygame.draw.circle(self.screen, (0, 255, 0), (250, 250), 200, 0)  # 繪製圓圈
            
            self.draw_options(selected_index)

            pygame.display.flip()  # 更新顯示
            clock.tick(30)  # 控制幀率為30

        picked_option = self.options[selected_index]  # 直接使用之前選取的選項
        return picked_option


# 主程式入口
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)  # 創建應用程式實例
    root.mainloop()  # 開始主迴圈
    sys.exit(0)  # 確保應用程式完全終止
