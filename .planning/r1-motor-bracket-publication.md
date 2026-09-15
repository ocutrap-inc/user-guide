# R1 motor bracket publication

spec: DOC-25
exit-impact: ops

## Scope

R1-only troubleshooting page at `troubleshooting/adjusting-the-motor-bracket-r1.md`.
The black top motor bracket is removed first and reinstalled last with its two
bolts and washers, confirmed by the owner using the existing assembly diagram
on 2026-09-15. The metal plate stays on the cage: loosen its nuts, slide a small
amount toward the front opening to decrease the gap, then tighten.

The owner's latest approved images take precedence over the earlier arrow
rotation request. The built-in imagegen tool removed obsolete draft labels;
photographic source files were preserved. The existing assembly diagram is reused.

## Validation

- Site typecheck, docs usability tests, AI-search tests and LED tests passed.
- Production site build passed; changed-page local links and assets passed.
- KB PDF rebuilt and source-hash verified; affected pages visually reviewed.
- Website desktop rendering reviewed. Final live verification follows merge.

## Tracking availability

ClickUp Internal Documentation list 901318828640 is the routed tracker. No
ClickUp connector is callable, and the browser opens to a sign-in screen.
No tracker item was created; do not substitute a Linear issue.

## DOC-26 follow-up (2026-09-15)

The owner requested a tightly cropped black-bracket illustration, six mounting
bolts with nuts underneath, and explicit top/inner metal bracket terminology.
The inner bracket has two press-fit inserts protruding into the trap; its flat
side sits on top of the cage. The new crop is used only by the adjustment guide;
the original assembly graphic remains available to existing setup pages.

Image edit: built-in imagegen, crop to the bracket assembly and its two exploded
bolts/washers; remove driver, text and black border, preserving the depicted
hardware. Output: `.gitbook/assets/r1-top-motor-bracket-assembly-cropped.png`.
