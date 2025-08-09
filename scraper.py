import os
import re
import time
from bs4 import BeautifulSoup
import requests

USE_PLAYWRIGHT = os.getenv('ENABLE_PLAYWRIGHT', '0') == '1'

DELHI_HC_BASE = 'https://delhihighcourt.nic.in'
SEARCH_ENDPOINT = DELHI_HC_BASE + '/app/get-case-type-status'  # Example endpoint, adjust if needed

HEADERS = {
    'User-Agent': 'CourtDataFetcher/1.0 (+https://github.com/aditya112346/court-data-fetcher)'
}

def fetch_case_html(case_type: str, case_number: str, filing_year: str) -> tuple[str, str]:
    # NOTE: Delhi HC parameters might differ, confirm by inspecting their search page.
    # Using GET for example purposes; change to POST if necessary.
    params = {
        'caseNumber': case_number,
        'year': filing_year,
        'caseType': case_type
    }
    try:
        resp = requests.get(SEARCH_ENDPOINT, params=params, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        return resp.url, resp.text
    except Exception as e:
        if USE_PLAYWRIGHT:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(user_agent=HEADERS['User-Agent'])
                # Construct URL or fill form manually here if needed
                query_url = f"{DELHI_HC_BASE}/app/case-number?caseNumber={case_number}&year={filing_year}&caseType={case_type}"
                page.goto(query_url, timeout=30000)
                time.sleep(1)
                html = page.content()
                browser.close()
                return query_url, html
        else:
            raise

def parse_case_html(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')

    result = {
        'petitioner': None,
        'respondent': None,
        'filing_date': None,
        'next_hearing': None,
        'orders': []
    }

    # Delhi HC might have different class names / table structure — adjust accordingly
    # Trying to find likely case details table(s)
    tables = soup.find_all('table', class_=re.compile(r'case-details|caseinfo|table', re.I))

    for table in tables:
        for row in table.find_all('tr'):
            cols = [c.get_text(strip=True) for c in row.find_all(['th','td'])]
            if not cols:
                continue
            line = ' '.join(cols).lower()

            if 'petitioner' in line and not result['petitioner']:
                result['petitioner'] = cols[-1]
            elif 'respondent' in line and not result['respondent']:
                result['respondent'] = cols[-1]
            elif ('filing date' in line or 'date of filing' in line) and not result['filing_date']:
                result['filing_date'] = cols[-1]
            elif ('next hearing' in line or 'next date' in line) and not result['next_hearing']:
                result['next_hearing'] = cols[-1]

    # Extract orders/judgments PDFs or links
    for a in soup.find_all('a', href=True):
        href = a['href']
        href_lower = href.lower()
        if href_lower.endswith('.pdf') or 'judgment' in href_lower or 'order' in href_lower:
            title = a.get_text(strip=True) or 'Order/Judgment'
            if href.startswith('/'):
                href = DELHI_HC_BASE + href
            result['orders'].append({'title': title, 'url': href})

    return result