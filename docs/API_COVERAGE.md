# Backlog API coverage

Which [Backlog API v2](https://developer.nulab.com/docs/backlog/) endpoints python-backlog implements.

Checked against the official API list on 2026-11-15 (API version 2.120.1). **53 of 152 endpoints (35%) are implemented.** Endpoints without a dedicated method can still be called with `BacklogAPI.invoke_method()`.

`User.add()`, `User.update()` and `User.delete()` call endpoints (`POST users`, `PATCH users/:userId`, `DELETE users/:userId`) that are no longer listed in the official documentation, so they are not counted here.

| Group | Implemented |
|---|---|
| [Activities](#activities) | 0 / 1 |
| [Documents](#documents) | 0 / 10 |
| [Git](#git) | 4 / 14 |
| [Issues](#issues) | 20 / 24 |
| [Notifications](#notifications) | 0 / 4 |
| [Priorities](#priorities) | 0 / 1 |
| [Projects](#projects) | 16 / 48 |
| [Rate limit](#rate-limit) | 1 / 1 |
| [Resolutions](#resolutions) | 0 / 1 |
| [Space](#space) | 1 / 8 |
| [Stars](#stars) | 0 / 2 |
| [Teams](#teams) | 0 / 3 |
| [Users](#users) | 2 / 14 |
| [Watching](#watching) | 0 / 5 |
| [Wiki](#wiki) | 9 / 16 |

## Activities

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `activities/:activityId` | [Get Activity](https://developer.nulab.com/docs/backlog/api/2/get-activity/) | — |

## Documents

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `documents` | [Get document list](https://developer.nulab.com/docs/backlog/api/2/get-document-list/) | — |
| POST | `documents` | [Add document](https://developer.nulab.com/docs/backlog/api/2/add-document/) | — |
| DELETE | `documents/:documentId` | [Delete document](https://developer.nulab.com/docs/backlog/api/2/delete-document/) | — |
| GET | `documents/:documentId` | [Get document](https://developer.nulab.com/docs/backlog/api/2/get-document/) | — |
| GET | `documents/:documentId/attachments/:attachmentId` | [Get document Attachments](https://developer.nulab.com/docs/backlog/api/2/get-document-attachments/) | — |
| GET | `documents/:documentId/comments` | [Get document comment](https://developer.nulab.com/docs/backlog/api/2/get-document-comment/) | — |
| DELETE | `documents/:documentId/tags` | [Remove document tag](https://developer.nulab.com/docs/backlog/api/2/remove-document-tag/) | — |
| POST | `documents/:documentId/tags` | [Add document tag](https://developer.nulab.com/docs/backlog/api/2/add-document-tag/) | — |
| GET | `documents/count` | [Count document](https://developer.nulab.com/docs/backlog/api/2/count-document/) | — |
| GET | `documents/tree` | [Get document tree](https://developer.nulab.com/docs/backlog/api/2/get-document-tree/) | — |

## Git

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `projects/:projectIdOrKey/git/repositories` | [Get List of Git Repositories](https://developer.nulab.com/docs/backlog/api/2/get-list-of-git-repositories/) | `Git.list_git_repositories()` |
| GET | `projects/:projectIdOrKey/git/repositories/:repoIdOrName` | [Get Git Repository](https://developer.nulab.com/docs/backlog/api/2/get-git-repository/) | — |
| GET | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests` | [Get Pull Request List](https://developer.nulab.com/docs/backlog/api/2/get-pull-request-list/) | `Git.list_pull_requests()` |
| POST | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests` | [Add Pull Request](https://developer.nulab.com/docs/backlog/api/2/add-pull-request/) | `Git.add_pull_request()` |
| GET | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/:number` | [Get Pull Request](https://developer.nulab.com/docs/backlog/api/2/get-pull-request/) | — |
| PATCH | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/:number` | [Update Pull Request](https://developer.nulab.com/docs/backlog/api/2/update-pull-request/) | — |
| GET | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/:number/attachments` | [Get List of Pull Request Attachment](https://developer.nulab.com/docs/backlog/api/2/get-list-of-pull-request-attachment/) | — |
| DELETE | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/:number/attachments/:attachmentId` | [Delete Pull Request Attachments](https://developer.nulab.com/docs/backlog/api/2/delete-pull-request-attachments/) | — |
| GET | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/:number/attachments/:attachmentId` | [Download Pull Request Attachment](https://developer.nulab.com/docs/backlog/api/2/download-pull-request-attachment/) | — |
| GET | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/:number/comments` | [Get Pull Request Comment](https://developer.nulab.com/docs/backlog/api/2/get-pull-request-comment/) | — |
| POST | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/:number/comments` | [Add Pull Request Comment](https://developer.nulab.com/docs/backlog/api/2/add-pull-request-comment/) | `Git.add_pull_request_comment()` |
| PATCH | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/:number/comments/:commentId` | [Update Pull Request Comment Information](https://developer.nulab.com/docs/backlog/api/2/update-pull-request-comment-information/) | — |
| GET | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/:number/comments/count` | [Get Number of Pull Request Comments](https://developer.nulab.com/docs/backlog/api/2/get-number-of-pull-request-comments/) | — |
| GET | `projects/:projectIdOrKey/git/repositories/:repoIdOrName/pullRequests/count` | [Get Number of Pull Requests](https://developer.nulab.com/docs/backlog/api/2/get-number-of-pull-requests/) | — |

## Issues

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `issues` | [Get Issue List](https://developer.nulab.com/docs/backlog/api/2/get-issue-list/) | `Issue.list()` |
| POST | `issues` | [Add Issue](https://developer.nulab.com/docs/backlog/api/2/add-issue/) | `Issue.create()` |
| DELETE | `issues/:issueIdOrKey` | [Delete Issue](https://developer.nulab.com/docs/backlog/api/2/delete-issue/) | `Issue.delete()` |
| GET | `issues/:issueIdOrKey` | [Get Issue](https://developer.nulab.com/docs/backlog/api/2/get-issue/) | `Issue.get()` |
| PATCH | `issues/:issueIdOrKey` | [Update Issue](https://developer.nulab.com/docs/backlog/api/2/update-issue/) | `Issue.update()` |
| GET | `issues/:issueIdOrKey/attachments` | [Get List of Issue Attachments](https://developer.nulab.com/docs/backlog/api/2/get-list-of-issue-attachments/) | `Issue.list_issue_attachments()` |
| DELETE | `issues/:issueIdOrKey/attachments/:attachmentId` | [Delete Issue Attachment](https://developer.nulab.com/docs/backlog/api/2/delete-issue-attachment/) | `Issue.delete_issue_attachment()` |
| GET | `issues/:issueIdOrKey/attachments/:attachmentId` | [Get Issue Attachment](https://developer.nulab.com/docs/backlog/api/2/get-issue-attachment/) | `Issue.get_issue_attachment()` |
| GET | `issues/:issueIdOrKey/comments` | [Get Comment List](https://developer.nulab.com/docs/backlog/api/2/get-comment-list/) | `Issue.get_comments()` |
| POST | `issues/:issueIdOrKey/comments` | [Add Comment](https://developer.nulab.com/docs/backlog/api/2/add-comment/) | `Issue.add_comment()` |
| DELETE | `issues/:issueIdOrKey/comments/:commentId` | [Delete Comment](https://developer.nulab.com/docs/backlog/api/2/delete-comment/) | `Issue.delete_comment()` |
| GET | `issues/:issueIdOrKey/comments/:commentId` | [Get Comment](https://developer.nulab.com/docs/backlog/api/2/get-comment/) | `Issue.get_comment()` |
| PATCH | `issues/:issueIdOrKey/comments/:commentId` | [Update comment](https://developer.nulab.com/docs/backlog/api/2/update-comment/) | `Issue.update_comment()` |
| GET | `issues/:issueIdOrKey/comments/:commentId/notifications` | [Get List of Comment Notifications](https://developer.nulab.com/docs/backlog/api/2/get-list-of-comment-notifications/) | `Issue.get_comment_notifications()` |
| POST | `issues/:issueIdOrKey/comments/:commentId/notifications` | [Add Comment Notification](https://developer.nulab.com/docs/backlog/api/2/add-comment-notification/) | `Issue.add_comment_notification()` |
| GET | `issues/:issueIdOrKey/comments/count` | [Count Comment](https://developer.nulab.com/docs/backlog/api/2/count-comment/) | `Issue.count_comments()` |
| GET | `issues/:issueIdOrKey/participants` | [Get Issue Participant List](https://developer.nulab.com/docs/backlog/api/2/get-issue-participant-list/) | — |
| GET | `issues/:issueIdOrKey/relatedIssues` | [Get List of Related Issues](https://developer.nulab.com/docs/backlog/api/2/get-list-of-related-issues/) | — |
| POST | `issues/:issueIdOrKey/relatedIssues` | [Add Related Issue](https://developer.nulab.com/docs/backlog/api/2/add-related-issue/) | — |
| DELETE | `issues/:issueIdOrKey/relatedIssues/:relatedIssueId` | [Remove Related Issue](https://developer.nulab.com/docs/backlog/api/2/remove-related-issue/) | — |
| GET | `issues/:issueIdOrKey/sharedFiles` | [Get List of Linked Shared Files](https://developer.nulab.com/docs/backlog/api/2/get-list-of-linked-shared-files/) | `Issue.list_issue_shared_files()` |
| POST | `issues/:issueIdOrKey/sharedFiles` | [Link Shared Files to Issue](https://developer.nulab.com/docs/backlog/api/2/link-shared-files-to-issue/) | `Issue.link_issue_shared_files()` |
| DELETE | `issues/:issueIdOrKey/sharedFiles/:id` | [Remove Link to Shared File from Issue](https://developer.nulab.com/docs/backlog/api/2/remove-link-to-shared-file-from-issue/) | `Issue.unlink_issue_shared_file()` |
| GET | `issues/count` | [Count Issue](https://developer.nulab.com/docs/backlog/api/2/count-issue/) | `Issue.count()` |

## Notifications

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `notifications` | [Get Notification](https://developer.nulab.com/docs/backlog/api/2/get-notification/) | — |
| POST | `notifications/:id/markAsRead` | [Read Notification](https://developer.nulab.com/docs/backlog/api/2/read-notification/) | — |
| GET | `notifications/count` | [Count Notification](https://developer.nulab.com/docs/backlog/api/2/count-notification/) | — |
| POST | `notifications/markAsRead` | [Reset Unread Notification Count](https://developer.nulab.com/docs/backlog/api/2/reset-unread-notification-count/) | — |

## Priorities

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `priorities` | [Get Priority List](https://developer.nulab.com/docs/backlog/api/2/get-priority-list/) | — |

## Projects

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `projects` | [Get Project List](https://developer.nulab.com/docs/backlog/api/2/get-project-list/) | `Project.list()` |
| POST | `projects` | [Add Project](https://developer.nulab.com/docs/backlog/api/2/add-project/) | `Project.create()` |
| DELETE | `projects/:projectIdOrKey` | [Delete Project](https://developer.nulab.com/docs/backlog/api/2/delete-project/) | — |
| GET | `projects/:projectIdOrKey` | [Get Project](https://developer.nulab.com/docs/backlog/api/2/get-project/) | `Project.get()` |
| PATCH | `projects/:projectIdOrKey` | [Update Project](https://developer.nulab.com/docs/backlog/api/2/update-project/) | `Project.update()` |
| GET | `projects/:projectIdOrKey/activities` | [Get Project Recent Updates](https://developer.nulab.com/docs/backlog/api/2/get-project-recent-updates/) | — |
| DELETE | `projects/:projectIdOrKey/administrators` | [Delete Project Administrator](https://developer.nulab.com/docs/backlog/api/2/delete-project-administrator/) | — |
| GET | `projects/:projectIdOrKey/administrators` | [Get List of Project Administrators](https://developer.nulab.com/docs/backlog/api/2/get-list-of-project-administrators/) | — |
| POST | `projects/:projectIdOrKey/administrators` | [Add Project Administrator](https://developer.nulab.com/docs/backlog/api/2/add-project-administrator/) | — |
| GET | `projects/:projectIdOrKey/categories` | [Get Category List](https://developer.nulab.com/docs/backlog/api/2/get-category-list/) | `Category.list()`, `Project.list_categories()` |
| POST | `projects/:projectIdOrKey/categories` | [Add Category](https://developer.nulab.com/docs/backlog/api/2/add-category/) | `Category.add()`, `Project.add_category()` |
| DELETE | `projects/:projectIdOrKey/categories/:id` | [Delete Category](https://developer.nulab.com/docs/backlog/api/2/delete-category/) | `Category.delete()`, `Project.delete_category()` |
| PATCH | `projects/:projectIdOrKey/categories/:id` | [Update Category](https://developer.nulab.com/docs/backlog/api/2/update-category/) | `Category.update()`, `Project.update_category()` |
| GET | `projects/:projectIdOrKey/customFields` | [Get Custom Field List](https://developer.nulab.com/docs/backlog/api/2/get-custom-field-list/) | `CustomField.list()` |
| POST | `projects/:projectIdOrKey/customFields` | [Add Custom Field](https://developer.nulab.com/docs/backlog/api/2/add-custom-field/) | `CustomField.add()` |
| DELETE | `projects/:projectIdOrKey/customFields/:id` | [Delete Custom Field](https://developer.nulab.com/docs/backlog/api/2/delete-custom-field/) | `CustomField.delete()` |
| PATCH | `projects/:projectIdOrKey/customFields/:id` | [Update Custom Field](https://developer.nulab.com/docs/backlog/api/2/update-custom-field/) | — |
| POST | `projects/:projectIdOrKey/customFields/:id/items` | [Add List Item for List Type Custom Field](https://developer.nulab.com/docs/backlog/api/2/add-list-item-for-list-type-custom-field/) | — |
| DELETE | `projects/:projectIdOrKey/customFields/:id/items/:itemId` | [Delete List Item for List Type Custom Field](https://developer.nulab.com/docs/backlog/api/2/delete-list-item-for-list-type-custom-field/) | — |
| PATCH | `projects/:projectIdOrKey/customFields/:id/items/:itemId` | [Update List Item for List Type Custom Field](https://developer.nulab.com/docs/backlog/api/2/update-list-item-for-list-type-custom-field/) | — |
| GET | `projects/:projectIdOrKey/diskUsage` | [Get Project Disk Usage](https://developer.nulab.com/docs/backlog/api/2/get-project-disk-usage/) | — |
| GET | `projects/:projectIdOrKey/files/:sharedFileId` | [Get File](https://developer.nulab.com/docs/backlog/api/2/get-file/) | — |
| GET | `projects/:projectIdOrKey/files/metadata/:path` | [Get List of Shared Files](https://developer.nulab.com/docs/backlog/api/2/get-list-of-shared-files/) | — |
| GET | `projects/:projectIdOrKey/image` | [Get Project Icon](https://developer.nulab.com/docs/backlog/api/2/get-project-icon/) | — |
| GET | `projects/:projectIdOrKey/issueTypes` | [Get Issue Type List](https://developer.nulab.com/docs/backlog/api/2/get-issue-type-list/) | `Project.list_issue_types()` |
| POST | `projects/:projectIdOrKey/issueTypes` | [Add Issue Type](https://developer.nulab.com/docs/backlog/api/2/add-issue-type/) | `Project.add_issue_type()` |
| DELETE | `projects/:projectIdOrKey/issueTypes/:id` | [Delete Issue Type](https://developer.nulab.com/docs/backlog/api/2/delete-issue-type/) | `Project.delete_issue_type()` |
| PATCH | `projects/:projectIdOrKey/issueTypes/:id` | [Update Issue Type](https://developer.nulab.com/docs/backlog/api/2/update-issue-type/) | `Project.update_issue_type()` |
| GET | `projects/:projectIdOrKey/statuses` | [Get Status List of Project](https://developer.nulab.com/docs/backlog/api/2/get-status-list-of-project/) | — |
| POST | `projects/:projectIdOrKey/statuses` | [Add Status](https://developer.nulab.com/docs/backlog/api/2/add-status/) | — |
| DELETE | `projects/:projectIdOrKey/statuses/:id` | [Delete Status](https://developer.nulab.com/docs/backlog/api/2/delete-status/) | — |
| PATCH | `projects/:projectIdOrKey/statuses/:id` | [Update Status](https://developer.nulab.com/docs/backlog/api/2/update-status/) | — |
| PATCH | `projects/:projectIdOrKey/statuses/updateDisplayOrder` | [Update Order of Status](https://developer.nulab.com/docs/backlog/api/2/update-order-of-status/) | — |
| DELETE | `projects/:projectIdOrKey/teams` | [Delete Project Team](https://developer.nulab.com/docs/backlog/api/2/delete-project-team/) | — |
| GET | `projects/:projectIdOrKey/teams` | [Get Project Team List](https://developer.nulab.com/docs/backlog/api/2/get-project-team-list/) | — |
| POST | `projects/:projectIdOrKey/teams` | [Add Project Team](https://developer.nulab.com/docs/backlog/api/2/add-project-team/) | — |
| DELETE | `projects/:projectIdOrKey/users` | [Delete Project User](https://developer.nulab.com/docs/backlog/api/2/delete-project-user/) | — |
| GET | `projects/:projectIdOrKey/users` | [Get Project User List](https://developer.nulab.com/docs/backlog/api/2/get-project-user-list/) | `Project.list_users()` |
| POST | `projects/:projectIdOrKey/users` | [Add Project User](https://developer.nulab.com/docs/backlog/api/2/add-project-user/) | — |
| GET | `projects/:projectIdOrKey/versions` | [Get Version/Milestone List](https://developer.nulab.com/docs/backlog/api/2/get-version-milestone-list/) | — |
| POST | `projects/:projectIdOrKey/versions` | [Add Version/Milestone](https://developer.nulab.com/docs/backlog/api/2/add-version-milestone/) | — |
| DELETE | `projects/:projectIdOrKey/versions/:id` | [Delete Version](https://developer.nulab.com/docs/backlog/api/2/delete-version/) | — |
| PATCH | `projects/:projectIdOrKey/versions/:id` | [Update Version/Milestone](https://developer.nulab.com/docs/backlog/api/2/update-version-milestone/) | — |
| GET | `projects/:projectIdOrKey/webhooks` | [Get List of Webhooks](https://developer.nulab.com/docs/backlog/api/2/get-list-of-webhooks/) | — |
| POST | `projects/:projectIdOrKey/webhooks` | [Add Webhook](https://developer.nulab.com/docs/backlog/api/2/add-webhook/) | — |
| DELETE | `projects/:projectIdOrKey/webhooks/:webhookId` | [Delete Webhook](https://developer.nulab.com/docs/backlog/api/2/delete-webhook/) | — |
| GET | `projects/:projectIdOrKey/webhooks/:webhookId` | [Get Webhook](https://developer.nulab.com/docs/backlog/api/2/get-webhook/) | — |
| PATCH | `projects/:projectIdOrKey/webhooks/:webhookId` | [Update Webhook](https://developer.nulab.com/docs/backlog/api/2/update-webhook/) | — |

## Rate limit

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `rateLimit` | [Get Rate Limit](https://developer.nulab.com/docs/backlog/api/2/get-rate-limit/) | `BacklogAPI.get_rate_limit()` |

## Resolutions

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `resolutions` | [Get Resolution List](https://developer.nulab.com/docs/backlog/api/2/get-resolution-list/) | — |

## Space

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `space` | [Get Space](https://developer.nulab.com/docs/backlog/api/2/get-space/) | — |
| GET | `space/activities` | [Get Recent Updates](https://developer.nulab.com/docs/backlog/api/2/get-recent-updates/) | — |
| POST | `space/attachment` | [Post Attachment File](https://developer.nulab.com/docs/backlog/api/2/post-attachment-file/) | `Attachment.upload()` |
| GET | `space/diskUsage` | [Get Space Disk Usage](https://developer.nulab.com/docs/backlog/api/2/get-space-disk-usage/) | — |
| GET | `space/image` | [Get Space Logo](https://developer.nulab.com/docs/backlog/api/2/get-space-logo/) | — |
| GET | `space/licence` | [Get Licence](https://developer.nulab.com/docs/backlog/api/2/get-licence/) | — |
| GET | `space/notification` | [Get Space Notification](https://developer.nulab.com/docs/backlog/api/2/get-space-notification/) | — |
| PUT | `space/notification` | [Update Space Notification](https://developer.nulab.com/docs/backlog/api/2/update-space-notification/) | — |

## Stars

| Method | Path | API | python-backlog |
|---|---|---|---|
| POST | `stars` | [Add Star](https://developer.nulab.com/docs/backlog/api/2/add-star/) | — |
| DELETE | `stars/:starId` | [Remove Star](https://developer.nulab.com/docs/backlog/api/2/remove-star/) | — |

## Teams

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `teams` | [Get List of Teams](https://developer.nulab.com/docs/backlog/api/2/get-list-of-teams/) | — |
| GET | `teams/:teamId` | [Get Team](https://developer.nulab.com/docs/backlog/api/2/get-team/) | — |
| GET | `teams/:teamId/icon` | [Get Team Icon](https://developer.nulab.com/docs/backlog/api/2/get-team-icon/) | — |

## Users

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `users` | [Get User List](https://developer.nulab.com/docs/backlog/api/2/get-user-list/) | `User.list()` |
| GET | `users/:userId` | [Get User](https://developer.nulab.com/docs/backlog/api/2/get-user/) | `User.get()` |
| GET | `users/:userId/activities` | [Get User Recent Updates](https://developer.nulab.com/docs/backlog/api/2/get-user-recent-updates/) | — |
| GET | `users/:userId/icon` | [Get User Icon](https://developer.nulab.com/docs/backlog/api/2/get-user-icon/) | — |
| GET | `users/:userId/stars` | [Get Received Star List](https://developer.nulab.com/docs/backlog/api/2/get-received-star-list/) | — |
| GET | `users/:userId/stars/count` | [Count User Received Stars](https://developer.nulab.com/docs/backlog/api/2/count-user-received-stars/) | — |
| GET | `users/:userId/watchings` | [Get Watching List](https://developer.nulab.com/docs/backlog/api/2/get-watching-list/) | — |
| GET | `users/:userId/watchings/count` | [Count Watching](https://developer.nulab.com/docs/backlog/api/2/count-watching/) | — |
| GET | `users/myself` | [Get Own User](https://developer.nulab.com/docs/backlog/api/2/get-own-user/) | — |
| GET | `users/myself/recentlyViewedIssues` | [Get List of Recently Viewed Issues](https://developer.nulab.com/docs/backlog/api/2/get-list-of-recently-viewed-issues/) | — |
| POST | `users/myself/recentlyViewedIssues` | [Add Recently Viewed Issue](https://developer.nulab.com/docs/backlog/api/2/add-recently-viewed-issue/) | — |
| GET | `users/myself/recentlyViewedProjects` | [Get List of Recently Viewed Projects](https://developer.nulab.com/docs/backlog/api/2/get-list-of-recently-viewed-projects/) | — |
| GET | `users/myself/recentlyViewedWikis` | [Get List of Recently Viewed Wikis](https://developer.nulab.com/docs/backlog/api/2/get-list-of-recently-viewed-wikis/) | — |
| POST | `users/myself/recentlyViewedWikis` | [Add Recently Viewed Wiki](https://developer.nulab.com/docs/backlog/api/2/add-recently-viewed-wiki/) | — |

## Watching

| Method | Path | API | python-backlog |
|---|---|---|---|
| POST | `watchings` | [Add Watching](https://developer.nulab.com/docs/backlog/api/2/add-watching/) | — |
| DELETE | `watchings/:watchingId` | [Delete Watching](https://developer.nulab.com/docs/backlog/api/2/delete-watching/) | — |
| GET | `watchings/:watchingId` | [Get Watching](https://developer.nulab.com/docs/backlog/api/2/get-watching/) | — |
| PATCH | `watchings/:watchingId` | [Update Watching](https://developer.nulab.com/docs/backlog/api/2/update-watching/) | — |
| POST | `watchings/:watchingId/markAsRead` | [Mark Watching as Read](https://developer.nulab.com/docs/backlog/api/2/mark-watching-as-read/) | — |

## Wiki

| Method | Path | API | python-backlog |
|---|---|---|---|
| GET | `wikis` | [Get Wiki Page List](https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-list/) | `Wiki.list()` |
| POST | `wikis` | [Add Wiki Page](https://developer.nulab.com/docs/backlog/api/2/add-wiki-page/) | `Wiki.create()` |
| DELETE | `wikis/:wikiId` | [Delete Wiki Page](https://developer.nulab.com/docs/backlog/api/2/delete-wiki-page/) | `Wiki.delete()` |
| GET | `wikis/:wikiId` | [Get Wiki Page](https://developer.nulab.com/docs/backlog/api/2/get-wiki-page/) | `Wiki.get()` |
| PATCH | `wikis/:wikiId` | [Update Wiki Page](https://developer.nulab.com/docs/backlog/api/2/update-wiki-page/) | `Wiki.update()` |
| GET | `wikis/:wikiId/attachments` | [Get List of Wiki attachments](https://developer.nulab.com/docs/backlog/api/2/get-list-of-wiki-attachments/) | `Wiki.list_attachments()` |
| POST | `wikis/:wikiId/attachments` | [Attach File to Wiki](https://developer.nulab.com/docs/backlog/api/2/attach-file-to-wiki/) | `Wiki.add_attachment()` |
| DELETE | `wikis/:wikiId/attachments/:attachmentId` | [Remove Wiki Attachment](https://developer.nulab.com/docs/backlog/api/2/remove-wiki-attachment/) | `Wiki.delete_attachment()` |
| GET | `wikis/:wikiId/attachments/:attachmentId` | [Get Wiki Page Attachment](https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-attachment/) | `Wiki.get_attachment()` |
| GET | `wikis/:wikiId/history` | [Get Wiki Page History](https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-history/) | — |
| GET | `wikis/:wikiId/sharedFiles` | [Get List of Shared Files on Wiki](https://developer.nulab.com/docs/backlog/api/2/get-list-of-shared-files-on-wiki/) | — |
| POST | `wikis/:wikiId/sharedFiles` | [Link Shared Files to Wiki](https://developer.nulab.com/docs/backlog/api/2/link-shared-files-to-wiki/) | — |
| DELETE | `wikis/:wikiId/sharedFiles/:id` | [Remove Link to Shared File from Wiki](https://developer.nulab.com/docs/backlog/api/2/remove-link-to-shared-file-from-wiki/) | — |
| GET | `wikis/:wikiId/stars` | [Get Wiki Page Star](https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-star/) | — |
| GET | `wikis/count` | [Count Wiki Page](https://developer.nulab.com/docs/backlog/api/2/count-wiki-page/) | — |
| GET | `wikis/tags` | [Get Wiki Page Tag List](https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-tag-list/) | — |
