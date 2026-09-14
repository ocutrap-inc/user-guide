# GPS v1081 documentation update

Date: 2026-09-14. exit-impact: revenue.
Specs: REQ-GPS-BOOT-01, REQ-GPS-REFINE-01, REQ-GPS-SETTINGS-01.

Extend existing draft user-guide PR #133 to match the firmware guide and
requirements in particle-firmware PR #253 and shared contract PR #126.
The combined v1081 binary is staged in Particle without release.

Updated GPS FAQ, settings reference, technical specifications, combined KB and
website mirrors. Explain 30-second startup eligibility / fixed 15-minute window,
prompt first fix / improved estimates, two-minute manual and scheduled refinement,
camera and sleep priority, supported intervals, manual requests while disabled,
no-fix preservation, LTE-M delivery and backup-power limitations. Customer copy
clearly identifies unreleased candidate behavior and older firmware differences.

Validation: changed local GPS links resolve; four website mirrors match source;
PDF builder processes 76 documents and embeds all 41 images with none skipped;
PDF source-hash verification passes (216 pages / 16.2 MB). All four changed
pages render through the website Markdown renderer. Rendered affected pages reviewed for table
layout, clipping and page transitions. No site code or firmware changed.

Keep the PR draft. Website/PDF publication waits for coordinated product rollout
qualification and authorization, including the FW-420 armed offline sleep limit.
No device commands, firmware release, production site deployment or main merge
in this task. GitHub may generate an automatic Vercel preview for PR review.

## Live documentation authorization - 2026-09-14

Graham requested live publication and a link. This supersedes the earlier draft
hold for the documentation only. Keep the unreleased-v1081 notice and all
firmware compatibility/power limitations. Merge current main's documentation
updates, regenerate the combined PDF, pass checks, merge PR #133 and verify
production GPS content. Do not release firmware or send device commands.
