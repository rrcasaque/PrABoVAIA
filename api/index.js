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

//função para construir as requisições
//parametros:
// - url de aquisição dos ativos
// - quantidade de divisões 
// - intervalo de obtenção de histórico

const getURL = async (url, divide,range) => {
    const DIVIDE = divide
    const finalRes = []
    await axios.get(url).then(resp => {
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
            urlReq += `?range=${range}&interval=1d&fundamental=true`
            finalRes.push(urlReq)
        }
    })
    return finalRes
}

// função para realizar todas as requisições 

const getHistoricalStocks = async (URLs, finalArray) => {
    await axios.get(URLs[0]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[1]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[2]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[3]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[4]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[5]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[6]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[7]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[8]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[9]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[10]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[11]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[12]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[13]).then(resp => {
        finalArray.push(resp.data.results)
    })
    await axios.get(URLs[14]).then(resp => {
        finalArray.push(resp.data.results)
    })
    return finalArray
}

app.get('/', async (req, res) => {    
    const aa = req.query.aa
    res.send(`resposta obtida: ${aa}`)
})

app.get('/getURL', async (req, res) => {    
    const resposta = await getURL('https://brapi.dev/api/available', 15)
    res.send(resposta)
})

//localhost:3000/getHistory?range='max'

app.get('/getHistory', async (req, res) => {    
    let range = 'max'
    if(req.query.range!=undefined) range = req.query.range
    const resposta = await getURL('https://brapi.dev/api/available', 15,range)     
    const finalArray = await getHistoricalStocks(resposta,[])
    res.send(finalArray)
})

app.use((req, res) => {
    res.status(404);
    res.send("página não encontrada!");
})

app.listen(port, () => console.log(`servidor iniciado na porta ${port}`));