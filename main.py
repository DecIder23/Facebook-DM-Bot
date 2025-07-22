import time
import random
from functions import *
from config import *

def main():
    """Main function to initialize Facebook bot and handle login"""
    driver = None
    try:
        # Initialize Chrome driver
        print("[INFO] Initializing browser...")
        driver = initialize_driver()
        
        # Navigate to Facebook
        print("[INFO] Loading Facebook...")
        if not navigate_to_facebook(driver):
            print("[ERROR] Failed to load Facebook. Exiting.")
            return
        
        # Check if already logged in
        if is_logged_in(driver):
            print("[INFO] Already logged in!")
        else:
            print("[INFO] Not logged in. Trying cookies...")
            
            # Try to login with cookies
            if load_cookies(driver):
                print("[INFO] Successfully logged in with cookies!")
            else:
                print("[INFO] Cookies failed. Logging in with credentials...")
                
                # Try to login with credentials
                if login_with_credentials(driver):
                    print("[INFO] Successfully logged in with credentials!")
                    # Save cookies for future use
                    save_cookies(driver)
                    print("[INFO] Cookies saved for future sessions.")
                else:
                    print("[ERROR] Login failed. Please check your credentials in config.py")
                    return
        
        # Login successful - scroll feed for a few seconds
        print("[INFO] Login completed successfully!")
        print("[INFO] Scrolling feed...")
        scroll_feed(driver, SCROLL_DURATION)
        
        # Start group processing
        print("[INFO] Starting group messaging process...")
        if process_groups(driver):
            print("[INFO] Group messaging completed successfully!")
        else:
            print("[ERROR] Group messaging process failed.")
        
        # Keep browser open for manual inspection
        input("\nPress ENTER to close the browser...")
        
    except KeyboardInterrupt:
        print("\n[INFO] Bot interrupted by user.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        if driver:
            print("[INFO] Closing browser...")
            input("enter to close the browser...")
            driver.quit()

if __name__ == "__main__":
    main()