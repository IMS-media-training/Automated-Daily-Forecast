# My Development Journal: IMS Weather Story Automation

**Last Updated:** November 10, 2025
**Project Status:** Phase 4 Complete, with some cool new features! ✅

---

## 🎯 Project Overview

### My Goal

To build an automated Python script that:

1.  Downloads the daily weather forecast XML from the Israel Meteorological Service (IMS).
2.  Parses the forecast data for 15 Israeli cities.
3.  Generates a beautifully designed Instagram story image (1080x1920px).
4.  Emails the image to my social media manager.
5.  Runs automatically every morning at 6:00 AM.

### My Background

-   **Who I am:** A designer on the IMS Social Media & Design Team, learning Python to automate some of our work.
-   **The Big Picture:** Get this running on the IMS servers after the CEO signs off.
-   **How I'm doing it:** Taking it one step at a time, building and learning as I go.

---

## 📋 My Project Journey (The Phases)

### Phase 1: Conquering the XML ✅ COMPLETE

**My Goal:** Figure out how to get the weather data out of that tricky XML file.

**Status:** Nailed it on October 16, 2025!

**What I did:**

-   [x] Got Python 3.13.2 and VS Code all set up.
-   [x] Wrestled with the XML file to get the Hebrew text to show up correctly (UTF-8 for the win!).
-   [x] Learned how to parse the XML and pull out the city data (name, coordinates, temps, weather code).
-   [x] Figured out how to filter the data for a specific date.
-   [x] Sorted the cities by latitude, from north to south.

**And then I made it production-ready:**

-   [x] Built scripts to automatically download the XML from the IMS website.
-   [x] Made an archive system to keep the last 14 days of XML files, just in case.
-   [x] Added a ton of error handling and logging to make it robust.
-   [x] Created a main workflow script to run everything in order.
-   [x] Added a `--dry-run` mode so I can test without messing anything up.

**Achievement:** I built a fully automated system that downloads, extracts, and validates the weather data. I was so proud of this!

### Phase 2: Making it Pretty (The Single City POC) ✅ COMPLETE

**My Goal:** Create a proof-of-concept image with just one city to see if I could make it look good.

**Status:** Done and looking sharp on October 16, 2025!

**What I did:**

-   [x] Dove into the Pillow library to create the image.
-   [x] Got the Fredoka variable font to work with Hebrew text.
-   [x] Created the 1080x1920px Instagram story canvas.
-   [x] Rendered the Tel Aviv forecast with a weather icon, temperature, and the city name in Hebrew.
-   [x] Used some cool Twemoji PNGs for the weather icons.
-   [x] Designed a professional-looking header with a logo placeholder and the date.
-   [x] Added a nice white-to-sky-blue gradient background.

**Achievement:** I proved I could generate a professional-looking image with all the right design elements. This was a huge confidence booster!

### Phase 3: The Full Monty (All 15 Cities) ✅ COMPLETE

**My Goal:** Generate a single image with the forecast for all 15 cities.

**Status:** Mission accomplished on October 30, 2025!

**What I did:**

-   [x] Created a vertical layout to display all 15 cities, sorted from north to south.
-   [x] Added the weather icon, temperature, and Hebrew city name for each city.
-   [x] Switched to the Open Sans variable font, which looks even better.
-   [x] Made sure everything was perfectly centered and aligned.
-   [x] Built the final, production-ready script: `generate_forecast_image.py`.

### Phase 3.5: The Icon Quest ✅ COMPLETE

**My Goal:** Find a complete set of weather icons to cover all the IMS weather codes.

**Status:** Done on November 3, 2025!

**What I did:**

-   [x] Dug through the IMS documentation (a Hebrew PDF!) and created a JSON file of all the weather codes.
-   [x] Found the awesome Twemoji icon set, which had everything I needed.
-   [x] Mapped all 23 IMS weather codes to the 11 unique icons.
-   [x] Made sure to give proper credit for the icons (CC-BY 4.0).

### Phase 4: Taking it to the Cloud (Automation & Email) ✅ COMPLETE

**My Goal:** Get the script to run automatically every day and email the image to my manager.

**Status:** It's alive! Completed on November 5, 2025.

**What I did:**

-   [x] Learned how to use GitHub Actions to run my script on a schedule.
-   [x] Set it up to run every morning at 6:00 AM Israel time.
-   [x] Figured out how to send emails with Python's `smtplib`.
-   [x] Created a nice HTML email template for the forecast.
-   [x] Used GitHub Secrets to keep my email credentials safe.

**Achievement:** The entire process is now fully automated! I still can't believe I built something that runs in the cloud all by itself.

### The Latest Cool Stuff (Recent Enhancements)

**Status:** Added on November 10, 2025.

**What I did:**

-   [x] **Daily Random Gradients:** I thought the background was a bit boring, so now it generates a new random gradient every day!
-   [x] **Gradient Test Mode:** I added a script (`test_gradients.py`) to quickly see what the different gradients look like.
-   [x] **Accessibility Fix:** The adaptive separator lines I tried didn't look great, so I changed them to solid black for better readability.
-   [x] **Smarter Dry-Run:** I improved the `--dry-run` mode so I can test the image generation without needing to have my email credentials set up.

---

## 💡 My Learning Points & Progress

### Skills I've Picked Up

-   Python programming (I'm getting pretty good at this!)
-   XML parsing with ElementTree
-   Image generation with Pillow
-   Working with fonts and Hebrew text
-   Sending emails with Python
-   Automating scripts with GitHub Actions
-   Managing secrets and environment variables

### Challenges I've Overcome

-   **Hebrew Encoding:** That was a tough one, but I finally cracked it.
-   **XML Parsing:** The IMS XML file is a bit of a maze, but I found my way through it.
-   **Email Authentication:** Getting the SMTP login to work with app passwords was a journey.
-   **GitHub Actions:** Learning how to set up the workflow and manage secrets was a big step.

---

## 📝 Notes for What's Next

### Phase 5: The Final Frontier (Server Deployment)

-   Test the script on a Linux server.
-   Write a deployment guide for the IT team.
-   Hand over the project for production deployment.

---

## 📧 Contact & Support

If I get stuck, I'll:

1.  Ask my AI assistant for help.
2.  Check the Python documentation.
3.  Talk to the IMS IT team about server stuff.

---

## End of Journal