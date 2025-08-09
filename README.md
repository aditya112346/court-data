# Court Case Fetcher

## Court Chosen
This project scrapes case details from the **Delhi High Court eCourts portal**:  
https://delhihighcourt.nic.in/web/

## Setup Steps

### Prerequisites
- Python 3.10 / 3.11 / 3.12 recommended
- Virtual environment via `venv` or `conda` is recommended
- Internet connection is required

### Installation
1. Clone the repository:

        git clone https://github.com/aditya112346/court-case-fetcher
        cd court-case-fetcher

2. Create and activate a virtual environment:

        python -m venv venv
    
3. Install dependencies:

        pip install -r requirements.txt

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Update values if needed

5. Initialize the database:

        python db_init.py

6. Run the application:

        python app.py

7. Open your browser and go to:  
`http://localhost:5000/`

## CAPTCHA Strategy

Currently, the Delhi High Court portal typically does not present CAPTCHA for most requests.  
If CAPTCHA or scraping restrictions arise, you can enable **Playwright**, which uses a headless browser to fetch pages mimicking a real user.

To enable Playwright:
- In `.env`, set:

        
        ENABLE_PLAYWRIGHT=1

- Install Playwright:
 
        pip install playwright
        playwright install

- Restart the app.

For complex CAPTCHAs, manual solving or paid third-party CAPTCHA solvers would be required (not implemented in this version).

## Environment Variables

- `FLASK_APP` – Flask entry point (default: `app.py`)
- `FLASK_ENV` – `development` or `production`
- `DATABASE_URL` – SQLAlchemy DB connection string (default: SQLite)
- `ENABLE_PLAYWRIGHT` – `0` or `1` (disable/enable Playwright)
- `LOG_RESPONSE_BYTES` – Maximum raw HTML bytes to store in DB (default: 200000)

## Sample Usage

- On the homepage, enter:  
- **Case Type**: e.g., `W.P.(CRL)`, `BAIL APPLN.`, `CIVIL`, `CRIMINAL` (You can enter any case type as free text)  
- **Case Number**: e.g., `1804`  
- **Filing Year**: e.g., `2025`  
- Submit the form — if the case exists on the portal, you will see:  
- Petitioner & Respondent  
- Filing date & Next hearing date  
- Orders and Judgments (with PDF download/open links)

## Troubleshooting

- If you get connection errors or timeouts, check if you can open the Delhi High Court portal directly in your browser.
- The site may be down or blocking automated requests.
- Try enabling Playwright for more reliable scraping.
- Use Python 3.10–3.12. Python 3.13 is not fully supported by some dependencies yet.
- For DB errors, rerun: `python db_init.py`


---

## License

This repository is released under the **MIT License**. Please provide credit if you use this code.

---

## Contact

If you face issues or want to request features, please open an **Issue** in the GitHub repository.

---

**Thank you for using Court Case Fetcher!**
