// Extra cleanup run when a staff user or a member is deleted.
//
// Each helper closes one residual trace found by the deletion audit:
//   destroyUserSessions      bug           sessions rows outlived the user (no FK, never purged)
//   scrubActions             non-compliant history log kept the deleted person's name / email
//   deleteOrphanedImages     bug           profile / cover images stayed on disk and publicly served
//   pruneDeletionBackups     non-compliant pre-deletion JSON backups were kept forever
const fs = require('fs-extra');
const path = require('path');
const logging = require('@tryghost/logging');
const config = require('../../../shared/config');

const IMAGE_PREFIX = '/content/images/';

/** Delete every session belonging to the user (sessions.user_id has no foreign key). */
async function destroyUserSessions(knex, userId, transacting) {
    const q = knex('sessions').where('user_id', userId);
    if (transacting) {
        q.transacting(transacting);
    }
    return q.del();
}

/**
 * Replace the given strings (name, email) in the history log with a placeholder.
 * The audit trail keeps the fact that something happened, not who it was about.
 */
async function scrubActions(knex, needles, replacement, transacting) {
    const values = [...new Set(needles.filter(n => typeof n === 'string' && n.length >= 3))];
    let changed = 0;
    for (const value of values) {
        const escaped = value.replace(/[\\%_]/g, c => `\\${c}`);
        const q = knex('actions').select('id', 'context').where('context', 'like', `%${escaped}%`);
        if (transacting) {
            q.transacting(transacting);
        }
        for (const row of await q) {
            const u = knex('actions').where('id', row.id)
                .update({context: row.context.split(value).join(replacement)});
            if (transacting) {
                u.transacting(transacting);
            }
            await u;
            changed += 1;
        }
    }
    return changed;
}

function relativeImagePath(url) {
    if (!url || typeof url !== 'string') {
        return null;
    }
    const i = url.indexOf(IMAGE_PREFIX);
    return i === -1 ? null : url.slice(i + IMAGE_PREFIX.length).split('?')[0];
}

/** True if any remaining row still points at the image. */
async function imageStillReferenced(knex, rel) {
    const like = `%${IMAGE_PREFIX}${rel.replace(/[\\%_]/g, c => `\\${c}`)}%`;
    const checks = [
        ['posts', ['feature_image', 'lexical', 'mobiledoc', 'html']],
        ['posts_meta', ['og_image', 'twitter_image']],
        ['users', ['profile_image', 'cover_image']],
        ['tags', ['feature_image', 'og_image', 'twitter_image']],
        ['settings', ['value']]
    ];
    for (const [table, cols] of checks) {
        const q = knex(table).count({n: '*'}).where(function () {
            for (const c of cols) {
                this.orWhere(c, 'like', like);
            }
        });
        const [{n}] = await q;
        if (Number(n) > 0) {
            return true;
        }
    }
    return false;
}

/**
 * Remove the deleted user's own images (original + resized copies) unless something
 * else still uses them. Runs after the deletion has committed.
 */
async function deleteOrphanedImages(knex, urls) {
    const storagePath = config.getContentPath('images');
    const removed = [];
    for (const url of urls) {
        const rel = relativeImagePath(url);
        if (!rel || rel.includes('..') || await imageStillReferenced(knex, rel)) {
            continue;
        }
        const {dir, name, ext} = path.parse(rel);
        const candidates = [rel, path.join(dir, `${name}_o${ext}`)];
        const sizeRoot = path.join(storagePath, 'size');
        if (await fs.pathExists(sizeRoot)) {
            // resized variants live under size/w<N>/<rel> (and size/w<N>/format/<fmt>/<rel>)
            const walk = async (d) => {
                for (const e of await fs.readdir(d, {withFileTypes: true})) {
                    const p = path.join(d, e.name);
                    if (e.isDirectory()) {
                        await walk(p);
                    } else if (p.endsWith(path.join(dir, `${name}${ext}`))) {
                        candidates.push(path.relative(storagePath, p));
                    }
                }
            };
            await walk(sizeRoot);
        }
        for (const c of candidates) {
            const p = path.join(storagePath, c);
            if (await fs.pathExists(p)) {
                await fs.remove(p);
                removed.push(c);
            }
        }
    }
    if (removed.length) {
        logging.info(`Deleted ${removed.length} image file(s) of a deleted user`);
    }
    return removed;
}

/**
 * Pre-deletion backups exist to undo a failed or mistaken deletion. Keep them only for
 * `privacy:deletionBackupRetentionDays` days (default 0 = remove once the deletion succeeded).
 * Only backups written by a deletion are tracked (in data/.deletion-backups.json), so
 * migration backups and manual exports are never touched.
 */
async function pruneDeletionBackups(justWritten) {
    const days = Number(config.get('privacy:deletionBackupRetentionDays') || 0);
    const dataDir = config.getContentPath('data');
    const manifestPath = path.join(dataDir, '.deletion-backups.json');
    const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;

    let manifest = [];
    if (await fs.pathExists(manifestPath)) {
        manifest = await fs.readJson(manifestPath).catch(() => []);
    }
    if (justWritten) {
        manifest.push({file: path.basename(justWritten), at: Date.now()});
    }

    const removed = [];
    const keep = [];
    for (const entry of manifest) {
        const p = path.join(dataDir, path.basename(entry.file));
        if (days === 0 || entry.at < cutoff) {
            if (await fs.pathExists(p)) {
                await fs.remove(p);
            }
            removed.push(entry.file);
        } else {
            keep.push(entry);
        }
    }
    await fs.writeJson(manifestPath, keep);
    return removed;
}

module.exports = {
    destroyUserSessions,
    scrubActions,
    deleteOrphanedImages,
    pruneDeletionBackups
};
