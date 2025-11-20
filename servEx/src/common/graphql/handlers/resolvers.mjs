import { Controllers } from '../../controllers.mjs'


class Resolvers {

    static handler(request, context) {
        return {
            ...request,
            about: {
                resolver: context.fieldName,
                fields: context.fieldNodes
            }
        }
    }

    static create() {
        return {
            async spotifExGenres(request, _, context) {
                return await Controllers.multi(
                    Resolvers.handler(request, context)
                )
            },
            async spotifExArtists(args, _, context) {
                return await Controllers.multi(
                    Resolvers.handler(request, context)
                )
            },
            async spotifExTracks(args, _, context) {
                return await Controllers.multi(
                    Resolvers.handler(request, context)
                )
            },
            async spotifExDaylists(args, _, context) {
                return await Controllers.multi(
                    Resolvers.handler(request, context)
                )
            }
        }
    }
}

export const resolvers = Resolvers.create()