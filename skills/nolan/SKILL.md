---
name: nolan
description: Use when converting horizontal tutorial, talking-head, screen-recording, Ableton, plugin, or music-production videos into polished vertical shorts with smart layout decisions, face/screen crop switching, PiP handling, burned-in subtitle repair, OCR/Whisper/transcript guidance, and dense QC passes such as 0.5s, 0.2s, 0.1s, or per-frame filmstrip review. Trigger for requests like "use Nolan", "not just zoom", "make this horizontal video into a short", "don't change the length", "fix bad zooms", "check every frame", or "create a proper vertical edit".
---

# Nolan

## Core Standard

Make vertical tutorial edits that feel intentionally re-directed, not auto-zoomed.

Default to preserving the full source duration unless the user explicitly asks to shorten or remove content. "Short" means vertical short format, not necessarily a shorter runtime.

Avoid these failure modes:
- Random zoomed room/background with no subject.
- Whole horizontal frame placed on top of a blurred/zoomed duplicate with no purpose.
- Face-focused section with an extra screen/PiP window floating on top.
- Plugin/Ableton section where the face dominates and the actual demonstrated screen is unreadable.
- Burned-in subtitles clipped by vertical cropping or duplicated under new subtitles.

## Layout Rules

Use content-aware layouts:

- **Talking head / face-focused**: make the face the main full-frame subject. Do not show a mini screen/PiP window. Use a stable crop; avoid over-cropping chin/forehead unless the source does it.
- **Plugin, Ableton, DAW, screen demo**: make the plugin/screen the main view. Put the face smaller as PiP near the top when useful, without covering important UI.
- **Split-screen source**: decide the subject from the moment. If the user is explaining UI, screen first with face small. If the user is reacting/summing up, face first with no PiP.
- **Transitions**: short screen-to-face or face-to-screen transitions can stay if they represent actual source content. Patch only if they create incoherent face-plus-random-window frames.
- **Center choice**: for 1920x1080 to 1080x1920 face crops, scale source height to 1920 and crop a 1080-wide window around the face center. Re-evaluate center when the face moves.

## Subtitle Rules

Treat original burned-in subtitles as authoritative when the user says the generated subtitles are wrong. Use OCR from source frames or manually read the source captions before rewriting.

Repair subtitles by covering old/cropped captions and drawing clean text:

- Use a black bottom band for normal captions.
- Use a taller black band only for exact intervals where old burned text rises above the normal band.
- Center text, keep it within the vertical frame, and dynamically shrink long lines.
- Prefer the source caption wording over Whisper when they disagree, unless the user asks for transcript cleanup.
- Verify exact boundary frames; subtitle bugs often happen for only 0.1s at caption changes.

## Workflow

1. **Inspect source**
   - Run `ffprobe` for width, height, frame rate, streams, and duration.
   - Identify whether the video is mostly talking head, screen demo, split screen, or mixed.
   - If speech matters, use Whisper for timing/context. If burned-in captions exist, OCR source crops or inspect source frames directly.

2. **Build first vertical edit**
   - Keep duration and audio unless user explicitly asks to cut.
   - Use deterministic `ffmpeg`/Python frame pipelines for repeatable crop/PiP choices.
   - Copy audio when possible. Re-encode video with sane settings such as `libx264`, `yuv420p`, `crf 18-20`.

3. **QC in two modes**
   - For a cold-start full edit, do a fast sampled pass first, usually one frame every 0.5s, to map the structure: face-only sections, screen-demo sections, split-screen sections, subtitle problem areas, and likely transition boundaries.
   - Once the layout exists, use direct per-frame filmstrips as the final QC: 30 frames per sheet at 60fps covers 0.5s without skipping any frames.
   - For an already-edited file, a small fix, or user-reported bad timestamps, skip sampled passes and go straight to per-frame filmstrips around the suspect ranges or the whole video.
   - Use denser sampled passes such as 0.2s or 0.1s only when per-frame filmstrip generation is impractical. Do not stack 0.5s -> 0.2s -> 0.1s before per-frame if per-frame is feasible.
   - Treat per-frame filmstrips as the authoritative visual QC for split-second layout and subtitle boundary errors.

4. **Patch exact ranges**
   - Patch only the failing ranges; do not rebuild large good sections.
   - Use accurate extraction for verification: `ffmpeg -i input.mp4 -ss 40.0 -frames:v 1 frame.jpg`. `-ss` before `-i` can land on nearby keyframes.
   - For face-only patches, replace the bad output frames with a clean source-based face crop and redraw captions.
   - For subtitle-only patches, keep the layout frame and redraw only the subtitle band.

5. **Verify**
   - Recheck exact patched timestamps at full size.
   - Recheck a few nearby unpatched sections to catch regressions.
   - Run `ffprobe` on final output and report width, height, frame rate, and container duration.
   - Open the final file in Finder when the user wants to inspect it.

## Per-Frame Filmstrip QC

Do not create thousands of loose full-size images for manual review. For a 113s 60fps video, every-frame QC is about 6,790 frames. Pack frames into filmstrip/contact-sheet PNG or JPG files instead.

Default to 30 frames per sheet for 60fps sources. This is equivalent to a 0.5s sheet while still checking every frame, so it replaces sampled 0.2s/0.1s escalation once an edit exists. Keep the sampled 0.5s pass only as a fast planning map for cold-start edits.

Recommended process:

- Generate every-frame filmstrips with `scripts/filmstrip_qc.py`.
- Use 30 frames per sheet for detailed polish. Use 60 frames per sheet only when the review needs to move faster.
- Inspect sheets for abrupt layout jumps, PiP appearing/disappearing in the wrong mode, subtitle clipping, or old subtitle leakage.
- When suspicious, extract exact full-size frames around the timestamp before patching.
- Do not patch from thumbnails alone; thumbnails are for finding suspects.

Example:

```bash
python3 /Users/yalcinefe/.codex/skills/nolan/scripts/filmstrip_qc.py \
  "/path/to/output.mp4" \
  --out-dir /tmp/nolan_qc \
  --every-frame \
  --frames-per-sheet 30 \
  --cols 5
```

For lighter passes:

```bash
python3 /Users/yalcinefe/.codex/skills/nolan/scripts/filmstrip_qc.py \
  "/path/to/output.mp4" \
  --out-dir /tmp/nolan_qc_0p1 \
  --interval 0.1 \
  --frames-per-sheet 30
```

## Patch Pattern

Use this pattern when fixing isolated issues:

- Keep `SOURCE` as the original horizontal file.
- Keep `BASE` as the current vertical output.
- Decode both as raw RGB frames.
- For each timestamp:
  - If the layout is correct but captions are wrong, edit only the caption band on `BASE`.
  - If a face-focused frame has bad PiP/window content, rebuild that frame from `SOURCE` face crop.
  - If a screen-focused frame is correct, do not force face-only just because a transition exists.
- Encode patched frames to a temp file, map audio from `BASE`, then replace `BASE`.

## Communication

Be direct about what QC found:

- "0.1s found real subtitle boundary bugs at X and Y."
- "This suspected frame is legitimate screen content, so I left it alone."
- "I patched exact ranges and verified full-size frames."

When the user is unhappy with the edit, avoid defending the previous pass. Re-run denser QC, identify concrete bad timestamps, patch only those, and verify visually.
