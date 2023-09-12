from pynput.keyboard import Controller
from pynput.mouse import Listener
from pynput import keyboard
import tkinter as tk
import pyautogui
import threading

class App:         

    def __init__(self, root):
        self.root = root
        self.root.title("Pixelyzernator")
        self.root.geometry("250x300")
        self.root.resizable(False, False)
        self.keyboard_controller = Controller()
        self.keystroke = None

        self.run = False
        self.listener = None
        self.stop_listener_flag = False

        def show():
            start_button = tk.Button(root, text="Start", command=self.start, width=5, height=1, relief="groove").place(x=70, y=10)
            stop_button = tk.Button(root, text="Stop", command=self.stop, width=5, height=1, relief="groove").place(x=133, y=10)
            clear_button = tk.Button(root, text="Clear", command=self.clear, width=5, height=1, relief="groove").place(x=193, y=10)

        def commands():
            self.scan()
            show()

        scan_button = tk.Button(root, text="Scan", command=commands, width=5, height=1, relief="groove").place(x=10, y=10)
   
        self.output_text = tk.Text(root, wrap=tk.WORD, height=10, width=28)
        self.output_text.place(x=10, y=40)

        self.color_canvas_og = tk.Canvas(root, width=80, height=60)
        self.color_canvas_og.place(x=10, y=210)
        label_widget_og = tk.Label(root, text=' Original', width=10)
        label_widget_og.place(x=11, y=275)

        trigger_button = tk.Button(root, text="SET", command=self.set, width=5, height=2, relief="groove").place(x=103, y=222)

        self.color_canvas = tk.Canvas(root, width=80, height=60)
        self.color_canvas.place(x=155, y=210)
        label_widget = tk.Label(root, text=' Current', width=10)
        label_widget.place(x=156, y=275)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_color_value(self, red, green, blue):
        return '#{:02x}{:02x}{:02x}'.format(red, green, blue)

    def get_color_value2(self, red, green, blue):
        return '#{:02x}{:02x}{:02x}'.format(red, green, blue)
    
    def on_key_press(self, key):
        try:
            keystroke = key.char
        except AttributeError:
            keystroke = str(key)
        if keystroke:
            self.update_output_text("You pressed: " + keystroke)
            self.root.clipboard_clear()
            self.root.clipboard_append(keystroke)
            self.root.update()
            self.keystroke = keystroke
            self.stop_listener()

    def set(self):
        self.update_output_text("\nPRESS MACRO KEY\n")
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()


 

    def start(self):
        if not self.run:
            self.run = True

    def stop(self):
        if self.run:
            self.run = False

    def clear(self):
        self.stop()
        self.keystroke = ""
        self.output_text.delete('1.0', tk.END)
        self.color_canvas.config(bg=self.get_color_value(240, 240, 240))
        self.color_canvas_og.config(bg=self.get_color_value(240, 240, 240))

    def autoscroll_text(self):
        self.output_text.see(tk.END)
        self.root.after(50, self.autoscroll_text)

    def update_output_text(self, text):
        self.output_text.insert(tk.END, text + '\n')
        self.output_text.see(tk.END)


    def update_pixel_color(self):
        if self.run:
            r, g, b = pyautogui.pixel(self.x, self.y)
            rgb = (r, g, b)
            if rgb == (self.r1, self.g1, self.b1):
                self.update_output_text("RGB: {},{},{} @ {}x{}".format(self.r1, self.g1, self.b1, self.x, self.y))
                self.color_canvas.config(bg=self.get_color_value(r, g, b))

            elif rgb != (self.r1, self.g1, self.b1):
                self.update_output_text("RGB: {},{},{} @ {}x{}".format(r, g, b, self.x, self.y))
                self.color_canvas.config(bg=self.get_color_value2(r, g, b))
                if self.keystroke:
                    self.keyboard_controller.type(self.keystroke)
        
        self.root.after(50, self.update_pixel_color)

    def on_close(self):
        self.stop()
        self.root.destroy()
    
    def scan(self):
        self.stop()
        self.update_output_text("SELECT PIXEL ON SCREEN")

        def on_click(x, y, button, pressed):
            if pressed:
                self.x, self.y = x, y
                self.r1, self.g1, self.b1 = pyautogui.pixel(self.x, self.y)
                self.update_output_text("\n----------------------------\nSELECTED:\nRGB: {},{},{} @ {}x{}\n----------------------------".format(self.r1, self.g1, self.b1, self.x, self.y))
                self.color_canvas_og.config(bg=self.get_color_value(self.r1, self.g1, self.b1))
                self.xy = (self.x, self.y)
                return False # stops listener

        listener_thread = threading.Thread(target=lambda: Listener(on_click=on_click).start())
        listener_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.update_pixel_color()
    root.mainloop()