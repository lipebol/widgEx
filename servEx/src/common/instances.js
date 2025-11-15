const { cryptHandler } = require(process.env.HANDLER_CRYPT)
const { mongoose } = require(process.env.ODM)
const { Sequelize, Op } = require(process.env.ORM)

const mongooseSpotifEx = mongoose.createConnection(
    cryptHandler(process.env.MONGODB_URI)
).useDb('spotifEx')

mongoose.set(
    'debug', (collection, method, query, agreggate, options) => {
        console.log(
            JSON.stringify(
                { collection, method, query, agreggate, options }, null, 2
            )
        )
    }
)

const sequelizeConnect = new Sequelize(
    process.env.POSTGRES_URI,
    {
        dialect: process.env.DIALECT,
        //port: parseInt(process.env.POSTGRES_PORT)
    }
)

module.exports = { mongoose, mongooseSpotifEx, Sequelize, sequelizeConnect, Op }