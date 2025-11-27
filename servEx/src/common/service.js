import { Op } from 'sequelize'
import * as models from './models.js'

export class Service {

    static async sql(dataobject) {
        try {

            this.sequelize = new setSequelize(this.newObject())

            this.sequelize.order(object.filter)
            this.sequelize.attributes(object.fields)


            if (object.params) {
                if (object.params.dates === process.env.MAX) {
                    return await models[object.model].max(object.filter)
                }
                this.sequelize.where(object.filter, this.setParams(object.params, this.newObject()))
            }


            if (object.page) {
                this.sequelize.offset(this.setOffSet(object.page, this.setLimit))
                this.sequelize.limit(this.setLimit)
            } else if (dataobject.count) {
                dataobject.count = await models[dataobject.model]
                    .count(this.sequelize.finally())
                return {
                    total: dataobject.count,
                    pages: Math.ceil(parseFloat(rows) / dataobject.limit)
                }
            }

            return await models[object.model].findAll(this.sequelize.finally())
        } catch (err) { console.log(err) }
    }


    static async nosql(dataobject) {
        try {
            const data = await models[dataobject.model]
                .find(dataobject.where).sort({ [dataobject.filter]: 'asc' })
                .select(dataobject.fields).skip(dataobject.offset)
                .limit(dataobject.limit).populate(dataobject.lookup).exec()

            if (data.length === 0) {
                dataobject.error = { name: 'NotFound', code: 404 }
            }

            if (!dataobject.error && dataobject.info) {
                return {
                    count: data.length, countpages: Math.ceil(
                        parseFloat(data.length) / 100
                    )
                }
            }
            return data
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


