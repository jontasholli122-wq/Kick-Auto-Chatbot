import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import logging
import json
import os
import glob
import random
import time
import threading
from queue import Queue
import sys
import tempfile
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Folder and file paths
COOKIE_FOLDER = "cookies"
CHATS_FILE = "chats.txt"

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kick.com Chat Bot Controller")
        self.root.geometry("900x700")
        
        # Bot control variables
        self.running_sessions = {}
        self.stop_events = {}
        self.session_threads = {}
        self.messages = []
        self.cookie_files = []
        self.session_lock = threading.Lock()
        
        # Load resources
        self.load_messages()
        self.load_cookie_files()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Kick.com Chat Bot Controller", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Session control frame
        control_frame = ttk.LabelFrame(main_frame, text="Session Control", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Available accounts
        ttk.Label(control_frame, text=f"Available Accounts: {len(self.cookie_files)}").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(control_frame, text=f"Available Messages: {len(self.messages)}").grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Concurrent sessions control
        ttk.Label(control_frame, text="Concurrent Sessions:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.sessions_var = tk.IntVar(value=1)
        sessions_spinbox = ttk.Spinbox(control_frame, from_=1, to=min(5, len(self.cookie_files)), 
                                     textvariable=self.sessions_var, width=10)
        sessions_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Session delay control
        ttk.Label(control_frame, text="Startup Delay Between Sessions (sec):").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.startup_delay_var = tk.IntVar(value=10)
        ttk.Spinbox(control_frame, from_=5, to=60, textvariable=self.startup_delay_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Message interval control
        ttk.Label(control_frame, text="Message Interval (seconds):").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        interval_frame = ttk.Frame(control_frame)
        interval_frame.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        self.min_interval_var = tk.IntVar(value=30)
        self.max_interval_var = tk.IntVar(value=90)
        
        ttk.Label(interval_frame, text="Min:").grid(row=0, column=0)
        ttk.Spinbox(interval_frame, from_=10, to=300, textvariable=self.min_interval_var, width=8).grid(row=0, column=1, padx=(5, 10))
        ttk.Label(interval_frame, text="Max:").grid(row=0, column=2)
        ttk.Spinbox(interval_frame, from_=10, to=300, textvariable=self.max_interval_var, width=8).grid(row=0, column=3, padx=(5, 0))
        
        # Browser options
        options_frame = ttk.LabelFrame(control_frame, text="Browser Options", padding="5")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Headless Mode (hidden browsers)", variable=self.headless_var).grid(row=0, column=0, sticky=tk.W)
        
        self.sequential_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Sequential Mode (start sessions one by one)", variable=self.sequential_var).grid(row=1, column=0, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(20, 0))
        
        self.start_button = ttk.Button(button_frame, text="Start Bot Sessions", command=self.start_sessions)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="Stop All Sessions", command=self.stop_all_sessions, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        refresh_button = ttk.Button(button_frame, text="Refresh Files", command=self.refresh_files)
        refresh_button.grid(row=0, column=2)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status Log", padding="10")
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Status display
        self.status_text = scrolledtext.ScrolledText(status_frame, height=15, width=90)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Running sessions display
        sessions_frame = ttk.LabelFrame(main_frame, text="Active Sessions", padding="10")
        sessions_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.sessions_label = ttk.Label(sessions_frame, text="No active sessions")
        self.sessions_label.grid(row=0, column=0, sticky=tk.W)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
    def refresh_files(self):
        """Refresh the loaded files."""
        self.load_messages()
        self.load_cookie_files()
        self.log("Files refreshed")
        messagebox.showinfo("Refresh", f"Loaded {len(self.cookie_files)} cookie files and {len(self.messages)} messages")
        
    def create_isolated_driver(self, session_id):
        """Create a Chrome driver with isolated user data directory."""
        try:
            # Create unique temp directory for this session
            temp_dir = tempfile.mkdtemp(prefix=f"chrome_session_{session_id}_")
            
            options = uc.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-first-run")
            options.add_argument("--disable-default-apps")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")  # Faster loading
            options.add_argument("--disable-javascript")  # Disable JS for faster loading (may need to remove if site requires it)
            options.add_argument(f"--user-data-dir={temp_dir}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            if self.headless_var.get():
                options.add_argument("--headless=new")
                
            # Create driver with version_main to avoid conflicts
            driver = uc.Chrome(options=options, use_subprocess=False, version_main=None)
            return driver, temp_dir
            
        except Exception as e:
            self.log(f"{session_id}: Failed to create driver - {str(e)}")
            return None, None
            
    def load_messages(self):
        """Load chat messages from file."""
        try:
            if os.path.exists(CHATS_FILE):
                with open(CHATS_FILE, "r", encoding="utf-8") as f:
                    self.messages = [line.strip() for line in f if line.strip()]
            else:
                # Create default messages file if it doesn't exist
                default_messages = [
                    "Hello everyone!",
                    "Great stream!",
                    "Loving the content!",
                    "This is awesome!",
                    "Keep it up!",
                    "Amazing gameplay!",
                    "LOL",
                    "Nice!",
                    "Poggers",
                    "Good stuff!",
                    "Epic moment!",
                    "KEKW",
                    "Incredible!",
                    "So good!",
                    "Best streamer!",
                    "monkaW",
                    "PogChamp",
                    "5Head",
                    "EZ Clap",
                    "Let's goooo!"
                ]
                with open(CHATS_FILE, "w", encoding="utf-8") as f:
                    for msg in default_messages:
                        f.write(msg + "\n")
                self.messages = default_messages
                
        except Exception as e:
            self.messages = ["Hello!", "Great stream!", "Amazing!"]
            
    def load_cookie_files(self):
        """Load available cookie files."""
        if os.path.exists(COOKIE_FOLDER):
            self.cookie_files = glob.glob(os.path.join(COOKIE_FOLDER, "*.json"))
        else:
            os.makedirs(COOKIE_FOLDER, exist_ok=True)
            self.cookie_files = []
            
    def log(self, message):
        """Add message to status display."""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Thread-safe GUI update
        def update_gui():
            self.status_text.insert(tk.END, log_message)
            self.status_text.see(tk.END)
            
        self.root.after(0, update_gui)
        logging.info(message)
        
    def update_sessions_display(self):
        """Update the active sessions display."""
        with self.session_lock:
            active_sessions = [sid for sid, status in self.running_sessions.items() if status]
            if active_sessions:
                text = f"Active Sessions: {', '.join(active_sessions)} ({len(active_sessions)} total)"
            else:
                text = "No active sessions"
                
        def update_gui():
            self.sessions_label.config(text=text)
        self.root.after(0, update_gui)
            
    def start_sessions(self):
        """Start the specified number of bot sessions."""
        if not self.cookie_files:
            messagebox.showerror("Error", f"No cookie files found in '{COOKIE_FOLDER}' folder!")
            return
            
        if not self.messages:
            messagebox.showerror("Error", f"No chat messages found in '{CHATS_FILE}' file!")
            return
            
        num_sessions = self.sessions_var.get()
        available_accounts = len(self.cookie_files)
        
        if num_sessions > available_accounts:
            messagebox.showwarning("Warning", f"Requested {num_sessions} sessions but only {available_accounts} accounts available. Starting {available_accounts} sessions.")
            num_sessions = available_accounts
            
        # Validate intervals
        min_interval = self.min_interval_var.get()
        max_interval = self.max_interval_var.get()
        if min_interval >= max_interval:
            messagebox.showerror("Error", "Max interval must be greater than min interval!")
            return
            
        # Select random cookie files
        selected_cookies = random.sample(self.cookie_files, num_sessions)
        
        self.log(f"Starting {num_sessions} bot sessions...")
        self.log(f"Message interval: {min_interval}-{max_interval} seconds")
        self.log(f"Startup delay: {self.startup_delay_var.get()} seconds between sessions")
        
        # Update button states
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Start sessions with proper delays
        if self.sequential_var.get():
            # Sequential startup (recommended for stability)
            self.start_sessions_sequential(selected_cookies)
        else:
            # Concurrent startup with delays
            self.start_sessions_concurrent(selected_cookies)
            
    def start_sessions_sequential(self, selected_cookies):
        """Start sessions one by one (more stable)."""
        def sequential_starter():
            for i, cookie_file in enumerate(selected_cookies):
                if not any(self.stop_events.values()):  # Check if not stopped
                    session_id = f"session_{i+1}"
                    self.start_single_session(session_id, cookie_file)
                    
                    # Wait between sessions (except for the last one)
                    if i < len(selected_cookies) - 1:
                        delay = self.startup_delay_var.get()
                        self.log(f"Waiting {delay} seconds before starting next session...")
                        time.sleep(delay)
                        
        starter_thread = threading.Thread(target=sequential_starter)
        starter_thread.daemon = True
        starter_thread.start()
        
    def start_sessions_concurrent(self, selected_cookies):
        """Start sessions with staggered delays."""
        for i, cookie_file in enumerate(selected_cookies):
            delay = i * self.startup_delay_var.get()
            session_id = f"session_{i+1}"
            
            def delayed_start(sid, cf, d):
                time.sleep(d)
                self.start_single_session(sid, cf)
                
            starter_thread = threading.Thread(target=delayed_start, args=(session_id, cookie_file, delay))
            starter_thread.daemon = True
            starter_thread.start()
            
    def start_single_session(self, session_id, cookie_file):
        """Start a single bot session."""
        with self.session_lock:
            stop_event = threading.Event()
            self.stop_events[session_id] = stop_event
            self.running_sessions[session_id] = True
            
        # Start session thread
        thread = threading.Thread(target=self.run_session, args=(session_id, cookie_file, stop_event))
        thread.daemon = True
        thread.start()
        
        self.session_threads[session_id] = thread
        self.update_sessions_display()
        
    def run_session(self, session_id, cookie_file, stop_event):
        """Run a single bot session with better isolation."""
        self.log(f"{session_id}: Starting with {os.path.basename(cookie_file)}")
        
        driver = None
        temp_dir = None
        
        try:
            # Load cookies
            with open(cookie_file, "r") as f:
                cookies = json.load(f)
                
            # Create isolated driver instance
            driver, temp_dir = self.create_isolated_driver(session_id)
            if not driver:
                raise Exception("Failed to create Chrome driver")
                
            # Navigate and login
            self.log(f"{session_id}: Navigating to Kick.com...")
            driver.get("https://kick.com/asmongod")
            time.sleep(random.uniform(3, 6))
            
            if stop_event.is_set():
                return
                
            # Inject cookies
            self.log(f"{session_id}: Injecting cookies...")
            cookie_count = 0
            for cookie in cookies:
                try:
                    # Clean up cookie format
                    if "sameSite" in cookie:
                        cookie["sameSite"] = cookie["sameSite"].capitalize() if cookie["sameSite"].lower() in ["lax", "strict", "none"] else "None"
                    cookie.pop("storeId", None)
                    if "expirationDate" in cookie:
                        cookie["expiry"] = int(cookie["expirationDate"])
                        del cookie["expirationDate"]
                    
                    driver.add_cookie(cookie)
                    cookie_count += 1
                except Exception as cookie_error:
                    continue
                    
            self.log(f"{session_id}: Injected {cookie_count} cookies")
            time.sleep(random.uniform(1, 3))
            
            if stop_event.is_set():
                return
                
            # Refresh and verify login
            driver.refresh()
            time.sleep(random.uniform(4, 7))
            
            # Verify login with multiple attempts
            login_verified = False
            for attempt in range(3):
                try:
                    # Check for chat elements
                    chat_elements = driver.find_elements(By.CSS_SELECTOR, ".editor-paragraph, #send-message-button, [data-testid='chat-input']")
                    if chat_elements:
                        login_verified = True
                        break
                    else:
                        self.log(f"{session_id}: Login attempt {attempt + 1} - chat interface not found, retrying...")
                        time.sleep(2)
                except:
                    time.sleep(2)
                    
            if not login_verified:
                raise Exception("Login verification failed - chat interface not accessible")
                
            self.log(f"{session_id}: Login successful!")
            
            # Send initial message
            if self.send_random_message(driver, session_id):
                self.log(f"{session_id}: Initial message sent")
            else:
                self.log(f"{session_id}: Initial message failed, but continuing...")
            
            # Start continuous messaging loop
            self.log(f"{session_id}: Starting continuous chat mode...")
            
            message_count = 0
            while not stop_event.is_set():
                # Random wait interval
                min_wait = self.min_interval_var.get()
                max_wait = self.max_interval_var.get()
                wait_time = random.uniform(min_wait, max_wait)
                
                if stop_event.wait(wait_time):
                    break
                    
                # Send random message
                if self.send_random_message(driver, session_id):
                    message_count += 1
                    if message_count % 5 == 0:  # Log every 5 messages
                        self.log(f"{session_id}: Sent {message_count} messages total")
                else:
                    self.log(f"{session_id}: Message failed, continuing...")
                    
        except Exception as e:
            self.log(f"{session_id}: Error - {str(e)}")
            
        finally:
            # Cleanup
            if driver:
                try:
                    driver.quit()
                except:
                    pass
                    
            # Clean up temp directory
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
                    
            with self.session_lock:
                self.running_sessions[session_id] = False
                
            self.log(f"{session_id}: Session ended")
            self.root.after(100, self.update_sessions_display)
            
    def send_random_message(self, driver, session_id):
        """Send a randomly selected chat message."""
        try:
            if not self.messages:
                return False
                
            # Select random message
            message = random.choice(self.messages)
            
            # Try multiple selectors for chat input
            chat_selectors = [
                ".editor-paragraph",
                "[data-testid='chat-input']",
                "textarea[placeholder*='chat']",
                "input[placeholder*='message']",
                "#chatroom-input"
            ]
            
            chat_input = None
            for selector in chat_selectors:
                try:
                    chat_input = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
                    
            if not chat_input:
                return False
            
            # Clear any existing text and focus
            try:
                chat_input.clear()
            except:
                pass
                
            time.sleep(random.uniform(0.3, 0.8))
            chat_input.click()
            time.sleep(random.uniform(0.2, 0.5))
            
            # Type message with human-like speed
            for char in message:
                chat_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.12))
                
            time.sleep(random.uniform(0.5, 1.2))
            
            # Send message (try Enter key first, then button)
            try:
                chat_input.send_keys(Keys.RETURN)
            except:
                # Fallback: try clicking send button
                try:
                    send_button = driver.find_element(By.ID, "send-message-button")
                    send_button.click()
                except:
                    return False
            
            self.log(f"{session_id}: → '{message}'")
            return True
            
        except Exception as e:
            return False
            
    def stop_all_sessions(self):
        """Stop all running sessions."""
        self.log("Stopping all sessions...")
        
        # Signal all sessions to stop
        for stop_event in self.stop_events.values():
            stop_event.set()
            
        # Update UI immediately
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
        # Clean up in background
        def cleanup():
            # Wait for threads to finish
            for thread in self.session_threads.values():
                thread.join(timeout=10)
                
            with self.session_lock:
                self.running_sessions.clear()
                self.stop_events.clear()
                self.session_threads.clear()
                
            self.root.after(100, self.update_sessions_display)
            self.log("All sessions stopped and cleaned up")
            
        cleanup_thread = threading.Thread(target=cleanup)
        cleanup_thread.daemon = True
        cleanup_thread.start()
        
    def on_closing(self):
        """Handle window close event."""
        active_sessions = [s for s in self.running_sessions.values() if s]
        if active_sessions:
            if messagebox.askokcancel("Quit", "Stop all sessions and quit?"):
                self.stop_all_sessions()
                self.root.after(2000, self.root.destroy)  # Give time for cleanup
        else:
            self.root.destroy()

def main():
    # Check for required files/folders
    if not os.path.exists(COOKIE_FOLDER):
        print(f"Creating {COOKIE_FOLDER} folder...")
        os.makedirs(COOKIE_FOLDER, exist_ok=True)
        print(f"Please add your cookie JSON files to the '{COOKIE_FOLDER}' folder")
        
    if not os.path.exists(CHATS_FILE):
        print(f"Creating default {CHATS_FILE} file...")
        default_messages = [
            "Hello everyone!",
            "Great stream!",
            "Loving the content!",
            "This is awesome!",
            "Keep it up!",
            "Amazing gameplay!",
            "LOL",
            "Nice!",
            "Poggers",
            "Good stuff!",
            "Epic moment!",
            "KEKW",
            "Incredible!",
            "So good!",
            "Best streamer!",
            "monkaW",
            "PogChamp", 
            "5Head",
            "EZ Clap",
            "Let's goooo!"
        ]
        with open(CHATS_FILE, "w", encoding="utf-8") as f:
            for msg in default_messages:
                f.write(msg + "\n")
        print(f"Created {CHATS_FILE} with default messages. You can edit it to add your own messages.")
    
    # Create and run GUI
    root = tk.Tk()
    app = ChatBotGUI(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    print("Starting Chat Bot GUI...")
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down...")
        
if __name__ == "__main__":
    main()