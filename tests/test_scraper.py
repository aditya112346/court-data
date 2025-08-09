from scraper import parse_case_html

SAMPLE_HTML = '''
<html><body>
<table class="case-details">
<tr><th>Petitioner</th><td>John Doe</td></tr>
<tr><th>Respondent</th><td>State</td></tr>
<tr><th>Filing Date</th><td>01-02-2023</td></tr>
</table>
<a href="/judgments/2023/order1.pdf">Judgment dated 01-02-2023</a>
</body></html>
'''

def test_parse_basic():
    parsed = parse_case_html(SAMPLE_HTML)
    assert parsed['petitioner'] == 'John Doe'
    assert parsed['respondent'] == 'State'
    assert parsed['filing_date'] == '01-02-2023'
    assert len(parsed['orders']) >= 1
