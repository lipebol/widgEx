import { buildSchema } from 'graphql'

export const schemas = buildSchema(`
    scalar Date

    interface Errors {
        error: String!
        message: String!
        status_code: Int!
    }

    type NotFound implements Errors {
        error: String!
        message: String!
        status_code: Int!
    }

    type BadRequest implements Errors {
        error: String!
        message: String!
        status_code: Int!
    }

    type InternalError implements Errors {
        error: String!
        message: String!
        status_code: Int!
    }

    type spotifExGenresFields {
        name: String
        url: String
    }

    type spotifExGenres {
        data: [spotifExGenresFields]
    }

    type spotifExArtists {
        name: String
        profile: String
        genres: [spotifExGenresFields]
    }

    type spotifExTracks {
        trackid: String
        length: String
        artUrl: String
        album: String
        artist: spotifExArtists
        autoRating: String
        discNumber: String
        title: String
        trackNumber: String
        url: String
    }
    
    type spotifExDaylists {
        track: spotifExTracks
        date: String
        listen: Int
    }

    union spotifExGenresResponse = spotifExGenres | NotFound | BadRequest | InternalError

    type Query {
        spotifExGenres(name: String): spotifExGenresResponse!
        spotifExArtists(name: String, page: Int): [spotifExArtists]
        spotifExTracks(title: String, page: Int): [spotifExTracks]
        spotifExDaylists(between: String, page: Int): [spotifExDaylists]
    }
`)