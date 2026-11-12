
## User `a`: 13 canary tokens, 5 identifiers

Distinct needles found, per layer and phase:

| layer | t0-before | t1-immediate | t2-after-jobs | t3-after-restart |
|---|---|---|---|---|
| db | 17 | 9 | 9 | 9 |
| binlog | 17 | 17 | 17 | 17 |
| innodb_raw | 17 | 17 | 17 | 17 |
| content | 6 | 7 | 7 | 7 |
| stdout | 2 | 6 | 6 | 6 |
| mail | 3 | 3 | 3 | 3 |
| public_web | 11 | 5 | 5 | 5 |
| admin_api | 16 | 8 | 8 | 8 |
| **any layer** | 17 | 17 | 17 | 17 |

Held by the app itself (db, content, logs, web, admin) after deletion: 8/13 tokens; publicly visible: 4/13.

After deletion (t3-after-restart): 13/13 canary tokens still observable somewhere; 0/13 data types completely removed (none).

Where each surviving needle is, in the last scan:

| needle | what | locations |
|---|---|---|
| `cnryghabib0bf52` | profile bio | binlog:DELETE users; binlog:UPDATE users; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd |
| `cnryghacafa8183` | co-authored post body | admin_api:posts; binlog:INSERT post_revisions; binlog:INSERT posts; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; public_web:/; public_web:/post-cnryghapt499a1e/; public_web:/rss/ |
| `cnryghaci78a4b8` | cover image upload (filename) | binlog:DELETE users; binlog:UPDATE users; content:logs/http___localhost_2368_production.log; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd; stdout:docker logs ghost |
| `cnryghadrd7e8fa` | draft post body | admin_api:posts; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:UPDATE post_revisions; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd |
| `cnryghaem04c294` | email address | binlog:DELETE invites; binlog:DELETE users; binlog:INSERT actions; binlog:INSERT invites; binlog:INSERT users; binlog:UPDATE actions; binlog:UPDATE invites; binlog:UPDATE users; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd; innodb_raw:undo_001; innodb_raw:undo_002; mail:mail: Reset Password; mail:mail: Site Owner has invited you to join Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt499a1e |
| `cnryghaim3d6825` | image uploaded into a post (filename) | admin_api:posts; binlog:INSERT post_revisions; binlog:UPDATE post_revisions; binlog:UPDATE posts; content:images/ (file name); content:logs/http___localhost_2368_production.log; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; public_web:/post-cnryghapt499a1e/; public_web:/rss/; public_web:uploaded image still served; stdout:docker logs ghost |
| `cnryghalo8fd623` | profile location | binlog:DELETE users; binlog:UPDATE users; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd |
| `cnryghanm42f95b` | display name | binlog:DELETE users; binlog:INSERT actions; binlog:INSERT users; binlog:UPDATE actions; binlog:UPDATE users; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd; innodb_raw:undo_002 |
| `cnryghapb903ef7` | published post body | admin_api:posts; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:UPDATE post_revisions; binlog:UPDATE posts; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:undo_002; public_web:/; public_web:/post-cnryghapt499a1e/; public_web:/rss/ |
| `cnryghapi766487` | profile image upload (filename) | binlog:DELETE users; binlog:UPDATE users; content:logs/http___localhost_2368_production.log; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd; stdout:docker logs ghost |
| `cnryghapt499a1e` | published post title | admin_api:history log; admin_api:posts; binlog:INSERT actions; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:UPDATE post_revisions; binlog:UPDATE posts; content:logs/http___localhost_2368_production.log; db:actions; db:post_revisions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:undo_002; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt499a1e; public_web:/; public_web:/post-cnryghapt499a1e/; public_web:/rss/; public_web:/sitemap-posts.xml; stdout:docker logs ghost |
| `cnrygharv08a9a3` | earlier post revision (text later edited away) | binlog:INSERT post_revisions; binlog:INSERT posts; binlog:UPDATE post_revisions; binlog:UPDATE posts; db:post_revisions; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:undo_002 |
| `cnryghawsc72a57` | profile website | binlog:DELETE users; binlog:UPDATE users; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd |
| `6af648eec44a450001c6137a` | user id | admin_api:history log; binlog:DELETE posts_authors; binlog:DELETE roles_users; binlog:DELETE sessions; binlog:DELETE users; binlog:INSERT actions; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:INSERT posts_authors; binlog:INSERT roles_users; binlog:INSERT sessions; binlog:INSERT users; binlog:UPDATE actions; binlog:UPDATE post_revisions; binlog:UPDATE posts; binlog:UPDATE posts_authors; binlog:UPDATE users; content:logs/http___localhost_2368_production.log; db:actions; db:posts; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:ghost/posts_authors.ibd; innodb_raw:ghost/roles_users.ibd; innodb_raw:ghost/users.ibd; innodb_raw:undo_001; innodb_raw:undo_002; stdout:docker logs ghost |
| `6af648f5c44a450001c61384` | post id | admin_api:history log; admin_api:posts; binlog:INSERT actions; binlog:INSERT comments; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:INSERT posts_authors; binlog:INSERT posts_tags; binlog:UPDATE post_revisions; binlog:UPDATE posts; binlog:UPDATE posts_authors; content:logs/http___localhost_2368_production.log; db:actions; db:comments; db:post_revisions; db:posts; db:posts_authors; db:posts_tags; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/comments.ibd; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:ghost/posts_authors.ibd; innodb_raw:ghost/posts_tags.ibd; innodb_raw:undo_001; innodb_raw:undo_002; public_web:/post-cnryghapt499a1e/; public_web:/rss/; stdout:docker logs ghost |
| `6af648f6c44a450001c6138c` | draft post id | admin_api:history log; admin_api:posts; binlog:INSERT actions; binlog:INSERT post_revisions; binlog:INSERT posts; binlog:INSERT posts_authors; binlog:INSERT posts_tags; binlog:UPDATE post_revisions; binlog:UPDATE posts_authors; content:logs/http___localhost_2368_production.log; db:actions; db:post_revisions; db:posts; db:posts_authors; db:posts_tags; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/post_revisions.ibd; innodb_raw:ghost/posts.ibd; innodb_raw:ghost/posts_authors.ibd; innodb_raw:ghost/posts_tags.ibd; innodb_raw:undo_002 |
| `cnryghaem04c294@example.com` | email | binlog:DELETE invites; binlog:DELETE users; binlog:INSERT actions; binlog:INSERT invites; binlog:INSERT users; binlog:UPDATE actions; binlog:UPDATE invites; binlog:UPDATE users; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/users.ibd; innodb_raw:undo_001; innodb_raw:undo_002; mail:mail: Reset Password; mail:mail: Site Owner has invited you to join Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt499a1e |

## User `m`: 8 canary tokens, 6 identifiers

Distinct needles found, per layer and phase:

| layer | t0-before | t1-immediate | t2-after-jobs | t3-after-restart |
|---|---|---|---|---|
| db | 13 | 10 | 10 | 10 |
| binlog | 13 | 13 | 13 | 13 |
| innodb_raw | 13 | 13 | 13 | 13 |
| content | 3 | 3 | 3 | 3 |
| stdout | 2 | 2 | 2 | 2 |
| mail | 8 | 8 | 8 | 8 |
| public_web | 8 | 4 | 4 | 4 |
| admin_api | 8 | 2 | 2 | 2 |
| **any layer** | 14 | 13 | 13 | 13 |

Held by the app itself (db, content, logs, web, admin) after deletion: 6/8 tokens; publicly visible: 2/8.

After deletion (t3-after-restart): 8/8 canary tokens still observable somewhere; 0/8 data types completely removed (none).

Where each surviving needle is, in the last scan:

| needle | what | locations |
|---|---|---|
| `cnryghmcmf64162` | comment body | binlog:INSERT comments; db:comments; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/comments.ibd; mail:mail: 💬 New comment on your post: Post cnryghapt499a1e; public_web:/members/api/comments/post/6af648f5c44a450001c61384/ |
| `cnryghmem89355a` | email address | binlog:DELETE members; binlog:INSERT members; binlog:INSERT tokens; binlog:UPDATE members; binlog:UPDATE tokens; db:tokens; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd; innodb_raw:ghost/tokens.ibd; innodb_raw:undo_002; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 🙌 Complete your sign up to Audit Blog!; mail:mail: 🥳 Free member signup: Reader cnryghmnme53a44 |
| `cnryghmlb7a9622` | member label | admin_api:history log; admin_api:labels; binlog:INSERT actions; binlog:INSERT labels; db:actions; db:labels; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/labels.ibd |
| `cnryghmnme53a44` | display name | binlog:INSERT members; binlog:INSERT tokens; binlog:UPDATE members; binlog:UPDATE tokens; db:tokens; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd; innodb_raw:ghost/tokens.ibd; innodb_raw:undo_002; mail:mail: 🥳 Free member signup: Reader cnryghmnme53a44 |
| `cnryghmnta09e9b` | admin note on member | binlog:DELETE members; binlog:UPDATE members; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd |
| `cnryghmrfe23b78` | signup referrer URL (attribution) | binlog:INSERT members_created_events; binlog:INSERT tokens; binlog:UPDATE tokens; db:tokens; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members_created_events.ibd; innodb_raw:ghost/tokens.ibd |
| `cnryghmrp1f05c8` | reply body | binlog:INSERT comments; db:comments; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/comments.ibd; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt499a1e; public_web:/members/api/comments/post/6af648f5c44a450001c61384/ |
| `cnryghmun3ec6f2` | name after self-service profile update | binlog:DELETE members; binlog:INSERT actions; binlog:UPDATE actions; binlog:UPDATE members; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd; innodb_raw:undo_001; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 💬 New comment on your post: Post cnryghapt499a1e |
| `68399895-cdfe-46e1-b194-7f8b55861425` | member uuid | binlog:DELETE members; binlog:INSERT members; binlog:UPDATE members; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd; innodb_raw:undo_002; mail:mail: ↪️ New reply to your comment on Audit Blog |
| `6af648fac44a450001c61397` | member id | admin_api:history log; binlog:DELETE members; binlog:DELETE members_labels; binlog:DELETE members_newsletters; binlog:INSERT actions; binlog:INSERT comment_likes; binlog:INSERT comments; binlog:INSERT members; binlog:INSERT members_created_events; binlog:INSERT members_labels; binlog:INSERT members_login_events; binlog:INSERT members_newsletters; binlog:INSERT members_status_events; binlog:INSERT members_subscribe_events; binlog:UPDATE actions; binlog:UPDATE members; content:logs/http___localhost_2368_production.log; db:actions; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/actions.ibd; innodb_raw:ghost/comment_likes.ibd; innodb_raw:ghost/comments.ibd; innodb_raw:ghost/members.ibd; innodb_raw:ghost/members_created_events.ibd; innodb_raw:ghost/members_login_events.ibd; innodb_raw:ghost/members_newsletters.ibd; innodb_raw:ghost/members_status_events.ibd; innodb_raw:ghost/members_subscribe_events.ibd; innodb_raw:undo_001; innodb_raw:undo_002; mail:mail: 🥳 Free member signup: Reader cnryghmnme53a44; stdout:docker logs ghost |
| `6af6490bc44a450001c613b1` | comment id | binlog:INSERT comment_likes; binlog:INSERT comments; content:logs/http___localhost_2368_production.log; db:comment_likes; db:comments; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/comment_likes.ibd; innodb_raw:ghost/comments.ibd; innodb_raw:undo_001; innodb_raw:undo_002; public_web:/members/api/comments/post/6af648f5c44a450001c61384/; stdout:docker logs ghost |
| `6af6490bc44a450001c613b4` | comment id | binlog:INSERT comments; content:logs/http___localhost_2368_production.log; db:comments; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/comments.ibd; innodb_raw:undo_002; public_web:/members/api/comments/post/6af648f5c44a450001c61384/ |
| `cnryghmem89355a@example.com` | email | binlog:DELETE members; binlog:INSERT members; binlog:INSERT tokens; binlog:UPDATE members; binlog:UPDATE tokens; db:tokens; innodb_raw:#innodb_redo/#ib_redo12; innodb_raw:ghost/members.ibd; innodb_raw:ghost/tokens.ibd; innodb_raw:undo_002; mail:mail: ↪️ New reply to your comment on Audit Blog; mail:mail: 🙌 Complete your sign up to Audit Blog!; mail:mail: 🥳 Free member signup: Reader cnryghmnme53a44 |
