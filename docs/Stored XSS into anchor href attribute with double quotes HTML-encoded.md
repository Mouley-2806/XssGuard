Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded

Input field:
Website field

Initial test input:
TEST123.com

Payload:
javascript:alert(1)

Vulnerable sink:
<a id="author" href="USER_INPUT">...</a>

Observed sink:
<a id="author" href="TEST123.com">vbhj</a>

XSS context:
href attribute of an anchor (<a>) element

Why it is vulnerable:
The Website input is stored and later inserted into the href attribute without preventing a JavaScript URL.

Result:
The stored JavaScript URL can execute when the author link is activated.