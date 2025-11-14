const { mongoose } = require(process.env.ODM)
const { Sequelize } = require(process.env.ORM)

const mongooseSpotifEx = mongoose.createConnection(process.env.ENGINE_MONGODB).useDb('spotifEx')

mongoose.set(
    'debug', (collection, method, query, agreggate, options) => {
        console.log(JSON.stringify({ collection, method, query, agreggate, options }, null, 2))
    }
)

const sequelizeConnect = new Sequelize(
    process.env.ENGINE_POSTGRES,
    {
        dialect: process.env.DIALECT,
        //port: parseInt(process.env.POSTGRES_PORT)
    }
)

module.exports = { mongoose, mongooseSpotifEx, Sequelize, sequelizeConnect }