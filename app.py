import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from dotenv import load_dotenv
from scraper import fetch_case_html, parse_case_html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import QueryLog, Base
from io import BytesIO
import requests

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL','sqlite:///courtdata.db')
LOG_BYTES = int(os.getenv('LOG_RESPONSE_BYTES','200000'))

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET','dev-secret-change')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {})
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

@app.route('/', methods=['GET'])
def index():
    # Removed fixed list, now allowing user to enter any case type text
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    case_type = request.form.get('case_type', '').strip()
    case_number = request.form.get('case_number', '').strip()
    filing_year = request.form.get('filing_year', '').strip()

    if not (case_type and case_number and filing_year):
        flash('Please provide Case Type, Case Number and Filing Year')
        return redirect(url_for('index'))

    try:
        url, html = fetch_case_html(case_type, case_number, filing_year)
    except Exception as e:
        flash(f'Failed to fetch from court portal: {e}')
        return redirect(url_for('index'))

    parsed = parse_case_html(html)

    session = Session()
    raw_to_save = (html[:LOG_BYTES]) if html else ''
    q = QueryLog(case_type=case_type, case_number=case_number, filing_year=filing_year,
                 raw_response=raw_to_save, parsed_json=json.dumps(parsed))
    session.add(q)
    session.commit()

    return render_template('result.html', parsed=parsed,
                           query={'case_type': case_type, 'case_number': case_number, 'filing_year': filing_year},
                           source_url=url)

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        flash('No URL provided')
        return redirect(url_for('index'))
    try:
        r = requests.get(url, stream=True, timeout=20)
        r.raise_for_status()
        bio = BytesIO(r.content)
        filename = url.split('/')[-1][:200]
        return send_file(bio, download_name=filename, as_attachment=True)
    except Exception as e:
        flash(f'Failed to download PDF: {e}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
