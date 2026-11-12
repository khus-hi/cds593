
## User `a`: 13 canary tokens, 5 identifiers

Distinct needles found, per layer and phase:

| layer | t0-before | t1-immediate | t2-after-jobs | t3-after-restart |
|---|---|---|---|---|
| db | 17 | 12 | 12 | 12 |
| binlog | 17 | 17 | 17 | 17 |
| innodb_raw | 17 | 17 | 17 | 17 |
| content | 6 | 16 | 16 | 16 |
| stdout | 2 | 6 | 6 | 6 |
| mail | 3 | 3 | 3 | 3 |
| public_web | 11 | 7 | 7 | 7 |
| admin_api | 16 | 11 | 11 | 11 |
| **any layer** | 17 | 17 | 17 | 17 |

After deletion (t3-after-restart): 13/13 canary tokens still observable somewhere; 0/13 data types completely removed (none).

Where each surviving needle is, in the last scan:

| needle | what | locations |
|---|---|---|
| `cnryghabie99a18` | profile bio | binlog:DELETE users; binlog:UPDATE users; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd |
| `cnryghaca14603f` | co-authored post body | admin_api:posts; binlog:INSERT post_revisions; binlog:INSERT posts; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; public_web:/; public_web:/post-cnryghapt064f56/; public_web:/rss/ |
| `cnryghaci601d12` | cover image upload (filename) | binlog:DELETE users; binlog:UPDATE users; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; content:images/ (file name); content:logs/http___localhost_2368_production.log; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd; public_web:uploaded image still served; stdout:docker logs ghost |
| `cnryghadr02e0cb` | draft post body | admin_api:posts; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:UPDATE post_revisions; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd |
| `cnryghaema3029e` | email address | admin_api:history log; binlog:DELETE invites; binlog:DELETE users; binlog:INSERT actions; binlog:INSERT invites; binlog:INSERT users; binlog:UPDATE invites; binlog:UPDATE users; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; db:actions; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/users.ibd; innodb_raw:undo_001; innodb_raw:undo_002; mail:mail: Reset Password; mail:mail: Site Owner has invited you to join Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt064f56 |
| `cnryghaim9f122f` | image uploaded into a post (filename) | admin_api:posts; binlog:INSERT post_revisions; binlog:UPDATE post_revisions; binlog:UPDATE posts; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; content:images/ (file name); content:logs/http___localhost_2368_production.log; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; public_web:/post-cnryghapt064f56/; public_web:/rss/; public_web:uploaded image still served; stdout:docker logs ghost |
| `cnryghalo751709` | profile location | binlog:DELETE users; binlog:UPDATE users; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd |
| `cnryghanm0c2d4b` | display name | admin_api:history log; binlog:DELETE users; binlog:INSERT actions; binlog:INSERT users; binlog:UPDATE users; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; db:actions; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/users.ibd |
| `cnryghapbdc849e` | published post body | admin_api:posts; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:UPDATE post_revisions; binlog:UPDATE posts; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:undo_002; public_web:/; public_web:/post-cnryghapt064f56/; public_web:/rss/ |
| `cnryghapicb9f84` | profile image upload (filename) | binlog:DELETE users; binlog:UPDATE users; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; content:images/ (file name); content:logs/http___localhost_2368_production.log; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd; public_web:uploaded image still served; stdout:docker logs ghost |
| `cnryghapt064f56` | published post title | admin_api:history log; admin_api:posts; binlog:INSERT actions; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:UPDATE post_revisions; binlog:UPDATE posts; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; content:logs/http___localhost_2368_production.log; db:actions; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:undo_002; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt064f56; public_web:/; public_web:/post-cnryghapt064f56/; public_web:/rss/; public_web:/sitemap-posts.xml; stdout:docker logs ghost |
| `cnrygharvfcec73` | earlier post revision (text later edited away) | binlog:INSERT post_revisions; binlog:INSERT posts; binlog:UPDATE post_revisions; binlog:UPDATE posts; db:post_revisions; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:undo_002 |
| `cnryghaws53ca34` | profile website | binlog:DELETE users; binlog:UPDATE users; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd |
| `6af643ab1a6add0001bce148` | user id | admin_api:history log; binlog:DELETE posts_authors; binlog:DELETE roles_users; binlog:DELETE users; binlog:INSERT actions; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:INSERT posts_authors; binlog:INSERT roles_users; binlog:INSERT sessions; binlog:INSERT users; binlog:UPDATE post_revisions; binlog:UPDATE posts; binlog:UPDATE posts_authors; binlog:UPDATE users; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; content:logs/http___localhost_2368_production.log; db:actions; db:posts; db:sessions; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:ghost/posts_authors.ibd; innodb_raw:ghost/roles_users.ibd; innodb_raw:ghost/sessions.ibd; innodb_raw:ghost/users.ibd; innodb_raw:undo_001; innodb_raw:undo_002; stdout:docker logs ghost |
| `6af643b21a6add0001bce152` | post id | admin_api:history log; admin_api:posts; binlog:INSERT actions; binlog:INSERT comments; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:INSERT posts_authors; binlog:INSERT posts_tags; binlog:UPDATE post_revisions; binlog:UPDATE posts; binlog:UPDATE posts_authors; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; content:logs/http___localhost_2368_production.log; db:actions; db:comments; db:post_revisions; db:posts; db:posts_authors; db:posts_tags; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/comments.ibd; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:ghost/posts_authors.ibd; innodb_raw:ghost/posts_tags.ibd; innodb_raw:undo_001; innodb_raw:undo_002; public_web:/post-cnryghapt064f56/; public_web:/rss/; stdout:docker logs ghost |
| `6af643b41a6add0001bce15a` | draft post id | admin_api:history log; admin_api:posts; binlog:INSERT actions; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:INSERT posts_authors; binlog:INSERT posts_tags; binlog:UPDATE post_revisions; binlog:UPDATE posts_authors; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; content:logs/http___localhost_2368_production.log; db:actions; db:post_revisions; db:posts; db:posts_authors; db:posts_tags; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:ghost/posts_authors.ibd; innodb_raw:ghost/posts_tags.ibd; innodb_raw:undo_002 |
| `cnryghaema3029e@example.com` | email | admin_api:history log; binlog:DELETE invites; binlog:DELETE users; binlog:INSERT actions; binlog:INSERT invites; binlog:INSERT users; binlog:UPDATE invites; binlog:UPDATE users; content:data/audit-blog.ghost.2026-11-12-22-55-24.json; db:actions; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/users.ibd; innodb_raw:undo_001; innodb_raw:undo_002; mail:mail: Reset Password; mail:mail: Site Owner has invited you to join Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt064f56 |

## User `m`: 8 canary tokens, 6 identifiers

Distinct needles found, per layer and phase:

| layer | t0-before | t1-immediate | t2-after-jobs | t3-after-restart |
|---|---|---|---|---|
| db | 13 | 11 | 11 | 11 |
| binlog | 13 | 13 | 13 | 13 |
| innodb_raw | 13 | 13 | 13 | 13 |
| content | 3 | 3 | 3 | 3 |
| stdout | 2 | 2 | 2 | 2 |
| mail | 8 | 8 | 8 | 8 |
| public_web | 8 | 4 | 4 | 4 |
| admin_api | 8 | 3 | 3 | 3 |
| **any layer** | 14 | 13 | 13 | 13 |

After deletion (t3-after-restart): 8/8 canary tokens still observable somewhere; 0/8 data types completely removed (none).

Where each surviving needle is, in the last scan:

| needle | what | locations |
|---|---|---|
| `cnryghmcm3e51c0` | comment body | binlog:INSERT comments; db:comments; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/comments.ibd; mail:mail: 💬 New comment on your post: Post cnryghapt064f56; public_web:/members/api/comments/post/6af643b21a6add0001bce152/ |
| `cnryghmema7fe23` | email address | binlog:DELETE members; binlog:INSERT members; binlog:INSERT tokens; binlog:UPDATE members; binlog:UPDATE tokens; db:tokens; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd; innodb_raw:ghost/tokens.ibd; innodb_raw:undo_002; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 🙌 Complete your sign up to Audit Blog!; mail:mail: 🥳 Free member signup: Reader cnryghmnm75eeb5 |
| `cnryghmlb8150f8` | member label | admin_api:history log; admin_api:labels; binlog:INSERT actions; binlog:INSERT labels; db:actions; db:labels; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/labels.ibd |
| `cnryghmnm75eeb5` | display name | binlog:INSERT members; binlog:INSERT tokens; binlog:UPDATE members; binlog:UPDATE tokens; db:tokens; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd; innodb_raw:ghost/tokens.ibd; innodb_raw:undo_002; mail:mail: 🥳 Free member signup: Reader cnryghmnm75eeb5 |
| `cnryghmnt82415f` | admin note on member | binlog:DELETE members; binlog:UPDATE members; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd |
| `cnryghmrf1a967d` | signup referrer URL (attribution) | binlog:INSERT members_created_events; binlog:INSERT tokens; binlog:UPDATE tokens; db:tokens; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members_created_events.ibd; innodb_raw:ghost/tokens.ibd |
| `cnryghmrp5b351d` | reply body | binlog:INSERT comments; db:comments; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/comments.ibd; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt064f56; public_web:/members/api/comments/post/6af643b21a6add0001bce152/ |
| `cnryghmunaf2c40` | name after self-service profile update | admin_api:history log; binlog:DELETE members; binlog:INSERT actions; binlog:UPDATE members; db:actions; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/members.ibd; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt064f56 |
| `45dbcfda-25d4-499f-9346-d062ac14d728` | member uuid | binlog:DELETE members; binlog:INSERT members; binlog:UPDATE members; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd; innodb_raw:undo_002; mail:mail: ↪️ New reply to your comment on Audit Blog |
| `6af643b71a6add0001bce165` | member id | admin_api:history log; binlog:DELETE members; binlog:DELETE members_labels; binlog:DELETE members_newsletters; binlog:INSERT actions; binlog:INSERT comment_likes; binlog:INSERT comments; binlog:INSERT members; binlog:INSERT members_created_events; binlog:INSERT members_labels; binlog:INSERT members_login_events; binlog:INSERT members_newsletters; binlog:INSERT members_status_events; binlog:INSERT members_subscribe_events; binlog:UPDATE members; content:logs/http___localhost_2368_production.log; db:actions; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/comment_likes.ibd; innodb_raw:ghost/comments.ibd; innodb_raw:ghost/members.ibd; innodb_raw:ghost/members_created_events.ibd; innodb_raw:ghost/members_login_events.ibd; innodb_raw:ghost/members_newsletters.ibd; innodb_raw:ghost/members_status_events.ibd; innodb_raw:ghost/members_subscribe_events.ibd; innodb_raw:undo_001; innodb_raw:undo_002; mail:mail: 🥳 Free member signup: Reader cnryghmnm75eeb5; stdout:docker logs ghost |
| `6af643c81a6add0001bce17f` | comment id | binlog:INSERT comment_likes; binlog:INSERT comments; content:logs/http___localhost_2368_production.log; db:comment_likes; db:comments; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/comment_likes.ibd; innodb_raw:ghost/comments.ibd; innodb_raw:undo_001; innodb_raw:undo_002; public_web:/members/api/comments/post/6af643b21a6add0001bce152/; stdout:docker logs ghost |
| `6af643c81a6add0001bce182` | comment id | binlog:INSERT comments; content:logs/http___localhost_2368_production.log; db:comments; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/comments.ibd; innodb_raw:undo_002; public_web:/members/api/comments/post/6af643b21a6add0001bce152/ |
| `cnryghmema7fe23@example.com` | email | binlog:DELETE members; binlog:INSERT members; binlog:INSERT tokens; binlog:UPDATE members; binlog:UPDATE tokens; db:tokens; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd; innodb_raw:ghost/tokens.ibd; innodb_raw:undo_002; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 🙌 Complete your sign up to Audit Blog!; mail:mail: 🥳 Free member signup: Reader cnryghmnm75eeb5 |
