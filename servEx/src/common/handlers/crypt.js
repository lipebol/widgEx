import { spawnSync } from 'child_process'

export const cryptHandler = (uri) => {
    return spawnSync(
        `clevis-decrypt-tang < ${uri}`, 
        { shell: true, encoding: 'utf8' }
    ).stdout.trim()
}