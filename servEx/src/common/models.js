import { mongoose } from 'mongoose'
import { mongooseAddons, mongooseSpotifEx } from './instances.js'

export const spotifExGenres = mongooseSpotifEx.model(
    'spotifExGenres', new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            name: { type: String, required: true },
            url: { type: String, required: true }
        }, mongooseAddons
    ), 'genres'
)

export const spotifExArtists = mongooseSpotifEx.model(
    'spotifExArtists', new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            name: { type: String, required: true },
            profile: { type: String, required: true },
            genres: [{ type: mongoose.ObjectId, ref: 'spotifExGenres' }]
        }, mongooseAddons
    ), 'artists'
)

export const spotifExTracks = mongooseSpotifEx.model(
    'spotifExTracks', new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            trackid: { type: String, required: true },
            length: { type: Number, required: true },
            artUrl: { type: String, required: true },
            album: { type: String, required: true },
            artist: { type: mongoose.ObjectId, ref: 'spotifExArtists' },
            autoRating: { type: Number, required: true },
            discNumber: { type: String, required: true },
            title: { type: String, required: true },
            trackNumber: { type: Number, required: true },
            url: { type: String, required: true }
        }, mongooseAddons
    ), 'tracks'
)

export const spotifExDaylists = mongooseSpotifEx.model(
    'spotifExDaylists', new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            track: { type: mongoose.ObjectId, ref: 'spotifExTracks' },
            date: { type: String, required: true },
            listen: { type: Number, required: true }
        }, mongooseAddons
    ), 'daylists'
)