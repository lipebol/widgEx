const router = require(process.env.SERVER).Router()
const { createHandler } = require(process.env.GRAPHQL_HTTP)
const GraphiQL = require(process.env.GRAPHIQL).default
const { schemas } = require(process.env.SCHEMAS)
const { resolvers } = require(process.env.RESOLVERS)


router.all(process.env.SLASH, createHandler({ schema: schemas, rootValue: resolvers }))
router.get(process.env.GRAPHQL_TOOL, GraphiQL({ endpoint: process.env.GRAPHQL_ENDPOINT }))

module.exports = router