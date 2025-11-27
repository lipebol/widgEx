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

    type Info {
        total: Int
        pages: Int
    }

    type spotifExGenresFields {
        name: String
        url: String
    }

    type spotifExGenres {
        data: [spotifExGenresFields]
    }

    type spotifExArtistsFields {
        name: String
        profile: String
        genres: [spotifExGenresFields]
    }

    type spotifExArtists {
        data: [spotifExArtistsFields]
    }

    type spotifExTracksFields {
        trackid: String
        length: String
        artUrl: String
        album: String
        artist: spotifExArtistsFields
        autoRating: String
        discNumber: String
        title: String
        trackNumber: String
        url: String
    }

    type spotifExTracks {
        data: [spotifExTracksFields]
    }
    
    type spotifExDaylistsFields {
        track: spotifExTracksFields
        date: String
        listen: Int
    }

    type spotifExDaylists {
        data: [spotifExDaylistsFields]
    }

    union spotifExGenresResponse = spotifExGenres | Info | NotFound | BadRequest | InternalError
    union spotifExArtistsResponse = spotifExArtists | Info | NotFound | BadRequest | InternalError
    union spotifExTracksResponse = spotifExTracks | Info | NotFound | BadRequest | InternalError
    union spotifExDaylistsResponse = spotifExDaylists | Info | NotFound | BadRequest | InternalError

    type Query {
        spotifExGenres(name: String, info: Boolean): spotifExGenresResponse!
        spotifExArtists(name: String, page: Int, info: Boolean, lookup: Boolean): spotifExArtistsResponse!
        spotifExTracks(title: String, page: Int, info: Boolean, lookup: Boolean): spotifExTracksResponse!
        spotifExDaylists(date: String, page: Int, info: Boolean, lookup: Boolean): spotifExDaylistsResponse!
    }
`)