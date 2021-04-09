const requestOptions = {
        method: 'POST',
        headers: { Authorization: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczNzg2ODYsIk5hbWUiOjF9.tJG5Pxtnqcx4JUhByDMnQ4z5s0CVs9vxYy7cvGNLeh4`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ JSON: JSON.stringify({title:'t',flavor:'f',color:'#FFF',description:'d' }) })
    };
console.log(fetch('http://10.10.10.217/requests', requestOptions))
