# Cereal Scripts

This folder contains several scripts I used when solving Cereal on HTB. This was the most difficult box I've done so far, and involved manual exploitation of a custom .NET deserialisation vulnerability, as well as an XSS CVE in a Markdown library that I had not seen before.

## gentoken.py

This was the initial script I used for generating JWT tokens to use when authenticating to the web application.

## www-files

These were several mini scripts I used when experimenting with the XSS Vulnerability, as well as when trying to get the formatting of the JSON payload right.

### stringify.js

When I did this box, I never actually visited the site via the browser after cracking the JWT token. I submitted all of my requests manually (not because I thought this was better, but because I sort of forgot adding the cookie to local storage would have worked).

This meant I spent most of my time on this box debugging the Controller structure and request syntax. As I was making my requests manually, a lot of issues arose getting the correct JSON syntax in curl and Burp Repeater - there were lots of special characters to escape, and both tools behaved differently. To help generate payloads that were consistent with the javascript running the site, I made a quick javascript file to replicate the format on the box.

### base64.js

This script was used to base64-encode my XSS payload, as doing so manually seemed to not work consistently. I wanted to use native javascript functions to encode it to make sure that the payload would work when decoded by the site.

## cereal-chain.py

This was the final script I used to gain user access on the box. It took me a while to decide to script the exploit, but once I did it making changes was a lot easier (as it saved regenerating base64 and JSON payloads).

The script chains together all the necessary parts of the exploit to upload a file to the box, which can then be used to execute code.

The script requires launching two listeners:
- one to serve the reverse shell payload or other file that will be downloaded to the box
- one to catch responses from the XSS - as a debugging technique, I set my XSS to post back the response from the requests that were made via an `<img>` tag. This was a technique I had not used before, and it ended up working very well - in future I might try to add automatic decoding of the base64 response that hits the server

I would have liked to build in a listener to serve up the files and catch the incoming connection, but I wasn't sure how to do that within the same program and handle I/O. I will look at doing this in future, but I was happy with the exploit and didn't want to spend much more time on the box at that point :D
