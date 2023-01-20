const express = require('express');
const port = process.env.PORT || 3000;
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


app.get('/getAllReq', (req, res) => {
    const DIVIDE = 15
    axios.get('https://brapi.dev/api/available').then(resp => {
        const finalRes = []
        const availableStocks = resp.data.stocks
        const qtdStocks = availableStocks.length
        const qtdReq = Math.ceil(qtdStocks / DIVIDE)
        for (let i = 0; i < DIVIDE; i++) {
            let urlReq = 'https://brapi.dev/api/quote/'
            for (let j = qtdReq * i; j < qtdReq * (i + 1); j++) {
                if (j > qtdStocks || availableStocks[j] == null)
                    break
                else
                    urlReq += `${availableStocks[j]}%2C`
            }
            urlReq = urlReq.slice(0, -3)
            urlReq += '?range=max&interval=1d&fundamental=true'
            finalRes.push(urlReq)
        }
        res.status(200);
        res.send(finalRes)
    })
})

app.use((req, res) => {
    res.status(404);
    res.send("página não encontrada!");
})

app.listen(port, () => console.log(`servidor iniciado na porta ${port}`));