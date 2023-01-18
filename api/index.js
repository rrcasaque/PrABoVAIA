const express = require('express');
const port = process.env.PORT || 310;
const app = express();
const cors = require('cors');
const axios = require('axios');

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", 'GET,PUT,POST,DELETE');
    app.use(cors());
    next();
});

const corsOptions = {
    allowedHeaders: ['Content-Type', 'Authorization']
};

app.use(cors(corsOptions));

//https://brapi.dev/api/quote/PETR4%2CMGLU3?range=max&interval=1d&fundamental=true

// axios.get('https://brapi.dev/api/available').then(resp => {
//     let url = 'https://brapi.dev/api/quote/'
//     resp.data.stocks.map(quote => {
//         url += `${quote}%2C`
//     })
// url = url.slice(0, -3)
// url += '?range=max&interval=1d&fundamental=true'
// res.status(200)
// res.send(url);
// });

app.get('/', (req, res) => {
    axios.get('https://brapi.dev/api/available').then(resp => {        
        const historicalQuotes = [] 
        resp.data.stocks.map((stock) => {
            axios.get(`https://brapi.dev/api/quote/${stock}?range=max&interval=1d&fundamental=true`).then(resp => {
                historicalQuotes.push(resp.data);                
            })
        })        
        res.status(200)
        res.send(historicalQuotes);        
    });    
})

app.use((req, res) => {
    res.status(404);
    res.send("página não encontrada!");
})

app.listen(port, () => console.log(`servidor iniciado na porta ${port}`));