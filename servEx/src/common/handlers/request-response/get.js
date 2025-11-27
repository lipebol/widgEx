import { SetHandler } from './set.mjs'

export class GetHandler {

    static create(request, response) {
        try {
            const handler = new SetHandler(request, response)
            return request.route ?
                GetHandler.#REST(handler) :
                GetHandler.#GraphQL(handler, request.about.resolver)
        } catch (err) { console.log(err) }
    }

    static response(dataobject) {
        try {
            if (dataobject.response) {
                this.status = parseInt(
                    process.env[Object.keys(data).toString().toUpperCase()]
                )
                return response.status(this.status ? this.status : 200).json(data)
            } else {
                // __typename: --> essential when you deal with unions/interfaces
                if (dataobject.error) {
                    return {
                        __typename: dataobject.error.name, error: dataobject.error.name,
                        message: process.env[dataobject.error.name],
                        status_code: dataobject.error.code
                    }
                }
                return dataobject.info ? {
                    __typename: 'Info', total: dataobject.data.count,
                    pages: dataobject.data.countpages
                } : { __typename: dataobject.about.resolver, data: dataobject.data }
            }
        } catch (err) { console.log(err) }
    }

    static #REST(handler) {
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

    static #GraphQL(handler, resolvername) {
        try {
            switch (resolvername) {
                case 'spotifExGenres':
                    handler.model()
                        .fields()
                        .nosql()
                    break
                case 'spotifExArtists':
                    handler.model()
                        .page()
                        .lookup('genres')
                        .nosql()
                    break
                case 'spotifExTracks':
                    handler.model()
                        .lookup('artist', { path: 'genres' })
                        .nosql()
                    break
                case 'spotifExDaylists':
                    handler.model()
                        .lookup('track', { path: 'artist', populate: { path: 'genres' } })
                        .nosql()
                    break
            }
            return handler.build()
        } catch (err) { console.log(err) }
    }
}