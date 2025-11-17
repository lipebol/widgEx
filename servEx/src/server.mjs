import 'dotenv/config'
import cors from 'cors'
import Express from 'express'
import router from './common/graphql/gql.mjs'
const Server = Express()

Server.use(cors())

Server.use(process.env.GRAPHQL_ENDPOINT, router)

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