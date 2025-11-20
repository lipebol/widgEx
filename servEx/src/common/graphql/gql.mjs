import { dirname, join } from 'path'
import { fileURLToPath } from 'url'
import { Router } from 'express'
import { createHandler } from 'graphql-http/lib/use/express'
import { schemas } from './handlers/schemas.mjs'
import { resolvers } from './handlers/resolvers.mjs'

const router = Router()

router.all(process.env.SLASH, createHandler({ schema: schemas, rootValue: resolvers }))
router.get(
    process.env.GRAPHQL_TOOL, (request, response) => {
        response.sendFile(join(dirname(fileURLToPath(import.meta.url)), process.env.GRAPHIQL))
    }
)

export default router