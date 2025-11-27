import { cryptHandler } from './handlers/crypt.js'
import { mongoose } from 'mongoose'
import { Sequelize } from 'sequelize'

// ========================================= mongoose =========================================
mongoose.set(
    'debug', (collection, method, query, agreggate, options) => {
        console.log(
            JSON.stringify(
                { collection, method, query, agreggate, options }, null, 2
            )
        )
    }
)

export const mongooseAddons = {
    collation: { locale: 'en', strength: 2 },
    versionKey: false
}

export const mongooseSpotifEx = mongoose.createConnection(
    cryptHandler(process.env.MONGODB_URI)
).useDb('spotifEx')


// ========================================= Sequelize =========================================

export const sequelizeConnect = new Sequelize(
    process.env.POSTGRES_URI,
    {
        dialect: process.env.DIALECT,
        //port: parseInt(process.env.POSTGRES_PORT)
    }
)