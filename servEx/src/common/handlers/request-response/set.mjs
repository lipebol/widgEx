import { ParamsHandler } from "./params.js"

export class SetHandler {

    constructor(request, response) {
        try {
            this.handler = {
                ...request,
                response: response,
                validator: new Array()
            }
        } catch (err) { console.log(err) }
    }

    url(args) {
        try { return args.split('?')[0].split('/').slice(2) } catch (err) { console.log(err) }
    }

    model() {
        try {
            this.handler.model = this.handler.name && this.handler.table ?
                `_${(this.handler.name + this.handler.table).toUpperCase()}` :
                this.handler.about.resolver
            return this
        } catch (err) { console.log(err) }
    }

    filter() {
        try {
            this.handler.filter = this.handler.name && this.handler.column ? /// <--- REST
                process.env[`${(this.handler.name + this.handler.column).toUpperCase()}`] :
                Object.keys(this.handler)[0].toString() /// <--- GraphQL
            return this
        } catch (err) { console.log(err) }
    }

    query(args) { /// <--- REST
        try {
            if (args) {
                let [param] = Object.keys(args)
                let [arg] = Object.values(args)
                if (param && arg) { this.object.params = { [param]: arg } }
            }
        } catch (err) { console.log(err) }
    }

    param() { /// <--- GraphQL
        try {
            this.handler.params = Object.values(this.handler)[0] === '*' ?
                undefined : {
                    [this.handler.paramsType = this.handler.between ? 'dates' : 'multi']:
                        Object.values(this.handler)[0]
                }
            if (this.handler.params) { ParamsHandler.check(this.handler) }
            return this
        } catch (err) { console.log(err) }
    }

    page() {
        try {
            if (this.handler.page !== undefined) {
                this.handler.page = parseInt(this.handler.page) <= 0 ? 1 :
                    parseInt(this.handler.page)
            }
            return this
        } catch (err) { console.log(err) }
    }

    count() { try { this.handler.count = '*' } catch (err) { console.log(err) } }

    fields() {
        try {
            const unwrap = (content) => {
                return (
                    Array.isArray(content) ? content[0] : content
                ).selectionSet?.selections
            }

            unwrap(this.handler.about.fields).forEach(
                (node) => {
                    if (
                        node.typeCondition?.name.value
                        === this.handler.about.resolver
                    ) {
                        this.handler.fields = unwrap(unwrap(node))
                            .map(selection => selection.name.value)
                    }
                }
            )
            return this
        } catch (err) { console.log(err) }
    }

    lookup(...args) {
        try {
            if (args) {
                this.handler.lookup = args.length === 1 ?
                    args[0] : { path: args[0], populate: args[1] }
            }
            return this
        } catch (err) { console.log(err) }
    }

    sql() { try { this.handler.db = 'sql' } catch (err) { console.log(err) } }

    nosql() { try { this.handler.db = 'mongodb' } catch (err) { console.log(err) } }

    finally() { try { return this.handler } catch (err) { console.log(err) } }
}