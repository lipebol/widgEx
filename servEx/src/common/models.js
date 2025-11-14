const { mongoose, mongooseSpotifEx } = require(process.env.INSTANCES)

const SPOTIFEX_GENRES = mongooseSpotifEx.model(
    'SPOTIFEX_GENRES', new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            name: { type: String, required: true },
            url: { type: String, required: true }
        }
    ), 'genres'
)

const SPOTIFEX_ARTISTS = mongooseSpotifEx.model(
    'SPOTIFEX_ARTISTS', new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            name: { type: String, required: true },
            profile: { type: String, required: true },
            genres: [{ type: mongoose.ObjectId, ref: 'SPOTIFEX_GENRES' }]
        }
    ), 'artists'
)

const SPOTIFEX_TRACKS = mongooseSpotifEx.model(
    'SPOTIFEX_TRACKS', new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            trackid: { type: String, required: true },
            length: { type: Number, required: true },
            artUrl: { type: String, required: true },
            album: { type: String, required: true },
            artist: { type: mongoose.ObjectId, ref: 'SPOTIFEX_ARTISTS' },
            autoRating: { type: Number, required: true },
            discNumber: { type: String, required: true },
            name: { type: String, required: true },
            trackNumber: { type: Number, required: true },
            url: { type: String, required: true }
        }
    ), 'tracks'
)

const SPOTIFEX_DAYLISTS = mongooseSpotifEx.model(
    'SPOTIFEX_DAYLISTS', new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            track: { type: mongoose.ObjectId, ref: 'SPOTIFEX_TRACKS' },
            date: { type: String, required: true },
            listen: { type: Number, required: true }
        }
    ), 'daylists'
)

module.exports = { SPOTIFEX_GENRES, SPOTIFEX_ARTISTS, SPOTIFEX_TRACKS, SPOTIFEX_DAYLISTS }