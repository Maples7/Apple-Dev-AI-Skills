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

## End State

After cleanup, the project should still make it obvious:

- where to rerun proof captures
- where to rerun final export
- which folders are source material
- which folders are final deliverables
