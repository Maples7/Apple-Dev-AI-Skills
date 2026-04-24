# Cleanup

Clean up only the artifacts that are genuinely disposable.

## Usually Safe To Remove

- temporary proof exports regenerated only for review
- downloaded archives created during export
- temporary extraction directories
- validation preview folders used only to spot-check the batch
- one-off scratch files that duplicate information already stored in the manifest or profile

## Usually Worth Keeping

- the project profile and capture manifest
- the automation scripts themselves
- approved raw captures when they are the source for future re-exports
- final exported store assets delivered to the user

## Confirm Before Deleting

Ask before deleting:

- raw screenshots that may be reused later
- the preview/export project when it is the reproducible source of truth
- any prior output tree the user may still need for comparison

## Git Ignore Boundary

- If a generated path should stay local for reruns, review, or caching, do not rely on memory alone; tell the user it likely belongs in the project's `.gitignore`.
- Typical candidates include validation preview folders, local web build caches, export temp directories, downloaded archives, or other generated folders that are reproducible and should not be committed.
- If it is unclear whether a path is source material, a deliverable, or disposable local state, ask the user before editing `.gitignore`.

## End State

After cleanup, the project should still make it obvious:

- where to rerun proof captures
- where to rerun final export
- which folders are source material
- which folders are final deliverables
