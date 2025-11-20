import { SetHandler } from './set.mjs'

export class GetHandler {

    static create(request, response) {
        try {
            const handler = new SetHandler(request, response)
            return request.route ?
                GetHandler.REST(handler) :
                GetHandler.GraphQL(handler, request.about.resolver)
        } catch (err) { console.log(err) }
    }

    static response(handler) {
        try {
            console.log(handler)
            if (handler.response) {
                this.status = parseInt(
                    process.env[Object.keys(data).toString().toUpperCase()]
                )
                return response.status(this.status ? this.status : 200).json(data)
            } else {
                if (handler.error) {
                    return GetHandler.GraphQLError(
                        handler.error.name, handler.error.code
                    )
                } else {
                    return handler.data.length === 0 ?
                        GetHandler.GraphQLError('NotFound', 404) :
                        { __typename: handler.about.resolver, data: handler.data }
                }
            }
        } catch (err) { console.log(err) }
    }

    static REST(handler) {
        try {
            let [version, name, table, column] = set.url(request.originalUrl)
            sethandler.model({ name, table })
            if (request.query && column) {
                sethandler.filter({ name, column })
                sethandler.query(request.query)
                if (request.query.page) {
                    sethandler.page(request.query.page)
                } else { sethandler.count() }
            }
            return sethandler.finally()
        } catch (err) { console.log(err) }
    }

    static GraphQL(handler, resolver) {
        try {
            switch (resolver) {
                case 'spotifExGenres':
                    handler.model()
                        .filter()
                        .param()
                        .fields()
                        .nosql()
                    break
                case 'spotifExArtists':
                    handler.model()
                        .filter()
                        .param()
                        .page()
                        .lookup('genres')
                        .nosql()
                    break
            }
            return handler.finally()
        } catch (err) { console.log(err) }
    }

    static GraphQLError(name, code) {
        // __typename: --> essential when you deal with unions/interfaces
        return {
            __typename: name, error: name,
            message: process.env[name], status_code: code
        }
    }
}