PortSwigger Reflected XSS Lab — Complete Revision Report
Lab Name
Reflected XSS into HTML context with most tags and attributes blocked
The purpose of this lab is to exploit a reflected XSS vulnerability even though the application blocks most normal HTML tags and event attributes.
The goal is to make the application execute:
print()
The lab must be solved without the victim manually interacting with the page. PortSwigger's official solution confirms this requirement.
1. What is XSS?
XSS means:
Cross-Site Scripting
It happens when a website takes something controlled by the user and puts it into an HTML page without properly preventing it from being interpreted as HTML/JavaScript.
For example, imagine a search page produces:
<h1>
    0 search results for 'TEST123'
</h1>
If the website directly inserts my input there, then instead of:
TEST123
I might try:
<script>alert(1)</script>
If the browser interprets it as HTML/JavaScript, JavaScript executes.
That is XSS.
2. What was happening in this lab?
I discovered that my search input was reflected into the page.
I tested:
TEST123
The response contained:
<h1>
    0 search results for 'TEST123'
</h1>
That was important because it proved:
My input
    ↓
Server receives it
    ↓
Server puts it into HTML response
    ↓
Browser displays it
This is called reflected XSS because the input is reflected from the request into the response.
PortSwigger describes reflected XSS as a situation where the application receives data in an HTTP request and includes it unsafely in the response.
3. First thing I tried
A normal XSS payload is:
<img src=1 onerror=print()>
Understanding it:
<img src=1>
tries to load an image.
Because 1 isn't a valid image URL, the image fails.
Then:
onerror=print()
means:
When the image fails, execute print().
So:
image fails
    ↓
onerror happens
    ↓
print() runs
But the lab blocks the <img> tag.
Therefore, the normal payload doesn't work.
PortSwigger specifically uses this payload as the starting point for this lab.
4. Why couldn't I just use ?
I also tried things like:
<script>alert(1)</script>
and:
<h1>TEST</h1>
and:
<svg>TEST</svg>
The application blocks many HTML tags.
So the problem isn't:
"Can I inject HTML?"
The real problem is:
"Which HTML tags are still allowed?"
I don't want to guess forever.
That's why I use Burp Intruder.
5. What is Burp Intruder?
Burp Intruder is useful when I want to test many possibilities automatically.
Instead of manually trying:
<img>
<body>
<div>
<form>
svg
...
I can tell Burp:
Try every tag from this list and tell me what happens.
This is called enumerating the allowed tags.
PortSwigger's documentation specifically recommends using Burp Intruder to enumerate which tags and attributes are permitted by an XSS filter.
6. Getting the request into Burp
I used Burp's browser.
The basic flow was:
Burp
 ↓
Proxy
 ↓
Open Browser
 ↓
Open the current PortSwigger lab
 ↓
Search for TEST123
 ↓
Proxy → HTTP history
 ↓
Find:
GET /?search=TEST123
Then:
Right click request
        ↓
Send to Intruder
Important:
The lab URL changes because PortSwigger gives each lab instance its own ID.
So always use the current URL shown by ymy lab, not an old URL from a previous attempt.
7. Intruder — finding the allowed HTML tag
The first Intruder request was changed to:
GET /?search=<> HTTP/2
The important idea was:
<>
I wanted Burp to test things such as:
<body>
<img>
<div>
<form>
...
automatically.
8. What is § in Burp?
The § symbol is Burp's way of saying:
"This is the part I want to replace during the attack."
I do not need to type § on the keyboard.
Burp creates it using the:
Add §
button.
I wanted:
<§§>
This means:
<
PAYLOAD GOES HERE
>
For example, if Burp uses:
body
the request becomes:
<body>
If it uses:
img
it becomes:
<img>
9. Why I used the XSS Cheat Sheet
PortSwigger provides an XSS Cheat Sheet containing many HTML tags and event handlers.
Current cheat sheet:
PortSwigger XSS Cheat Sheet
It has buttons such as:
Copy tags to clipboard
Copy events to clipboard
Copy payloads to clipboard
I used:
Copy tags to clipboard
for the first Intruder attack.
The cheat sheet is regularly updated by PortSwigger.
10. First Intruder attack
My position was:
<§§>
Then:
Payloads
    ↓
Copy tags from XSS Cheat Sheet
    ↓
Paste into Burp
    ↓
Start attack
Burp tested many tags.
Most results were:
400
One important result was:
body → 200
This was the important discovery.
11. What does 400 vs 200 mean?
In this lab:
400
The application rejected that particular tag.
Example:
img → 400
script → 400
svg → 400
200
The application accepted the request.
I found:
body → 200
So I learned:
body is an allowed HTML tag.
PortSwigger's official solution confirms that most payloads produce 400 while body produces 200.
12. What did I learn?
My first attack taught me:
Allowed tag = body
So now I know I can try:
<body>
But just having:
<body>
doesn't execute JavaScript.
I need an event handler.
13. What is an event handler?
An event handler is something that runs JavaScript when a particular event happens.
Examples:
onclick=...
onload=...
onerror=...
onresize=...
onfocus=...
For example:
<body onresize=print()>
means:
When the body is resized, run print().
So my next question became:
Which event handler is allowed?
14. Second Intruder attack
I changed my payload position to:
<body §§=1>
Here:
%20
means a space.
So the human-readable version is:
<body §§=1>
The important part is that the payload goes before:
=1
PortSwigger's official lab instructions use exactly:
<body §§=1>
for the second Intruder attack.
16. Second Intruder payload list
This time I didn't use the HTML tag list.
I did:
Payloads
    ↓
Clear
    ↓
XSS Cheat Sheet
    ↓
Copy events to clipboard
    ↓
Paste into Burp
    ↓
Start attack
Now Burp tested things like:
onload
onclick
onerror
onfocus
onresize
...
17. Second Intruder results
Again, I got a mixture of:
400
and:
200
The important result was:
onresize → 200
So I discovered:
Allowed HTML tag:
body
Allowed event:
onresize
Therefore I can construct:
<body onresize=print()>
This is the key discovery of the entire lab.
PortSwigger confirms that onresize is the event that returns 200 in this lab.
18. Why doesn't solve the lab by itself?
Because onresize only runs when a resize happens.
This:
<body onresize=print()>
does NOT mean:
Run print immediately.
It means:
Run print when the body is resized.
So I need to somehow cause a resize automatically.
And I cannot depend on the victim manually resizing their browser.
The lab specifically says the solution must not require user interaction.
19. Why do I use an iframe?
An iframe allows me to load another webpage inside a page.
Basic example:
<iframe src="https://example.com">
In my attack, the iframe loads the vulnerable lab page.
The iframe also gives me something whose size I can change.
So the iframe is basically my resize trigger.
Think:
iframe
  ↓
loads vulnerable page
  ↓
iframe size changes
  ↓
resize happens
  ↓
onresize runs
  ↓
print()
20. Why do I use onload?
onload means:
Do something when the iframe has finished loading.
My iframe contains:
onload=this.style.width='100px'
When the iframe loads:
onload
   ↓
change width
   ↓
resize
So:
onload
starts the process.
While:
onresize
catches the resize.
And:
print()
proves JavaScript executed.
Easy memory trick:
onload     = START
onresize   = CATCH
print()    = PROOF
21. Final exploit structure
PortSwigger's official solution uses:
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search="><body onresize=print()>" onload=this.style.width='100px'>
This is the exact official structure.
Ymy lab ID during my work was:
0aad00a304c6846380bae5ae009b00d7
So ymy final URL conceptually contains:
https://0aad00a304c6846380bae5ae009b00d7.web-security-academy.net/
22. The final URL WITHOUT encoding
You specifically wanted the URL without encoding.
The readable version of the URL inside the iframe is:
https://0aad00a304c6846380bae5ae009b00d7.web-security-academy.net/?search="><body onresize=print()>
This is what the encoded portion represents.
Breaking it down:
https://0aad00a304c6846380bae5ae009b00d7.web-security-academy.net/
is ymy lab.
Then:
?search=
is the search parameter.
Then:
"><body onresize=print()>
is the important injection.
So conceptually:
LAB URL
   +
search=
   +
"><body onresize=print()>
24. Complete final iframe
Ymy final Exploit Server body should conceptually be:
<iframe src="https://0aad00a304c6846380bae5ae009b00d7.web-security-academy.net/?search="><body onresize=print()>" onload=this.style.width='100px'>
Notice there are TWO different things happening:
Inside src
I load the vulnerable lab:
?search=...
and inject:
"><body onresize=print()>
Outside the URL
I have:
onload=this.style.width='100px'
This causes the iframe to change width after loading.
25. Why does the " matter?
This is very important.
The application is putting my search input inside HTML.
The payload begins conceptually with:
">
The:
"
helps terminate the existing quoted context.
The:
>
helps close the existing HTML element.
Then I introduce:
<body onresize=print()>
So the browser can interpret my injected HTML.
That's why this isn't enough:
onresize=print()
I need to get the browser into a position where it interprets that as an HTML attribute.
26. Complete attack chain
This is the most important section to remember.
If you forget everything else, read this.
SEARCH INPUT
    ↓
TEST123
    ↓
Input is reflected in HTML
    ↓
Normal XSS payload is blocked
    ↓
Use Burp Intruder
    ↓
Test HTML tags
    ↓
body = 200
    ↓
body is allowed
    ↓
Test event handlers
    ↓
onresize = 200
    ↓
onresize is allowed
    ↓
Create:
<body onresize=print()>
    ↓
Need to trigger resize automatically
    ↓
Use iframe
    ↓
iframe loads vulnerable page
    ↓
iframe onload changes width
    ↓
resize happens
    ↓
body onresize runs
    ↓
print()
    ↓
LAB SOLVED
27. What each part does
body
<body>
This is the HTML tag I discovered was allowed.
onresize
onresize=...
This is the allowed event handler I discovered.
It waits for a resize.
print()
print()
This is the JavaScript function the lab wants me to execute.
It acts as proof that XSS worked.
iframe
<iframe>
This lets me load the vulnerable page and gives me something whose dimensions can be changed.
onload
onload=...
This runs after the iframe loads.
this.style.width='100px'
this.style.width='100px'
this refers to the iframe.
So this changes the iframe's width.
That creates the resize event.
28. Why I didn't use alert()
You may normally see XSS examples like:
alert(1)
But this particular lab asks you to call:
print()
So don't replace it with:
alert(1)
The intended solution specifically uses print().
29. Why I didn't use document.cookie
I discussed document.cookie earlier.
Normally:
document.cookie
reads cookies accessible to JavaScript.
But this lab isn't asking me to steal cookies.
Its goal is simply:
execute print()
So there is no need to use:
document.cookie
for this lab.
30. Why Burp was necessary
Without Burp, I would have to manually test:
<img>
<body>
<div>
<form>
...
and then:
onload
onclick
onerror
onresize
...
That could take a long time.
Burp Intruder lets me test the whole list automatically.
So the purpose of Intruder here was not:
"Hack the website."
It was:
"Find out which tags and events the filter allows."
31. What the status codes taught us
Remember:
400 = rejected
200 = accepted
First attack:
body → 200
Therefore:
body is allowed
Second attack:
onresize → 200
Therefore:
onresize is allowed
This is why the two Intruder attacks were necessary.
32. The two Intruder setups
Attack 1 — Find allowed tag
Position:
<§§>
Payloads:
HTML tags
Result:
body → 200
Attack 2 — Find allowed event
Position:
<body §§=1>
Payloads:
HTML events
Result:
onresize → 200
33. The URLs/resources used
my lab
Use the current lab URL displayed by PortSwigger because lab IDs can change.
my lab ID during this exercise was:
0aad00a304c6846380bae5ae009b00d7
Readable lab URL:
https://0aad00a304c6846380bae5ae009b00d7.web-security-academy.net/
XSS Cheat Sheet
PortSwigger XSS Cheat Sheet
Used for:
Copy tags to clipboard
and:
Copy events to clipboard
Official lab solution
Official PortSwigger Lab Solution
This is the page to revisit if you want to compare ymy solution with the official one.
PortSwigger XSS contexts
PortSwigger XSS Contexts Guide
Useful for understanding why the location of ymy input inside HTML matters.
Burp Intruder — XSS filter enumeration
PortSwigger Burp XSS Filter Enumeration Guide
Useful when you want to repeat this technique in another lab.
34. What to remember for future XSS labs
When you see:
"Most tags/attributes are blocked"
don't immediately start guessing random payloads.
Think:
1. Where is my input reflected?
2. What HTML context am I in?
3. What tags are allowed?
4. What events are allowed?
5. Can I trigger the event automatically?
For this lab:
Context:
HTML body
Allowed tag:
body
Allowed event:
onresize
Trigger:
iframe + onload
JavaScript:
print()
35. One-minute revision
If you come back after a month and remember nothing, read this:
The search input was reflected into HTML. Normal XSS tags such as script, img, h1, and svg were blocked. I used Burp Intruder to automatically test HTML tags. I placed the payload position between < and > as <§§>. The tag body returned HTTP 200, so body was allowed.
Then I tested event handlers using <body §§=1>. Most events returned 400, but onresize returned 200. Therefore the allowed XSS structure was:
<body onresize=print()>
But onresize needs a resize event. I therefore used an iframe. When the iframe loads, its onload changes its width:
onload=this.style.width='100px'
The width change causes a resize, which triggers:
<body onresize=print()>
So:
iframe loads
→ onload
→ width changes
→ resize
→ onresize
→ print()
The final exploit is:
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search="><body onresize=print()>" onload=this.style.width='100px'>
Replace YOUR-LAB-ID with the current lab ID.
36. The three things to memorize
You do not need to memorize the entire final payload.
Memorize these three discoveries:
1. body
2. onresize
3. iframe causes the resize
And this chain:
body
 ↓
onresize
 ↓
print()
with:
iframe + onload
providing the automatic resize.
That's the core lesson of this lab.