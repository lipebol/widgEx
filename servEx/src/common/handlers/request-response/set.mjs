import { ParamsHandler } from "./params.js"

export class SetHandler {

    constructor(request, response) {
        try {
            this.handler = {
                ...ParamsHandler.check(request),
                response: response,
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

    query(args) { /// <--- REST
        try {
            if (args) {
                let [param] = Object.keys(args)
                let [arg] = Object.values(args)
                if (param && arg) { this.object.params = { [param]: arg } }
            }
        } catch (err) { console.log(err) }
    }

    count() { try { this.handler.count = '*' } catch (err) { console.log(err) } }

    fields() {
        try {
            if (this.handler.about.fields && !this.handler.error) {
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
            }
            return this
        } catch (err) { console.log(err) }
    }

    lookup(...args) {
        try {
            if (this.handler.lookup) {
                if (args && !this.handler.error) {
                    this.handler.lookup = args.length === 1 ?
                        args[0] : { path: args[0], populate: args[1] }
                }
            }
            return this
        } catch (err) { console.log(err) }
    }

    page() {
        try {
            if (this.handler.page && !this.handler.error) {
                this.handler.page = parseInt(this.handler.page) <= 0 ? 1 :
                    parseInt(this.handler.page)
            }
            return this
        } catch (err) { console.log(err) }
    }

    sql() {
        try {
            if (!this.handler.error) { this.handler.db = 'sql' }
        } catch (err) { console.log(err) }
    }

    nosql() {
        try {
            if (!this.handler.error) { this.handler.db = 'nosql' }
        } catch (err) { console.log(err) }
    }

    build() {
        try {
            if (!this.handler.error) {
                if (this.handler.page) {
                    this.handler.offset = (this.handler.page - 1) * this.handler.limit
                }
                if (this.handler.filter && this.handler.params) {
                    switch (this.handler.db) {
                        case 'sql':
                            break
                        case 'nosql':
                            this.handler.where = (() => {
                                switch (this.handler.paramsType) {
                                    case 'dates':
                                        return {
                                            [this.handler.filter]: {
                                                '$gte': new Date(this.handler.params.start),
                                                '$lte': new Date(this.handler.params.end)
                                            }
                                        }
                                    case 'multi':
                                        return {
                                            [this.handler.filter]: {
                                                '$in': this.handler.params
                                            }
                                        }
                                }
                            })()
                            break
                    }
                }
            }
            return this.handler
        } catch (err) { console.log(err) }
    }
}