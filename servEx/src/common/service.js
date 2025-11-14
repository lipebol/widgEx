const { Sequelize, Op } = require(process.env.INSTANCES)
const {
     SPOTIFEX_GENRES, SPOTIFEX_ARTISTS, 
     SPOTIFEX_TRACKS, SPOTIFEX_DAYLISTS 
} = require(process.env.MODELS)


class Service {

    constructor() {
        this.newObject = () => { return JSON.parse(process.env.OBJECT_EMPTY) }
        this.setModel = (model) => { return eval(model) }
        this.setLimit = parseInt(process.env.LIMIT)
        this.setOffSet = (page, limit) => { try { if (page && limit) { return (page - 1) * limit } } catch (err) { console.log(err) } }
        this.setParams = (params, newObject) => {
            try {
                if (params.dates) {
                    [newObject.start, newObject.end] = params.dates
                        .split(process.env.SEPARATOR)
                    newObject.end = newObject.end.concat(
                        process.env.SPACE, process.env.HOUR_END
                    )
                } else if (params.multi) {
                    newObject.multi = params.multi
                }
                return newObject
            } catch (err) { console.log(err) }
        }

        this.counter = (rows, newObject) => {
            newObject.total_registros = rows
            newObject.paginas = Math.ceil(parseFloat(rows) / this.setLimit)
            return newObject
        }
    }


    async sql(object) {
        try {

            this.sequelize = new setSequelize(this.newObject())

            this.sequelize.order(object.filter)
            this.sequelize.attributes(object.fields)


            if (object.params) {
                if (object.params.dates === process.env.MAX) {
                    return await this.setModel(object.model).max(object.filter)
                }
                this.sequelize.where(object.filter, this.setParams(object.params, this.newObject()))
            }


            if (object.page) {
                this.sequelize.offset(this.setOffSet(object.page, this.setLimit))
                this.sequelize.limit(this.setLimit)
            } else if (object.count) {
                return this.counter(
                    await this.setModel(object.model)
                        .count(this.sequelize.finally()), this.newObject()
                )
            }

            return await this.setModel(object.model).findAll(this.sequelize.finally())
        } catch (err) { console.log(err) }
    }


    async mongodb(object) {
        try {

            this.mongoose = new setMongoose(
                object.filter, object.params ?
                this.setParams(object.params, this.newObject()) : undefined
            )

            return await this.setModel(object.model)
                .find(this.mongoose.where()).sort(this.mongoose.sort())
                .select(object.fields).skip(this.setOffSet(object.page, this.setLimit))
                .limit(this.setLimit).populate(object.lookup).exec()
        } catch (err) { console.log(err) }
    }
}


class setSequelize {
    constructor(objectJSON) { this.object = objectJSON }
    where(filter, params) {
        try {
            if (filter && params) {
                this.object.where = Object.keys(params).length === 1 ?
                    { [filter]: { [Op.in]: params.multi } } :
                    { [filter]: { [Op.between]: [new Date(params.start), new Date(params.end)] } }
            }
        } catch (err) { console.log(err) }
    }
    order(filter) { try { if (filter) { this.object.order = [[filter, 'ASC']] } } catch (err) { console.log(err) } }
    attributes(fields) { try { if (fields) { this.object.attributes = fields } } catch (err) { console.log(err) } }
    offset(offset) { try { if (offset) { this.object.offset = offset } } catch (err) { console.log(err) } }
    limit(limit) { try { if (limit) { this.object.limit = limit } } catch (err) { console.log(err) } }
    finally() { try { return this.object } catch (err) { console.log(err) } }
}


class setMongoose {
    constructor(filter, params) {
        this.filter = filter
        this.params = params
    }
    where() {
        try {
            if (this.filter && this.params) {
                return Object.keys(this.params).length === 1 ?
                    { [this.filter]: { '$in': this.params.multi } } :
                    { [this.filter]: { '$gte': new Date(this.params.start), '$lte': new Date(this.params.end) } }
            }
        } catch (err) { console.log(err) }
    }
    sort() { try { if (this.filter) { return { [this.filter]: 'asc' } } } catch (err) { console.log(err) } }
}


const service = new Service()

module.exports = service
