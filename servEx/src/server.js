require('dotenv').config()
const cors = require(process.env.CORS)
const Express = require(process.env.SERVER)
const Server = Express()

Server.use(cors())


Server.use(process.env.GRAPHQL_ENDPOINT, require(process.env.GRAPHQL))


Server.use((req, res) => {
    if (
        (
            req.url.includes(process.env.API) && !(
                req.url.includes(process.env.DOC) || 
                req.url.includes(process.env.GRAPHIQL_ENDPOINT)
            )
        )
    ) {
        return res.status(404).json({ error: process.env.NOT_FOUND })
    }
    return res.status(404).redirect(process.env._404_)
})

Server.listen(process.env.SERVER_PORT)