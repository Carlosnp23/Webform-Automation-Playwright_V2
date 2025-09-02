from playwright.sync_api import sync_playwright
import mysql.connector
import time
import os
import db_config  # Database configuration

# ---------- Initialize users list ----------
users = []

# ---------- Connect to the database ----------
try:
    conn = mysql.connector.connect(
        host=db_config.host,
        port=db_config.port,
        user=db_config.user,
        password=db_config.password,
        database=db_config.database,
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch all users from the correct table
    cursor.execute(
        """
        SELECT 
            First_Name, Last_Name, Email, Gender, Date_of_Birth, 
            Mobile, Subjects, Hobbies, Picture, Current_Address, State_and_City
        FROM users_v2;
    """
    )
    users = cursor.fetchall()
    print(f"{len(users)} record(s) obtained from the database")

except mysql.connector.Error as err:
    print(f"Database connection error: {err}")

finally:
    if "conn" in locals() and conn.is_connected():
        conn.close()

# ---------- Image path ----------
image_path = os.path.join(
    "S:\\Projects\\Python\\Webform-Automation-Playwright v2", "profile.png"
)

# ---------- Start browser automation ----------
playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)

try:
    page = browser.new_page()
    page.goto(
        "https://demoqa.com/automation-practice-form",
        timeout=60000,
        wait_until="domcontentloaded",
    )

    for u in users:
        # ---------- Fill basic information ----------
        page.wait_for_selector("input[id='firstName']", state="visible")
        page.fill("input[id='firstName']", u["First_Name"])
        page.fill("input[id='lastName']", u["Last_Name"])
        page.fill("input[id='userEmail']", u["Email"])

        # ---------- Fill mobile number ----------
        if u.get("Mobile"):
            page.fill("#userNumber", u["Mobile"])

        # ---------- Select gender ----------
        gender = u["Gender"].lower()
        if gender == "male":
            page.click("label[for='gender-radio-1']")
        elif gender == "female":
            page.click("label[for='gender-radio-2']")
        else:
            page.click("label[for='gender-radio-3']")

        # ---------- Fill date of birth ----------
        if u["Date_of_Birth"]:
            dob_str = u["Date_of_Birth"].strftime("%d %b %Y")
            page.click("#dateOfBirthInput")
            page.fill("#dateOfBirthInput", dob_str)
            page.keyboard.press("Enter")
            page.wait_for_timeout(200)  # wait a bit after entering DOB

        # ---------- Fill subjects ----------
        if u["Subjects"]:
            subjects = [s.strip() for s in u["Subjects"].split(",") if s.strip()]
            for subject in subjects:
                input_subject = page.locator("#subjectsInput")
                input_subject.click()
                input_subject.type(subject, delay=100)
                page.keyboard.press("Enter")
                page.wait_for_timeout(200)

        # ---------- Select hobbies ----------
        if u["Hobbies"]:
            hobbies = [h.strip().lower() for h in u["Hobbies"].split(",")]
            if "sports" in hobbies:
                page.click("label[for='hobbies-checkbox-1']")
            if "reading" in hobbies:
                page.click("label[for='hobbies-checkbox-2']")
            if "music" in hobbies:
                page.click("label[for='hobbies-checkbox-3']")

        # ---------- Upload picture ----------
        if os.path.exists(image_path):
            page.set_input_files("#uploadPicture", image_path)

        # ---------- Fill current address ----------
        if u["Current_Address"]:
            current_address_input = page.locator("#currentAddress")
            current_address_input.click()
            current_address_input.fill("")  # clear before typing
            current_address_input.type(u["Current_Address"], delay=50)
            page.wait_for_timeout(200)

        # ---------- Select state and city safely (City, State from DB) ----------
        if u["State_and_City"]:
            state_city = u["State_and_City"].split(",")
            if len(state_city) == 2:
                city, state = state_city[0].strip(), state_city[1].strip()

                # ---------- Select state ----------
                state_dropdown = page.locator("#state")
                state_dropdown.scroll_into_view_if_needed()
                state_dropdown.click()
                page.wait_for_selector(
                    f"div[id^='react-select'][id*='option']:has-text('{state}')", timeout=5000
                )
                page.locator(
                    f"div[id^='react-select'][id*='option']:has-text('{state}')"
                ).click()
                page.wait_for_timeout(200)

                # ---------- Select city ----------
                city_dropdown = page.locator("#city")
                city_dropdown.scroll_into_view_if_needed()
                city_dropdown.click()
                page.wait_for_selector(
                    f"div[id^='react-select'][id*='option']:has-text('{city}')", timeout=5000
                )
                page.locator(
                    f"div[id^='react-select'][id*='option']:has-text('{city}')"
                ).click()
                page.wait_for_timeout(200)

        # ---------- Submit form at the end ----------
        page.wait_for_timeout(500)  # small wait to ensure all fields are filled
        page.click("#submit")

        # ---------- Wait and close the modal ----------
        page.wait_for_selector(
            "#example-modal-sizes-title-lg", state="visible", timeout=5000
        )
        page.click("#closeLargeModal")
        time.sleep(1)

    input("Forms submitted. Press Enter to close the browser...")

finally:
    browser.close()
    playwright.stop()
