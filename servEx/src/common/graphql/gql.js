const router = require(process.env.SERVER).Router()
const { createHandler } = require(process.env.GRAPHQL_HTTP)
const { schemas } = require(process.env.SCHEMAS)
const { resolvers } = require(process.env.RESOLVERS)


router.all(process.env.SLASH, createHandler({ schema: schemas, rootValue: resolvers }))
router.get(
    process.env.GRAPHQL_TOOL, (request, response) => {
        response.sendFile(require('path').join(__dirname, process.env.GRAPHIQL))
    }
)

module.exports = router