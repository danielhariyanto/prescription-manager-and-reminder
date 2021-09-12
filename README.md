# Prescription Manager and Reminder

DEMO: <a>https://drremindermedhacks.herokuapp.com/</a>


With increasing age, comes an increasing number of health issues…and with an increasing number of health issues, comes a growing list of medical prescriptions…With cognitive decline, this list becomes difficult for the older population to keep track and remind themselves of which medicines to take. Not only is the correct medicine important, but the time and frequency at which they are consumed plays a critical role as well. To tackle this everyday problem that can have significant effect on people’s health, we created Dr. Reminder. 


Dr. Reminder is a web app that helps users to manage all of their prescriptions in one place through a few clicks. The app analyzes a photo of the user’s prescription label and automatically creates a calendar to remind the user when to consume the right medicine. Dr. Reminder takes one step further in aiding people by including family and friends in the process. Every Dr. Reminder session created by the user will have a shareable link so users can share it with their contacts. This is extemely helpful for users who are not the most tech saavy as loved ones can help them input their prescriptions and set up Dr. Reminder for the elderly.


IMPORTANT!!!
- You can only upload images <1 MB (because we used the free version of an API).
- If you get an error after uploading images, it's because the images are not high quality enough.
- Another reason: it's because the free version allows a max of 25,000 requests a month and we've probably already used up all the requests.


IMPROVEMENTS
- Improve frontend because it only looks good on desktops right now. Will need to optimize for mobile phones.
- Improve NLP algorithm that parses through OCR-scanned prescription to create intake routine (right now it's hard coded).
- Improve OCR capabilities using a better OCR API without limitations.