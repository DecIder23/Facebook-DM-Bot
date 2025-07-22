import json
import time
import os
import csv
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from config import *

def get_chrome_options():
    """Configure Chrome options for undetected operation"""
    options = uc.ChromeOptions()
    
    # Disable extensions and features for speed and stealth
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-translate')
    options.add_argument('--disable-features=NetworkService,NetworkServiceInProcess')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-component-extensions-with-background-pages')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-device-discovery-notifications')
    options.add_argument('--disable-client-side-phishing-detection')
    options.add_argument('--disable-hang-monitor')
    options.add_argument('--disable-prompt-on-repost')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-permissions-api')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    
   
    
    return options

def is_logged_in(driver):
    """Check if user is already logged into Facebook"""
    try:
        if DEBUG:
            print("[DEBUG] Checking if user is logged in...")
        
        # Wait a bit for page to load
        time.sleep(3)
        
        # Check for multiple indicators that user is logged in
        login_indicators = [
            # Marketplace link
            "//a[@href='/marketplace/' or contains(@href, 'marketplace')]",
            # Groups link
            "//a[@href='/groups/' or contains(@href, 'groups')]",
            # Profile menu/avatar
            "//div[@role='banner']//div[@role='button']//img",
            # Home feed
            "//div[@role='main']//div[@role='feed']",
            # Left sidebar with navigation
            "//div[@role='navigation']",
        ]
        
        for indicator in login_indicators:
            try:
                element = driver.find_element(By.XPATH, indicator)
                if element.is_displayed():
                    if DEBUG:
                        print(f"[DEBUG] Found login indicator: {indicator}")
                    return True
            except NoSuchElementException:
                continue
        
        # Additional check: look for login form (indicates not logged in)
        try:
            login_form = driver.find_element(By.ID, "email")
            if login_form.is_displayed():
                if DEBUG:
                    print("[DEBUG] Login form found - user not logged in")
                return False
        except NoSuchElementException:
            pass
        
        if DEBUG:
            print("[DEBUG] No clear login indicators found")
        return False
        
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error checking login status: {e}")
        return False

def load_cookies(driver):
    """Load cookies from file and apply to current session"""
    try:
        if not os.path.exists(COOKIES_FILE):
            if DEBUG:
                print(f"[DEBUG] Cookies file {COOKIES_FILE} not found")
            return False
        
        with open(COOKIES_FILE, 'r') as f:
            cookies = json.load(f)
        
        if not cookies:
            if DEBUG:
                print("[DEBUG] No cookies found in file")
            return False
        
        if DEBUG:
            print(f"[DEBUG] Loading {len(cookies)} cookies...")
        
        # Add each cookie to the driver
        for cookie in cookies:
            try:
                # Ensure required fields are present
                if 'name' in cookie and 'value' in cookie:
                    # Remove problematic fields that might cause issues
                    cleaned_cookie = {
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': cookie.get('domain', '.facebook.com'),
                        'path': cookie.get('path', '/'),
                    }
                    
                    # Add optional fields if they exist and are valid
                    if 'secure' in cookie:
                        cleaned_cookie['secure'] = cookie['secure']
                    if 'httpOnly' in cookie:
                        cleaned_cookie['httpOnly'] = cookie['httpOnly']
                    
                    driver.add_cookie(cleaned_cookie)
            except Exception as e:
                if DEBUG:
                    print(f"[DEBUG] Error adding cookie {cookie.get('name', 'unknown')}: {e}")
                continue
        
        # Reload the page to apply cookies
        driver.refresh()
        time.sleep(5)
        
        # Check if login was successful
        if is_logged_in(driver):
            if DEBUG:
                print("[DEBUG] Successfully logged in using cookies")
            return True
        else:
            if DEBUG:
                print("[DEBUG] Cookies loaded but login verification failed")
            return False
            
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error loading cookies: {e}")
        return False

def save_cookies(driver):
    """Save current session cookies to file"""
    try:
        cookies = driver.get_cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        if DEBUG:
            print(f"[DEBUG] Saved {len(cookies)} cookies to {COOKIES_FILE}")
        return True
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error saving cookies: {e}")
        return False

def login_with_credentials(driver):
    """Login using email and password from config"""
    try:
        if DEBUG:
            print("[DEBUG] Attempting login with credentials...")
        
        # Wait for email field and enter email
        email_field = WebDriverWait(driver, LOGIN_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.clear()
        email_field.send_keys(FB_EMAIL)
        time.sleep(1)
        
        # Enter password
        password_field = driver.find_element(By.ID, "pass")
        password_field.clear()
        password_field.send_keys(FB_PASSWORD)
        time.sleep(1)
        
        # Click login button
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        
        if DEBUG:
            print("[DEBUG] Login form submitted, waiting for result...")
        
        # Wait for login to complete
        time.sleep(8)
        
        # Check if login was successful
        if is_logged_in(driver):
            if DEBUG:
                print("[DEBUG] Login successful!")
            return True
        else:
            # Check for error messages
            try:
                error_element = driver.find_element(By.XPATH, "//div[contains(@class, 'error') or contains(text(), 'incorrect') or contains(text(), 'wrong')]")
                if DEBUG:
                    print(f"[DEBUG] Login error: {error_element.text}")
            except NoSuchElementException:
                if DEBUG:
                    print("[DEBUG] Login failed - no specific error found")
            return False
            
    except TimeoutException:
        if DEBUG:
            print("[DEBUG] Timeout waiting for login elements")
        return False
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error during credential login: {e}")
        return False

def initialize_driver():
    """Initialize Chrome driver with proper options"""
    try:
        if DEBUG:
            print("[DEBUG] Initializing Chrome driver...")
        
        driver = uc.Chrome(version_main=CHROME_VERSION, options=get_chrome_options())
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        
        if DEBUG:
            print("[DEBUG] Chrome driver initialized successfully")
        return driver
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error initializing driver: {e}")
        raise

def navigate_to_facebook(driver):
    """Navigate to Facebook homepage"""
    try:
        if DEBUG:
            print("[DEBUG] Navigating to Facebook...")
        
        driver.get("https://www.facebook.com/")
        time.sleep(5)  # Wait for page to load
        
        if DEBUG:
            print("[DEBUG] Successfully navigated to Facebook")
        return True
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error navigating to Facebook: {e}")
        return False

def scroll_feed(driver, duration=3):
    """Scroll the Facebook feed for specified duration"""
    try:
        if DEBUG:
            print(f"[DEBUG] Scrolling feed for {duration} seconds...")
        
        end_time = time.time() + duration
        while time.time() < end_time:
            driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(0.5)
        
        if DEBUG:
            print("[DEBUG] Feed scrolling completed")
        return True
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error scrolling feed: {e}")
        return False

def get_group_links():
    """Read group links from CSV file"""
    try:
        if not os.path.exists(GROUP_LINKS_FILE):
            if DEBUG:
                print(f"[DEBUG] Group links file {GROUP_LINKS_FILE} not found")
            return []
        
        group_links = []
        with open(GROUP_LINKS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip():  # Skip empty rows
                    link = row[0].strip()
                    if link.startswith('http'):
                        group_links.append(link)
        
        if DEBUG:
            print(f"[DEBUG] Loaded {len(group_links)} group links")
        return group_links
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error reading group links: {e}")
        return []

def get_message_template():
    """Read message template from file"""
    try:
        if not os.path.exists(MESSAGE_FILE):
            if DEBUG:
                print(f"[DEBUG] Message file {MESSAGE_FILE} not found")
            return "Hello! Hope you're having a great day!"
        
        with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
            message = f.read().strip()
        
        if DEBUG:
            print(f"[DEBUG] Loaded message template: {message[:50]}...")
        return message
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error reading message file: {e}")
        return "Hello! Hope you're having a great day!"

def get_current_user_name(driver):
    """Get the name of the currently logged-in user"""
    try:
        # Try multiple selectors for user name
        name_selectors = [
            "//div[@role='banner']//span[contains(@class, 'x1heor9g')]",
            "//div[@role='banner']//a[@role='link']//span",
            "//div[@aria-label='Account']//span",
            "//div[@role='button']//span[contains(text(), ' ')]"
        ]
        
        for selector in name_selectors:
            try:
                name_element = driver.find_element(By.XPATH, selector)
                if name_element and name_element.text.strip():
                    name = name_element.text.strip()
                    if len(name) > 2 and ' ' in name:  # Basic validation
                        if DEBUG:
                            print(f"[DEBUG] Found user name: {name}")
                        return name
            except:
                continue
        
        if DEBUG:
            print("[DEBUG] Could not find user name, using default")
        return "User"
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error getting user name: {e}")
        return "User"

def get_group_members(driver, max_members=all):
    """Get first N members from current group"""
    try:
        if DEBUG:
            print(f"[DEBUG] Getting first {max_members} group members...")
        
        members = []
        
        # Look for members section - try different approaches
        try:
            # Method 1: Look for "Members" text and find nearby links
            members_section = driver.find_element(By.XPATH, "//span[contains(text(), 'Members') or contains(text(), 'members')]")
            driver.execute_script("arguments[0].scrollIntoView();", members_section)
            time.sleep(2)
        except:
            pass
        
        # Method 2: Look for profile links in the group
        member_selectors = [
            "//div[@role='article']//a[@role='link'][contains(@href, '/user/')]",
            "//div[@role='article']//a[contains(@href, '/profile.php')]",
            "//a[contains(@href, '/user/') or contains(@href, '/profile.php')]",
            "//div//a[@role='link'][contains(@aria-label, 'profile')]"
        ]
        
        for selector in member_selectors:
            try:
                member_elements = driver.find_elements(By.XPATH, selector)
                for element in member_elements[:max_members]:
                    try:
                        profile_url = element.get_attribute('href')
                        
                        # Extract name - try different methods
                        name = None
                        try:
                            name = element.get_attribute('aria-label')
                            if not name:
                                name = element.text.strip()
                            if not name:
                                name_span = element.find_element(By.TAG_NAME, "span")
                                name = name_span.text.strip()
                        except:
                            name = "Unknown User"
                        
                        if profile_url and name and len(members) < max_members:
                            # Clean up the name
                            if name.startswith('Profile picture of '):
                                name = name.replace('Profile picture of ', '')
                            
                            members.append({
                                'name': name,
                                'url': profile_url
                            })
                            
                    except Exception as e:
                        if DEBUG:
                            print(f"[DEBUG] Error processing member element: {e}")
                        continue
                        
                if len(members) >= max_members:
                    break
                    
            except Exception as e:
                if DEBUG:
                    print(f"[DEBUG] Error with selector {selector}: {e}")
                continue
        
        if DEBUG:
            print(f"[DEBUG] Found {len(members)} members")
            for i, member in enumerate(members):
                print(f"[DEBUG] Member {i+1}: {member['name']}")
        
        return members[:max_members]
        
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error getting group members: {e}")
        return []

def send_message_to_member(driver, member, message, current_user_name):
    """Send message to a specific group member"""
    try:
        if DEBUG:
            print(f"[DEBUG] Attempting to send message to {member['name']}...")
        
        # Navigate to member's profile
        driver.get(member['url'])
        time.sleep(5)
        
        # Look for message button - try multiple selectors
        message_button_selectors = [
            "//div[@role='button'][contains(text(), 'Message')]",
            "//a[contains(@href, '/messages/t/') or contains(text(), 'Message')]",
            "//div[@role='button']//span[contains(text(), 'Message')]",
            "//button[contains(text(), 'Message')]"
        ]
        
        message_button = None
        for selector in message_button_selectors:
            try:
                message_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                break
            except:
                continue
        
        if not message_button:
            if DEBUG:
                print(f"[DEBUG] Message button not found for {member['name']} - profile may be restricted")
            return False
        
        # Click message button
        message_button.click()
        time.sleep(3)
        
        # Find message input field
        message_input_selectors = [
            "//div[@role='textbox'][@contenteditable='true']",
            "//div[@data-text='true'][@contenteditable='true']",
            "//div[@contenteditable='true'][contains(@aria-label, 'message')]",
            "//textarea[@placeholder]"
        ]
        
        message_input = None
        for selector in message_input_selectors:
            try:
                message_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                break
            except:
                continue
        
        if not message_input:
            if DEBUG:
                print(f"[DEBUG] Message input not found for {member['name']}")
            return False
        
        # Prepare personalized message
        personalized_message = f"Hi {member['name']},\n\n{message}\n\nBest regards,\n{current_user_name}"
        
        # Type the message
        message_input.click()
        message_input.clear()
        message_input.send_keys(personalized_message)
        time.sleep(2)
        
        # Send the message
        send_button_selectors = [
            "//div[@role='button'][contains(@aria-label, 'Send')]",
            "//button[contains(@aria-label, 'Send')]",
            "//div[@role='button']//span[contains(text(), 'Send')]"
        ]
        
        for selector in send_button_selectors:
            try:
                send_button = driver.find_element(By.XPATH, selector)
                if send_button.is_enabled():
                    send_button.click()
                    time.sleep(MESSAGE_SEND_DELAY)
                    if DEBUG:
                        print(f"[DEBUG] Message sent to {member['name']}")
                    return True
            except:
                continue
        
        # Alternative: try Enter key
        try:
            message_input.send_keys(Keys.RETURN)
            time.sleep(MESSAGE_SEND_DELAY)
            if DEBUG:
                print(f"[DEBUG] Message sent to {member['name']} (using Enter key)")
            return True
        except:
            pass
        
        if DEBUG:
            print(f"[DEBUG] Could not send message to {member['name']}")
        return False
        
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error sending message to {member['name']}: {e}")
        return False

def log_result(log_file, group_url, member_name, member_url, status, message=""):
    """Log messaging results to CSV file"""
    try:
        file_exists = os.path.exists(log_file)
        
        with open(log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header if file is new
            if not file_exists:
                writer.writerow(['Timestamp', 'Group_URL', 'Member_Name', 'Member_URL', 'Status', 'Message'])
            
            # Write log entry
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, group_url, member_name, member_url, status, message])
        
        if DEBUG:
            print(f"[DEBUG] Logged result: {member_name} - {status}")
        return True
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error logging result: {e}")
        return False

def process_groups(driver):
    """Main function to process all groups and send messages"""
    try:
        # Get required data
        group_links = get_group_links()
        if not group_links:
            print("[ERROR] No group links found in grouplinks.csv")
            return False
        
        message_template = get_message_template()
        current_user_name = get_current_user_name(driver)
        
        print(f"[INFO] Processing {len(group_links)} groups...")
        print(f"[INFO] Current user: {current_user_name}")
        print(f"[INFO] Message template loaded: {len(message_template)} characters")
        
        # Process each group
        for i, group_url in enumerate(group_links, 1):
            print(f"\n[INFO] Processing group {i}/{len(group_links)}: {group_url}")
            
            try:
                # Navigate to group
                driver.get(group_url)
                time.sleep(GROUP_LOAD_DELAY)
                
                # Get group members
                members = get_group_members(driver, MEMBERS_PER_GROUP)
                if not members:
                    print(f"[WARNING] No members found in group: {group_url}")
                    continue
                
                print(f"[INFO] Found {len(members)} members to message")
                
                # Send messages to members
                for j, member in enumerate(members, 1):
                    print(f"[INFO] Messaging member {j}/{len(members)}: {member['name']}")
                    
                    try:
                        # Send message
                        if send_message_to_member(driver, member, message_template, current_user_name):
                            print(f"✅ Message sent to {member['name']}")
                            log_result(LOG_FILE, group_url, member['name'], member['url'], 'sent', message_template)
                        else:
                            print(f"⚠️ Failed to send message to {member['name']} (possibly restricted)")
                            log_result(RESTRICTED_LOG_FILE, group_url, member['name'], member['url'], 'restricted', 'Cannot send message')
                        
                        # Random delay between messages
                        if j < len(members):  # Don't delay after last member
                            delay = random.uniform(MIN_DELAY, MAX_DELAY)
                            print(f"[INFO] Waiting {delay:.1f} seconds before next message...")
                            time.sleep(delay)
                            
                    except Exception as e:
                        print(f"[ERROR] Error messaging {member['name']}: {e}")
                        log_result(RESTRICTED_LOG_FILE, group_url, member['name'], member['url'], 'error', str(e))
                        continue
                
                print(f"[INFO] Completed group {i}/{len(group_links)}")
                
                # Delay between groups
                if i < len(group_links):
                    print("[INFO] Moving to next group...")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"[ERROR] Error processing group {group_url}: {e}")
                continue
        
        print(f"\n[INFO] All groups processed successfully!")
        print(f"[INFO] Check {LOG_FILE} for successful messages")
        print(f"[INFO] Check {RESTRICTED_LOG_FILE} for restricted profiles")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error in process_groups: {e}")
        return False
