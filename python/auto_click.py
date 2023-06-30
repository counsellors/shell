from PIL import ImageGrab
import pyautogui
import keyboard
import time

class AutoClicker:
    def __init__(self, color):
        self.color = color
        self.last_color = None
        self.stop_auto_click = False
        self.stop_color_detection = False

    def start(self):
        print("Press 's' to start auto click.")
        try:  # 在主循环中增加try-except语句，捕获KeyboardInterrupt异常
            while True:
                command = input("Enter command (s: start auto-click, c: start auto-detect, q: quit): ")
                if command == 'q':
                    break
                elif command == 's':
                    self.start_auto_click()
                elif command == 'c':
                    self.start_color_detection()
        except KeyboardInterrupt:  # 捕获KeyboardInterrupt异常，并输出一条提示信息
            print("\nProgram terminated by user.")

    def start_auto_click(self):
        print("Press 'ctrl+f3' to stop auto click.")
        keyboard.add_hotkey('ctrl+f3', self.stop)
        start_time = time.time()
        while not self.stop_auto_click:
            try:  
                # 在截图screenshot的位置增加异常捕获
                screenshot = ImageGrab.grab()
                pixels = screenshot.load()
                is_clicked = 0
                for x in range(screenshot.width):
                    if is_clicked == 0:
                        for y in range(screenshot.height):
                            if is_clicked == 0:
                                if pixels[x, y] == self.color:
                                    pyautogui.click(x, y, button='left')
                                    print(f"Clicked at ({x}, {y})")
                                    is_clicked  = 1
                elapsed_time = time.time() - start_time
                if elapsed_time >= 10:
                    self.stop_auto_click = True
                time.sleep(2)
            except Exception as e:
                print(f"Error: {e}")
            # print("识别ctrl+f3..")
            # if keyboard.is_pressed('ctrl+f3'):
            #     self.stop_auto_click = True

        print("Auto click stopped.")

    def stop(self):
        self.stop_auto_click = True

    def start_color_detection(self):
        print("Press 'ctrl+f3' to stop color detection.")
        keyboard.add_hotkey('ctrl+f3', self.stop)
        while not self.stop_color_detection:
            try:  # 在截图screenshot的位置增加异常捕获
                screenshot = ImageGrab.grab(bbox=(pyautogui.position().x, pyautogui.position().y, pyautogui.position().x  + 1, pyautogui.position().y  + 1))
                color = screenshot.getpixel((0, 0))
                if color != self.last_color:
                    print(f"Current color: {color} ")
                    self.last_color = color
            except Exception as e:
                print("sunon> 截图左上角坐标:({} {}),右下角坐标: （{} {}）".format(pyautogui.position().x, pyautogui.position().y, pyautogui.position().x  + 1, pyautogui.position().y  + 1))
                print(f"Error: {e}")

        print("Color detection stopped.")

    def stop_cd(self):
        self.stop_color_detection = True

def main():
    color = (106, 153, 85)
    auto_clicker = AutoClicker(color)
    auto_clicker.start()

if __name__ == '__main__':
    main()