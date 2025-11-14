const { mongoose } = require(process.env.MONGOOSE)

const mongooseSpotifEx = mongoose.createConnection(process.env.ENGINE_MONGODB).useDb('spotifEx')

mongoose.set(
    'debug', (collection, method, query, agreggate, options) => {
        console.log(JSON.stringify({ collection, method, query, agreggate, options }, null, 2))
    }
)


module.exports = { mongoose, mongooseSpotifEx }