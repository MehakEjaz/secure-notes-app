from markupsafe import escape
# -----------------------------------
# Vulnerable Render Function
# -----------------------------------
def vulnerable_render(note):
    # Simulates vulnerable Flask output
    return f"Note Saved: {note}"
# -----------------------------------
# Secure Render Function
# -----------------------------------
def secure_render(note):

    # Escapes dangerous HTML
    safe_note = escape(note)

    return f"Note Saved: {safe_note}"
# -----------------------------------
# XSS Payloads
# -----------------------------------
payloads = [

    "<script>alert('XSS')</script>",

    "<img src=x onerror=alert('XSS')>",

    "<svg onload=alert('XSS')>",

    "<body onload=alert('XSS')>"
]
# -----------------------------------
# Vulnerable XSS Test
# -----------------------------------
def test_xss_vulnerable():

    for payload in payloads:

        response = vulnerable_render(payload)

        # Malicious script should appear directly
        assert payload in response
# -----------------------------------
# Secure XSS Test
# -----------------------------------
def test_xss_fixed():

    for payload in payloads:

        response = secure_render(payload)
        # Raw payload should NOT appear
        assert payload not in response
        # Escaped version SHOULD appear
        assert str(escape(payload)) in response
