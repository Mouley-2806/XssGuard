# XssGuard v1 Specification

## 1. Purpose

XssGuard is a Flask middleware-based security tool designed to inspect user-controlled HTTP input for patterns associated with Cross-Site Scripting (XSS).

The goal of v1 is to build a small defensive security component while learning how HTTP requests, user input, and XSS vulnerabilities interact.

---

## 2. Architecture

XssGuard v1 will be implemented as Flask middleware.

The basic flow is:

Browser
↓
HTTP Request
↓
XssGuard
↓
Flask Application
↓
HTTP Response
↓
Browser

XssGuard will inspect incoming HTTP requests before they reach the application.

---

## 3. Exact Input

XssGuard v1 will inspect the following user-controlled HTTP input:

### Query parameters

Example:

```text
/search?q=<script>alert(1)</script>
```

### Form parameters

Example:

```text
comment=<img src=x onerror=alert(1)>
```

### Selected HTTP headers

XssGuard may inspect selected request headers that can contain user-controlled values.

The initial implementation will focus on:

* Query parameters
* Form parameters
* Selected HTTP headers

---

## 4. Processing

For each input value, XssGuard will:

1. Extract the input.
2. Normalize the input where appropriate.
3. Check for patterns associated with XSS.
4. Determine whether a potential XSS pattern was detected.
5. Record the relevant parameter and input location.
6. Produce a structured detection result.

XssGuard v1 is a pattern-based detection system and does not claim that every detected value is exploitable.

---

## 5. Exact Output

XssGuard will produce a structured detection result.

### Potential XSS

```json
{
  "detected": true,
  "type": "potential_reflected_xss",
  "parameter": "q",
  "location": "query",
  "severity": "high"
}
```

### No detection

```json
{
  "detected": false,
  "type": null,
  "parameter": "q",
  "location": "query",
  "severity": "none"
}
```

XssGuard will also maintain a security log containing information such as:

```text
Potential XSS detected
Parameter: q
Location: query
Severity: high
```

---

## 6. Non-Goals

The following are explicitly outside the scope of XssGuard v1:

* Automatic exploitation of vulnerabilities
* Execution of JavaScript payloads
* Browser automation
* Scanning the entire internet
* Replacing Burp Suite or OWASP ZAP
* Guaranteeing that an application is free of XSS
* Detecting every possible XSS technique
* Automatically modifying or deleting user input
* Acting as a Web Application Firewall (WAF)
* Supporting every web framework
* JavaScript source-code analysis
* DOM-based XSS analysis
* Database-wide stored-XSS analysis

These capabilities may be considered in future versions but are not part of v1.

---

## 7. Security Scope

XssGuard v1 is primarily focused on detecting suspicious user-controlled input associated with reflected XSS.

The tool is intended for defensive security learning and experimentation in applications that the user owns or is authorized to test.

---

## 8. Success Criteria

XssGuard v1 will be considered complete when it can:

* Receive an HTTP request through Flask.
* Extract query parameters and form parameters.
* Inspect the extracted values.
* Identify predefined suspicious XSS patterns.
* Produce a structured detection result.
* Record a security log.
* Demonstrate the detection using a controlled local Flask application.

## 9. Version Boundary

This specification defines the fixed scope of XssGuard v1.

New functionality should not be added to v1 unless the scope is intentionally revised.
