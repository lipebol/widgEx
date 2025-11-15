const { spawnSync } = require(process.env.PROCESS)

const cryptHandler = (uri) => {
    return spawnSync(
        `clevis-decrypt-tang < ${uri}`, 
        { shell: true, encoding: 'utf8' }
    ).stdout.trim()
}

module.exports = { cryptHandler }