# Mercurial Tones Native Plug-in Proof Catalog

This catalog is the inherited regression contract for every new native plug-in. Each item states the required behavior, the minimum acceptable proof, and the failure history it prevents. Product-specific requirements may add gates; they may not remove applicable gates here.

## How to use this catalog

- Copy every ID into the product's proof report.
- Assign `PASS`, `FAIL`, `BLOCKED`, or evidence-backed `N/A`.
- Treat “Proof” as the minimum evidence, not an exhaustive recipe.
- Test the candidate actually intended for release, then repeat installation-sensitive checks against the installed artifact.
- Where a regression names a particular host, include that host whenever the product supports it.
- “Learned from” identifies the product history that made the gate necessary; it is not a claim that only that product is affected.

## 0. Evidence and release verdict

- [ ] **EVID-01 — Immutable candidate identity.** Record commit, dirty state, semantic version, build flavor, OS, architecture, formats, compiler, JUCE revision, and artifact hashes. **Proof:** machine-readable manifest plus `git status`. **Prevents:** mixing results from different builds.
- [ ] **EVID-02 — One status per gate.** Every applicable ID is `PASS`, `FAIL`, `BLOCKED`, or justified `N/A`. **Proof:** complete report with no blanks or `UNKNOWN`. **Prevents:** silent omissions.
- [ ] **EVID-03 — Runtime proof is runtime proof.** Source inspection may establish mechanism or N/A, never host behavior. **Proof:** named host procedure, log, screenshot, recording, or automated host test. **Prevents:** declaring focus, renderer, or lifecycle bugs fixed from grep alone.
- [ ] **EVID-04 — Exact red trigger.** Regression tests exercise the historical trigger, not merely a nearby happy path. **Proof:** red-before/green-after test or retained reproducer. **Prevents:** non-reproducing “fixes.”
- [ ] **EVID-05 — Evidence provenance.** Every artifact includes timestamp, product/version/flavor, platform, format, host/version, procedure, result, and path. **Proof:** evidence index. **Prevents:** screenshots and logs that cannot be attributed.
- [ ] **EVID-06 — Honest blockers.** Missing hardware, OS, host, signing identity, or authority is `BLOCKED`, not `PASS` or `N/A`. **Proof:** explicit matrix gap. **Prevents:** incomplete releases presented as verified.
- [ ] **EVID-07 — Structural N/A only.** Cite the source/build fact that makes a gate impossible. **Proof:** exact declaration or absent product capability. **Prevents:** using N/A to hide missing implementation.
- [ ] **EVID-08 — Release blocker rule.** Any applicable failure, blocker, version mismatch, unsigned artifact, dirty release tree, or missing evidence yields `NOT RELEASE READY`. **Proof:** verdict calculation. **Prevents:** subjective sign-off.

## 1. Repository, identity, version, and product hygiene

- [ ] **HYGIENE-01 — Canonical product identity.** Product name, company, plug-in code, manufacturer code, bundle ID, AU type/subtype, executable, support directory, preset directory, installer name, and visible branding are intentional and unique. **Proof:** identity manifest compared with source and artifacts. **Prevents:** cloned-product identities and host cache collisions. **Learned from:** Yasha, Scepter, Vanguard native cutovers.
- [ ] **HYGIENE-02 — Single version truth.** `VERSION`, CMake `project(VERSION)`, `PLUGIN_VERSION`, generated metadata, visible UI, installer/package name, and changelog agree. **Proof:** automated version audit against built VST3/AU/Standalone. **Prevents:** stale moduleinfo, UI, and installer versions. **Learned from:** Tether, Scepter, Yasha.
- [ ] **HYGIENE-03 — Stable identifiers.** Existing parameter IDs, automation order, plug-in codes, and bundle IDs never change in place. New parameters use new IDs. **Proof:** checked-in compatibility manifest diffed against the previous release. **Prevents:** broken sessions and automation.
- [ ] **HYGIENE-04 — AU ParameterID version hints are monotonic.** Each newly added AU parameter receives a newer hint without rewriting older hints. **Proof:** compatibility test and AU metadata inspection. **Prevents:** Logic/AU parameter-layout cache corruption. **Learned from:** Yasha 0.9.22–0.9.23, Scepter FFT parameter fix.
- [ ] **HYGIENE-05 — Legacy artifacts are removed intentionally.** Installer and validation detect stale old bundle names, duplicate format copies, and obsolete support paths. **Proof:** upgrade test from every supported legacy identity. **Prevents:** hosts loading the wrong binary.
- [ ] **HYGIENE-06 — No product-clone residue.** Search for old product names, IDs, URLs, paths, presets, screenshots, and installer labels. **Proof:** deny-list scan with reviewed exceptions. **Prevents:** cross-product contamination.
- [ ] **HYGIENE-07 — Clean generated metadata.** VST3 `moduleinfo.json`, AU plist, Windows version resource, package receipts, and symbol names describe the same candidate. **Proof:** extract from built and installed artifacts. **Prevents:** validator and host-cache mismatches.
- [ ] **HYGIENE-08 — No release diagnostics.** Debug overlays, fallback test paths, environment trial seams, hard-coded developer paths, TODO release blockers, and verbose realtime logging are absent or compile-time excluded. **Proof:** release-binary strings/static audit and runtime smoke. **Prevents:** shipped diagnostics and security bypasses.
- [ ] **HYGIENE-09 — Clean tree and patch hygiene.** `git diff --check` passes; generated/build artifacts and secrets are ignored; the release commit is intentional. **Proof:** clean `git status`, secret scan, diff check. **Prevents:** accidental local state in releases.
- [ ] **HYGIENE-10 — Changelog is evidence-bearing.** It describes behavior, compatibility impact, migration, validation commands/results, known limitations, and intentionally unchanged surfaces. **Proof:** release entry review. **Prevents:** losing regression knowledge between products.

## 2. Build, platform, format, and dependency compatibility

- [ ] **BUILD-01 — Supported format matrix builds.** VST3, AU, and Standalone build in both Release and Beta when advertised. **Proof:** clean builds from the release commit. **Prevents:** validating only a developer target.
- [ ] **BUILD-02 — Supported architecture matrix builds.** macOS universal `arm64+x86_64` and supported Windows architectures are produced as declared. **Proof:** `lipo`, PE, or equivalent architecture inspection. **Prevents:** architecture-only launch failures.
- [ ] **BUILD-03 — Deployment targets are explicit.** macOS deployment target and Windows minimum are compatible with product policy and all UI dependencies. **Proof:** build settings and launch on oldest supported OS. **Prevents:** silent OS floor increases.
- [ ] **BUILD-04 — Standalone entry point is target-scoped.** GUI entry-point definitions do not leak into plug-in targets. **Proof:** link all formats and inspect target definitions. **Prevents:** Windows duplicate/missing entry-point failures.
- [ ] **BUILD-05 — Native-only means native-only.** Native products fail configuration if WebView/browser fallback is accidentally enabled and do not link browser assets. **Proof:** negative configure test and dependency inspection. **Prevents:** accidental WebView regression after native cutover. **Learned from:** Scepter, Yasha, Vanguard.
- [ ] **BUILD-06 — WebView2 linkage is distributable.** WebView products use the intended static/dynamic WebView2 mode, ship required runtime assumptions, and use writable per-product/per-process data. **Proof:** clean Windows machine launch and two-process test. **Prevents:** missing runtime and fixed-folder locks. **Learned from:** Scepter, Yasha.
- [ ] **BUILD-07 — Fonts and essential assets are embedded.** UI does not depend on developer or system font files; finite fallback metrics exist. **Proof:** launch on clean account/machine with asset scan. **Prevents:** missing fonts and NaN layout.
- [ ] **BUILD-08 — Dependencies are pinned and reproducible.** JUCE and third-party revisions, licenses, and build acquisition are recorded. **Proof:** clean checkout build without untracked dependencies. **Prevents:** “works on my machine” releases.
- [ ] **BUILD-09 — Release compiler settings preserve DSP contract.** Fast-math or architecture flags do not change required numerical behavior. **Proof:** reference render/null/digest comparison across configurations. **Prevents:** release-only sound drift. **Learned from:** Dagon 1.0.6.
- [ ] **BUILD-10 — Plugin metadata regeneration is enforced.** A version or identity change fails validation when generated VST3/AU/PE metadata is stale. **Proof:** automated negative test. **Prevents:** old host-visible metadata. **Learned from:** Tether.

## 3. Real-time audio-thread safety and numerical resilience

- [ ] **RT-01 — No heap work in `processBlock`.** No allocation, resizing, string construction, filesystem, network, plug-in construction/destruction, or uncached parameter lookup occurs on the audio thread. **Proof:** source audit plus allocation instrumentation under automation and block changes. **Prevents:** clicks and UI/audio stalls. **Learned from:** Dagon, Shard.
- [ ] **RT-02 — No blocking lock shared with UI.** The audio thread never waits on a lock that the message thread, host callback, scanner, or third-party plug-in can hold. **Proof:** lock-order audit and stress harness. **Prevents:** deadlock/buzz. **Learned from:** Shard 0.9.2.
- [ ] **RT-03 — No host notification under exclusion.** `setLatencySamples`, `updateHostDisplay`, parameter notification, graph rebuild notification, and similar host calls occur outside callback/structure/prepare barriers and are change-checked. **Proof:** reentrant-host harness and lock instrumentation. **Prevents:** second-instance infinite spin. **Learned from:** Janggo 1.2.1.
- [ ] **RT-04 — Exact current sample count.** Every DSP stage receives the current `numSamples`, never the prepared maximum or buffer capacity. **Proof:** mixed sequence including 4096, 100, 333, and 1 sample after prepare at 256. **Prevents:** out-of-bounds and block-dependent audio.
- [ ] **RT-05 — Oversized blocks are chunked safely.** Blocks larger than prepared capacity process in bounded chunks without audio-thread allocation; MIDI positions are sliced correctly. **Proof:** audio/MIDI oversized-block test. **Prevents:** buffer overflow and dropped/misaligned MIDI.
- [ ] **RT-06 — Zero-length calls are harmless.** `numSamples <= 0` and valid zero-channel transitions do not read, clear, divide, or advance invalid state. **Proof:** adversarial process sequence. **Prevents:** host-transition crashes.
- [ ] **RT-07 — Non-finite input is contained.** NaN/Inf input and automation are scrubbed before recursive filters/detectors and cannot poison future blocks. **Proof:** inject non-finite values, then clean signal; all outputs/state remain finite. **Prevents:** persistent silence/explosions.
- [ ] **RT-08 — Denormals are controlled.** Near-zero recursive processing does not create CPU spikes. **Proof:** long silence/subnormal stress with CPU trace. **Prevents:** silence-time CPU surges.
- [ ] **RT-09 — Parameter reads are cached and atomic.** Audio processing uses cached pointers/atomics with bounded conversions, not tree/string access. **Proof:** source and profiler evidence. **Prevents:** hidden allocation and contention. **Learned from:** Dagon 1.0.6.
- [ ] **RT-10 — Time is sample-based.** Attack/release, debounce, transport stop, fades, and polling semantics use seconds/samples, not block counts. **Proof:** block-size invariance across the supported range. **Prevents:** host/block dependent behavior. **Learned from:** Yasha 25 ms transport-stop fix.
- [ ] **RT-11 — Mode/state transitions are click-safe.** Quality, oversampling, bypass, preset, license, and topology changes crossfade or reset intentionally. **Proof:** transition render with peak/discontinuity bound. **Prevents:** clicks and stale tails.
- [ ] **RT-12 — DSP reference behavior is configuration-stable.** Release/Beta and supported architectures meet product null/reference tolerances. **Proof:** committed reference corpus and tolerance rationale. **Prevents:** silent sound changes.

## 4. Channel layouts, buses, sidechain, and MIDI

- [ ] **BUS-01 — Layout support is explicit.** Mono/stereo input/output combinations are accepted or rejected intentionally; unsupported surround is rejected. **Proof:** layout negotiation tests in each format. **Prevents:** host-specific channel assumptions.
- [ ] **BUS-02 — Transitional buffers are safe.** A nominal stereo insert tolerates temporary mono or zero-channel host buffers without invalid clears/reads. **Proof:** transition sequence during prepare/release and layout changes. **Prevents:** Logic/host transition crashes. **Learned from:** Vanguard 0.15.181, Manta 1.0.43.
- [ ] **BUS-03 — Mono dry/wet is valid.** Dry/wet, delay, and bypass helpers are configured for actual channel count. **Proof:** mono render through all Mix and bypass positions. **Prevents:** helper assertions/crashes. **Learned from:** Manta 1.1.6.
- [ ] **BUS-04 — Sidechain uses actual bus buffers.** Processing checks `getBusBuffer` and its actual channels; it does not trust `Bus::isEnabled()` alone. **Proof:** enabled-silent, disabled, mono-routed, and stereo-routed cases. **Prevents:** silent or phantom sidechain. **Learned from:** Scepter, Janggo.
- [ ] **BUS-05 — Sidechain off means off.** A host-created silent auxiliary bus cannot alter processing when sidechain is disabled. **Proof:** null comparison with sidechain bus present but disabled. **Prevents:** unexpected ducking/analysis.
- [ ] **BUS-06 — Sidechain host matrix passes.** Ableton Live, FL Studio, Logic AU, and other declared hosts negotiate the intended default bus state and routing. **Proof:** named-host routing recordings/logs. **Prevents:** format-host layout mismatches.
- [ ] **BUS-07 — Hosted plug-in auxiliaries are bounded.** Plug-in hosts disable or adapt unsupported aux/sidechain buses and map mono/stereo deliberately. **Proof:** hosted plug-in matrix. **Prevents:** child plug-in prepare/load failures. **Learned from:** Shard.
- [ ] **BUS-08 — MIDI slicing and timestamps survive chunking.** MIDI input/output remains sample-accurate across oversized and changing blocks. **Proof:** impulse/note timestamp harness. **Prevents:** timing drift.
- [ ] **BUS-09 — Silence policy is explicit.** `silenceInProducesSilenceOut`, tail length, synth behavior, and analyzer behavior match metadata and reality. **Proof:** validator plus render. **Prevents:** wrong host suspension and tail cuts.

## 5. Latency, bypass, tails, and transport

- [ ] **LAT-01 — Latency is reported early and stably.** Initial construction, prepare, release/reprepare, state restore, and graph rebuild report the correct value without audio-thread mutation. **Proof:** lifecycle latency log in hosts and harness. **Prevents:** misalignment and host reentrancy.
- [ ] **LAT-02 — Quality changes are host-safe.** Use fixed maximum latency with internal alignment or a deferred, change-checked host update outside locks. **Proof:** change quality during playback in multiple instances. **Prevents:** freezes and phase jumps.
- [ ] **LAT-03 — Bypass is latency-compensated.** Host bypass and product bypass align with processed audio. **Proof:** impulse/null test at every latency mode. **Prevents:** comb filtering and timing jumps.
- [ ] **LAT-04 — Bypass delay remains primed.** Normal→bypass, license mute→bypass, and state changes do not expose empty delay state. **Proof:** transition render. **Prevents:** transient timing holes. **Learned from:** Shard 0.7.4/0.9.1, Vanguard 0.15.190.
- [ ] **LAT-05 — Tail behavior is intentional.** Transport stop, bypass, preset restore, quality switch, and release/prepare preserve or clear tails according to contract. **Proof:** impulse-tail scenario per transition. **Prevents:** chopped or stale audio.
- [ ] **LAT-06 — Transport discontinuity is bounded.** Loop, seek, stop/start, tempo change, and missing playhead info cannot create invalid time or runaway state. **Proof:** host transport stress. **Prevents:** stuck envelopes and NaNs.
- [ ] **LAT-07 — Host standby/suspend resumes cleanly.** Suspend/reprepare does not masquerade as editor destruction or permanent reset. **Proof:** host standby and quality-change release/prepare with editor open. **Prevents:** frozen UI/state. **Learned from:** Dagon 1.0.31.

## 6. Parameters, automation, state, migration, and undo

- [ ] **STATE-01 — State schema is versioned.** Current state carries a schema version and tolerantly parses older/newer optional fields. **Proof:** migration fixtures. **Prevents:** brittle session restore.
- [ ] **STATE-02 — Current, legacy, sparse, corrupt, and forward state are tested.** Complete current state may fast-path only when all live parameters are present; sparse/legacy state resets/migrates intentionally. **Proof:** fixture matrix. **Prevents:** hybrid stale states.
- [ ] **STATE-03 — Corrupt state is non-destructive.** Invalid types, arrays, permutations, non-finite values, truncation, and malformed text are rejected or sanitized without disturbing valid live state. **Proof:** fuzz/property tests. **Prevents:** crashes and silent corruption.
- [ ] **STATE-04 — Silent restore updates DSP atomics.** APVTS/raw parameter atomics and dependent caches synchronize even when preset/session load avoids host notifications. **Proof:** state restore followed by audio render without UI. **Prevents:** UI/state saying one value while DSP uses another. **Learned from:** Manta 0.5.51, Vanguard 0.15.176.
- [ ] **STATE-05 — Parameter contracts are stable.** ID, name, range, skew, step, default, unit, enum choices, automatable flag, and version hint are compared with prior releases. **Proof:** machine-readable manifest regression. **Prevents:** session/automation drift.
- [ ] **STATE-06 — Host gestures are balanced.** Continuous edits emit one begin/end gesture and bounded value changes; discrete controls notify once. **Proof:** automation recorder test. **Prevents:** broken undo and automation floods.
- [ ] **STATE-07 — Non-finite automation is finite.** NaN/Inf/out-of-range host values clamp safely and never poison UI/DSP. **Proof:** fuzz test. **Prevents:** recursive state corruption.
- [ ] **STATE-08 — Project state and global preferences have authority rules.** Project-restored values win over global seeds; legacy projects without a field follow the documented fallback. **Proof:** fresh/current/legacy reopen matrix. **Prevents:** one session overwriting another's UI or DSP choices.
- [ ] **STATE-09 — Programmatic restore is not user input.** Restoring a panel, zoom, or preset does not rewrite global preference or dirty state unless intended. **Proof:** preference/state diff. **Prevents:** accidental persistence feedback loops.
- [ ] **STATE-10 — Default program is named.** Hosts and validators receive a valid program count/name such as `Default`. **Proof:** official validator and program API test. **Prevents:** validator failures. **Learned from:** Janggo.
- [ ] **STATE-11 — Undo is user-meaningful.** One drag is one undo; destructive actions are recoverable; linking controls or changing modes does not erase history or rewrite unrelated values. **Proof:** interaction/undo sequence. **Prevents:** hostile editing behavior.
- [ ] **STATE-12 — Mode/profile selection preserves user controls unless specified.** Profiles do not silently rewrite unrelated Target/Pull/Focus/Mix/Output-style parameters. **Proof:** before/after parameter snapshot. **Prevents:** preset modes destroying user intent. **Learned from:** Tether.
- [ ] **STATE-13 — Runtime caches follow restored state.** Meters, curves, visualizations, latency, topology, tails, and derived DSP are refreshed or reset consistently after load. **Proof:** UI/audio state comparison immediately after restore. **Prevents:** stale visuals and sound.

## 7. Presets and filesystem safety

- [ ] **PRESET-01 — Factory Default and project state are distinct.** Loading Default has explicit semantics and does not inherit hidden state. **Proof:** dirty-state and full-parameter comparison. **Prevents:** non-reproducible defaults.
- [ ] **PRESET-02 — Preset apply is batched.** Skip unchanged parameter writes, bound host notifications, and call host-display update once where needed. **Proof:** notification counter. **Prevents:** automation/UI storms. **Learned from:** Shard 0.11.1, Vanguard 0.15.164.
- [ ] **PRESET-03 — Names cannot escape the preset root.** Slash, backslash, dot segments, Unicode separators, reserved names, long names, and symlink cases remain inside the intended directory. **Proof:** hostile-name path property test. **Prevents:** path traversal. **Learned from:** Shard 0.11.1.
- [ ] **PRESET-04 — File writes are atomic.** Write temporary, flush, validate, and replace; a crash or disk failure leaves the previous preset intact. **Proof:** interrupted-write simulation. **Prevents:** truncated presets.
- [ ] **PRESET-05 — Corrupt preset leaves live state intact.** Parsing and validation complete before adoption. **Proof:** checksum of state before/after invalid load. **Prevents:** partial application.
- [ ] **PRESET-06 — Preset discovery is not realtime or per-frame.** Directory scan and JSON parsing happen on explicit refresh/background path with revision caching. **Proof:** profiler and code path trace. **Prevents:** UI choking. **Learned from:** Vanguard 0.15.159–0.15.166.
- [ ] **PRESET-07 — Async chooser/menu callbacks are lifetime-safe.** Use weak/safe ownership, dismiss before teardown, and prevent overlapping operations. **Proof:** open chooser/menu then close editor repeatedly. **Prevents:** use-after-free. **Learned from:** Manta, Janggo.
- [ ] **PRESET-08 — User and factory locations are correct.** Paths are platform-appropriate, writable, migrated, and do not collide between products/flavors. **Proof:** clean-user install and upgrade. **Prevents:** missing or cross-product presets.

## 8. Host focus, keyboard, menus, modals, and text input

- [ ] **FOCUS-01 — Editor does not steal focus on open.** Creating/showing an editor leaves DAW transport and shortcuts responsive unless an explicit product shortcut requires focus. **Proof:** open editor and immediately press Space and key host shortcuts in every declared host. **Prevents:** host focus theft.
- [ ] **FOCUS-02 — Passive controls never grab keyboard focus.** Knob, slider, canvas, graph, meter, drag surface, and hosted-window mouse wrappers are mouse-focus only. **Proof:** click/drag each then exercise host shortcuts. **Prevents:** transport capture. **Learned from:** Shard 0.14.11, Manta 1.0.9–1.0.10.
- [ ] **FOCUS-03 — Search/text focus is intentional.** Text fields gain focus only on direct click or explicit shortcut, not during construction or broad panel clicks. **Proof:** tab/click matrix. **Prevents:** aggressive keyboard capture. **Learned from:** Shard 0.14.10.
- [ ] **FOCUS-04 — Dropdown selection returns focus to host.** After every native popup and custom dropdown selection/dismissal, DAW shortcuts work. **Proof:** select every menu item, dismiss with Escape/outside click, then test host keys. **Prevents:** menu-owned focus leaks.
- [ ] **FOCUS-05 — WebView controls hand focus back correctly.** After non-text click/select, native handoff targets the top-level host peer; INPUT/TEXTAREA/SELECT/OPTION interactions are excluded until editing/dropdown is complete. **Proof:** Windows WebView2 and macOS host matrix. **Prevents:** child-HWND focus capture and instantly closing selects. **Learned from:** Scepter 0.1.54/0.1.86/0.1.87, Yasha 0.4.21.
- [ ] **FOCUS-06 — Windows WebView2 uses real HWND handoff.** JUCE component focus release alone is not accepted as proof; `SetFocus` or equivalent reaches the correct top-level peer. **Proof:** foreground/focus HWND logging plus Ableton/FL test. **Prevents:** persistent WebView2 focus.
- [ ] **FOCUS-07 — Intentional shortcuts are scoped exceptions.** If the plug-in supports Space/key triggers, focus is requested only after explicit interaction, documented, reversible, and does not break host controls when inactive. **Proof:** shortcut ownership matrix. **Prevents:** turning a deliberate shortcut into global focus theft. **Learned from:** Aegis.
- [ ] **FOCUS-08 — Modals request focus only when showable.** License/name/text dialogs wait for a real peer, non-zero bounds, visibility, and parent hierarchy; retry asynchronously with safe ownership. **Proof:** fresh open, restored hidden window, and 0x0 construction. **Prevents:** silently failed or host-racing focus. **Learned from:** Manta 1.1.2, Vanguard 0.15.184.
- [ ] **FOCUS-09 — No automatic Windows TextEditor focus during wrapper construction.** Defer or require click to avoid IME/wrapper races. **Proof:** Windows host open/close stress. **Prevents:** wrapper focus deadlock/race. **Learned from:** Vanguard 0.15.184.
- [ ] **FOCUS-10 — One popup/modal at a time.** Existing popups are dismissed before another opens and before license overlay or editor teardown. **Proof:** rapid menu/modal switching and close. **Prevents:** orphan peers and stale focus.
- [ ] **FOCUS-11 — Dialogs are tracked and dismissed.** Name dialogs, file choosers, alert windows, popup menus, and key handlers have explicit ownership and teardown. **Proof:** open each then destroy editor/processor. **Prevents:** Ableton input retained after editor close. **Learned from:** Janggo 1.4.1.
- [ ] **FOCUS-12 — Multi-window focus is sane.** Detached hosted editors ignore key presses unless intended, close before processors die, and never seize DAW transport. **Proof:** open several detached windows and switch/close rapidly. **Prevents:** stale child windows and key theft. **Learned from:** Shard.
- [ ] **FOCUS-13 — Accessibility and tab traversal are bounded.** Tab order reaches interactive text/licensing controls without trapping the host; Escape dismisses transient UI. **Proof:** keyboard-only traversal. **Prevents:** inaccessible or inescapable focus.

## 9. Editor lifecycle, asynchronous work, and multi-instance resilience

- [ ] **LIFE-01 — Explicit shutdown begins before child destruction.** Stop new work, hide/disable input, dismiss transient UI, and mark shutdown before components disappear. **Proof:** ordered teardown instrumentation. **Prevents:** callbacks entering partially destroyed UI. **Learned from:** Manta 1.0.46 onward.
- [ ] **LIFE-02 — All timers and workers stop and join.** Parent/child timers, scanner, activation, render, analysis, and file workers have bounded cancellation and joins. **Proof:** repeated create/destroy with thread count baseline. **Prevents:** use-after-free and process hang.
- [ ] **LIFE-03 — Async callbacks use safe ownership.** `SafePointer`, `WeakReference`, cancellation token, or processor-owned result adoption covers every AsyncUpdater, callAsync, menu, chooser, timer, and network callback; no raw `this`. **Proof:** static callback inventory plus close-during-callback stress. **Prevents:** UAF. **Learned from:** Manta, Janggo, Vanguard.
- [ ] **LIFE-04 — Callback fields detach before targets die.** LookAndFeel pointers, listeners, lambdas, hosted child references, model callbacks, and native child views are cleared in safe order. **Proof:** sanitizer/lifecycle test. **Prevents:** late virtual calls into dead objects.
- [ ] **LIFE-05 — Processor-owned work survives editor closure appropriately.** Licensing or audio-model adoption completes without requiring the initiating editor. **Proof:** start work, close editor, verify processor result and reopen. **Prevents:** lost activation or corrupt state. **Learned from:** Shard 0.9.1.
- [ ] **LIFE-06 — `releaseResources` is not editor destruction.** Audio suspend/reprepare does not clear editor-open policy, UI revisions, or lifecycle ownership incorrectly. **Proof:** release/prepare while editor remains visible. **Prevents:** frozen/missing visualization. **Learned from:** Dagon 1.0.31.
- [ ] **LIFE-07 — Rapid lifecycle loop is clean.** At least 25 create/show/interact/hide/destroy cycles cover all menus, panels, dialogs, zooms, and license states under ASan/TSan where available. **Proof:** lifecycle runner log. **Prevents:** accumulated leaks and rare teardown crashes. **Learned from:** Manta.
- [ ] **LIFE-08 — Two or more editors remain responsive.** Open multiple instances/editors, automate, resize, switch quality, and close in different orders. **Proof:** host stress with audio continuity and message-thread responsiveness. **Prevents:** second-instance freezes. **Learned from:** Janggo 1.2.1/1.4.1.
- [ ] **LIFE-09 — Hidden editors consume no decorative work.** Hidden/closed panels stop timers and rendering rather than wake-and-return; required model/control updates remain correct. **Proof:** profiler comparing open/hidden/closed. **Prevents:** background CPU. **Learned from:** Manta 1.0.44, Vanguard.
- [ ] **LIFE-10 — Native child views detach before reset.** WebView, hosted editor, OS peer, and detached window teardown order is explicit. **Proof:** close/reopen stress in host. **Prevents:** native child use-after-free. **Learned from:** Vanguard.
- [ ] **LIFE-11 — Scanner and hosted objects have bounded ownership.** Scanner cancellation kills/joins child work; third-party processors are not destroyed under the host callback lock. **Proof:** cancel scan and close host during slow/broken plug-in load. **Prevents:** shutdown hangs/deadlocks. **Learned from:** Shard 0.7.4/0.9.2.
- [ ] **LIFE-12 — Shared caches have lifetime ownership.** Fonts, images, paths, and shared models are ref-counted or immutable; one editor closing cannot invalidate another. **Proof:** multi-editor close-order test. **Prevents:** cross-instance UAF.

## 10. UI throughput, choking, repaint, and pressure behavior

- [ ] **PERF-01 — No work-per-mouse-event storm.** Dragging coalesces model changes and caps expensive rebuild/repaint cadence. **Proof:** drag trace with repaint and rebuild counts. **Prevents:** choking UI. **Learned from:** Dagon 1.0.3/1.0.5.
- [ ] **PERF-02 — Expensive visuals are dirty/revision driven.** Frost, spectra, shadows, paths, preset lists, and raster caches rebuild only when inputs change. **Proof:** idle and drag instrumentation. **Prevents:** redundant frame work.
- [ ] **PERF-03 — One display revision advances once.** Rebuilding a cache cannot double-advance animation, smoothing, or analysis state. **Proof:** revision counter test. **Prevents:** display-speed drift. **Learned from:** Dagon 1.0.20.
- [ ] **PERF-04 — Frame rate and render budget are explicit.** Defaults suit each platform; pressure mode is measurable and bounded. **Proof:** frame-time percentile and CPU budget in one/two/many editors. **Prevents:** DAW UI starvation.
- [ ] **PERF-05 — Pressure shedding preserves information.** Drop shadows, gradients, density, fill, and decorative animation may degrade; control automation and meaningful signal geometry may not disappear. **Proof:** pressure-mode screenshots plus functional trace. **Prevents:** smooth but misleading UI. **Learned from:** Janggo 1.4.1/1.4.2.
- [ ] **PERF-06 — Identical values do not repaint.** Meter/control updates suppress repaint when the rendered value/revision is unchanged. **Proof:** idle repaint counter. **Prevents:** constant message-thread load.
- [ ] **PERF-07 — Buffers and paths are reused.** No large image/path/container allocation per frame; cache resolution matches current physical scale. **Proof:** allocation profile. **Prevents:** allocator churn. **Learned from:** Dagon 1.0.20, Janggo.
- [ ] **PERF-08 — GUI access to realtime analysis is non-blocking.** Message thread uses snapshots or bounded try-lock/skip; reprepare cannot free analysis memory while painting. **Proof:** rapid sample-rate/block reprepare during analyzer UI. **Prevents:** deadlock/UAF. **Learned from:** Shard.
- [ ] **PERF-09 — Static chrome is cached without staleness.** Cached backgrounds/fonts/shadows invalidate on size, scale, theme, and state changes. **Proof:** invalidation matrix. **Prevents:** wrong-size or stale rendering.
- [ ] **PERF-10 — Open-sync fallback is bounded.** Initial UI synchronization is one-shot/capped and then revision-driven, not a perpetual full refresh. **Proof:** refresh counter over idle minute. **Prevents:** hidden 30 Hz work. **Learned from:** Vanguard 0.15.159–0.15.166.
- [ ] **PERF-11 — Web/native transport has backpressure.** WebView evaluate/bridge messages are batched, bounded, and recover when callbacks are dropped. **Proof:** message flood and watchdog scenario. **Prevents:** WebView queue choke. **Learned from:** Scepter/Yasha.
- [ ] **PERF-12 — UI remains responsive under audio stress.** Worst supported sample rate/block, automation, multi-instance, resize, and meters do not block host input. **Proof:** message-thread latency trace and real-host interaction recording.

## 11. Zoom, resizing, DPI, and session memory

- [ ] **ZOOM-01 — Every advertised zoom is usable.** Exercise all choices, including 50/75/100/125/150/200% when offered. **Proof:** screenshots and interaction tests at each level. **Prevents:** untested intermediate scales.
- [ ] **ZOOM-02 — Geometry scales natively.** Layout, fonts, strokes, menu rows, panels, tooltips, and hit targets scale proportionally; do not use a whole-component transform or bitmap stretch as the implementation. **Proof:** 0.5x/1x/2x rendering and hit tests. **Prevents:** blurry or misaligned UI. **Learned from:** Manta 1.0.59–1.0.65.
- [ ] **ZOOM-03 — Size is clamped to usable display.** Initial, restored, and selected sizes fit the current display work area while maintaining aspect ratio and a functional minimum. **Proof:** smallest supported display, dock/menu/taskbar variants, multi-monitor move. **Prevents:** off-screen controls. **Learned from:** Janggo, Wavetable Editor, Tether.
- [ ] **ZOOM-04 — Construction-time 0x0 is ignored.** Transient empty bounds cannot overwrite a valid preference or state. **Proof:** forced 0x0 constructor/resized sequence. **Prevents:** forgotten/collapsed zoom. **Learned from:** Janggo 1.1.
- [ ] **ZOOM-05 — Per-project size restores.** Save a host project at non-default size, close host, reopen, and recover that instance size. **Proof:** host session roundtrip. **Prevents:** session zoom forgotten.
- [ ] **ZOOM-06 — New instances remember global user size.** After user resize/zoom and close, a fresh instance starts with the last global preference. **Proof:** new-project/new-instance test. **Prevents:** repetitive resizing. **Learned from:** Janggo 1.2.
- [ ] **ZOOM-07 — Project size wins over global seed.** Change global preference in another instance, then reopen a saved project; its explicit project size wins. **Proof:** precedence matrix. **Prevents:** global preference corrupting sessions.
- [ ] **ZOOM-08 — Legacy projects without size are deterministic.** Document and test whether global seed or product default applies; do not misclassify legacy restore as user resize. **Proof:** legacy fixture. **Prevents:** inconsistent migrations.
- [ ] **ZOOM-09 — Preference writes are debounced and flushed.** Do not write disk on every resize; flush after debounce, explicit save, and quick close/destructor. **Proof:** write counter and immediate-close test. **Prevents:** I/O storms and lost final size. **Learned from:** Janggo 1.2, Vanguard 0.15.205.
- [ ] **ZOOM-10 — Programmatic panel changes preserve scale.** Expand/collapse/advanced panels and host resize callbacks retain selected scale and do not infer 100% from transient bounds. **Proof:** panel toggle at every zoom plus reopen. **Prevents:** zoom reset. **Learned from:** Vanguard 0.15.187.
- [ ] **ZOOM-11 — Scale-dependent caches rerasterize.** Images, shadows, paths, fonts, and native child bounds invalidate at scale/DPI changes. **Proof:** live monitor-DPI move and pixel inspection. **Prevents:** blurry/stale caches.
- [ ] **ZOOM-12 — Logical and backing pixels are not confused.** Web/native drawing uses logical CSS/component dimensions while accounting for DPR exactly once. **Proof:** Retina/HiDPI screenshots and coordinate assertions. **Prevents:** off-screen playheads and labels. **Learned from:** Scepter.
- [ ] **ZOOM-13 — Paint and hit geometry share a source.** Knob/control painting and interaction derive from the same layout/transform function. **Proof:** center/edge hit grid at every zoom. **Prevents:** controls visually moving away from hit targets. **Learned from:** Aegis 0.1.208.
- [ ] **ZOOM-14 — Host resize constraints are stable.** Fixed aspect, minimum/maximum, host-initiated resize, and reopening do not oscillate or recursively resize. **Proof:** drag corners in each host and inspect callback count.

## 12. Rendering truth, visual robustness, and UI contracts

- [ ] **RENDER-01 — Real renderer is tested.** Run in actual DAW renderer paths on macOS and Windows; software snapshots alone do not pass. **Proof:** host screenshots/video at normal, invalidated-cache, and low-CPU/pressure paths. **Prevents:** CoreGraphics/Metal/WebView-only failures.
- [ ] **RENDER-02 — Opaque base coverage is unconditional.** Critical panels have a vector/base fill even if clipped image/texture blits fail; textured fills and veils are additive. **Proof:** forced cache miss/clipping scenario. **Prevents:** black/transparent holes. **Learned from:** Shard, Manta, Dagon.
- [ ] **RENDER-03 — Every control is visibly and interactively aligned.** Bounding boxes, labels, values, hover, drag, disabled state, and tooltip anchors agree at all scales. **Proof:** automated geometry plus screenshots.
- [ ] **RENDER-04 — Dropdowns and selectable toggles remain distinct.** Menu styling changes do not accidentally restyle segmented controls, Flow/Sync toggles, padding, or panel geometry. **Proof:** before/after UI snapshot scoped to intended control classes. **Prevents:** cross-control styling regressions. **Learned from:** Tether.
- [ ] **RENDER-05 — Tooltips explain current selection.** Mode dropdown tooltip includes the selected mode's behavior, not only the generic control name; it updates immediately. **Proof:** hover each selection. **Prevents:** opaque modes. **Learned from:** Tether.
- [ ] **RENDER-06 — Signal visualizations are truthful.** Input/dry and output/wet traces come from actual signals or the identical production processing path; estimators are forbidden when the UI promises measured signal. **Proof:** captured buffers compared with plotted history and bypass/null cases. **Prevents:** misleading displays. **Learned from:** Tether and Aegis estimator removal.
- [ ] **RENDER-07 — Path connectivity is explicit.** Do not use `Path::isEmpty()` to detect a move-to-only started path; retain a started flag/shared geometry helper. **Proof:** connectivity unit test and pixel guard. **Prevents:** disconnected waveform segments. **Learned from:** Janggo 1.4.2.
- [ ] **RENDER-08 — Gradients encode intentional meaning only.** Floor/ceiling/target shading does not imply processing that DSP does not perform; unwanted dark bands are absent. **Proof:** design-contract screenshot review. **Prevents:** misleading dynamics UI. **Learned from:** Tether.
- [ ] **RENDER-09 — First paint is complete.** No white/blank control, missing cached text, wrong alpha, or one-frame 0x0 layout appears on first open. **Proof:** first-frame capture from clean process. **Prevents:** initialization flashes.
- [ ] **RENDER-10 — Caller alpha is preserved.** Theme helpers do not overwrite a supplied translucent color with an enabled-state alpha of 1; disabled/hover alpha composes intentionally. **Proof:** pixel/color unit test and first-run screenshot. **Prevents:** solid-white trial buttons. **Learned from:** Tether 0.4.3 first-run review.
- [ ] **RENDER-11 — Control text remains legible and finite.** Long/localized labels, negative values, high DPI, unavailable fonts, and unusual state never clip into controls or yield invalid metrics. **Proof:** text stress snapshots.
- [ ] **RENDER-12 — UI self-snapshots have pixel guards.** Golden comparisons include meaningful regions and fail on blank/transparent output, not merely file creation. **Proof:** deliberate mutation test.
- [ ] **RENDER-13 — Meters and history have defined timing.** Display update/smoothing is independent of block size, handles hidden/reopen, and does not advance twice. **Proof:** timing and lifecycle tests.

## 13. Trial, licensing, activation, and security

- [ ] **LIC-01 — Release first-run path is exercised.** Clean all product license/trial state, launch Release, and capture first frame plus all interactions. Beta is not accepted because it may bypass licensing. **Proof:** clean-account recording/screenshots. **Prevents:** hidden first-run failures.
- [ ] **LIC-02 — Overlay visibility ownership is correct.** Parent visibility wiring does not override the overlay's internal trial/licensed/expired state. **Proof:** first-run, dismissed, licensed, expired, and reopen matrix. **Prevents:** permanently shown/hidden overlay. **Learned from:** Tether vs Shard wiring review.
- [ ] **LIC-03 — Every license control is readable and reachable.** Trial button, activate, purchase, key field, errors, dismissal, settings recovery, and expired state have correct text, opacity, hit bounds, and focus. **Proof:** UI snapshots and click automation. **Prevents:** white/invisible or unreachable actions.
- [ ] **LIC-04 — Trial badge remains recoverable.** After dismissal, settings can reopen license/trial information and activation. **Proof:** dismiss/reopen flow. **Prevents:** users losing activation UI.
- [ ] **LIC-05 — Offline signature verification is canonical.** Producer and plug-in share byte-for-byte canonical fixtures; valid, tampered, malformed, wrong product, expired/versioned, zero-signature, non-finite, and fractional cases are tested. **Proof:** cross-language fixtures. **Prevents:** divergent verification and parser exploits. **Learned from:** Shard.
- [ ] **LIC-06 — License adoption is transactional.** Snapshot old file/state, write, reread, parse, verify, then adopt; restore/delete on any failure. **Proof:** injected I/O and verification failures. **Prevents:** bricked or falsely licensed state.
- [ ] **LIC-07 — Trial time fails closed safely.** Earliest trusted anchor survives deletion/rollback; clock rollback and future timestamps follow documented policy; test seams are absent from Release. **Proof:** clock/file adversarial matrix and binary scan. **Prevents:** trial farming and accidental lockout.
- [ ] **LIC-08 — Activation work is processor-owned and joined.** Closing the editor cannot lose a valid activation; UI callbacks remain safe and reentry is disabled. **Proof:** close-during-activation and reopen. **Prevents:** UAF/lost license. **Learned from:** Shard 0.9.1.
- [ ] **LIC-09 — Key normalization matches backend.** Whitespace/case/serial-only rules and structured errors are explicit and tested. **Proof:** input corpus against staging/offline mock. **Prevents:** valid-key rejection.
- [ ] **LIC-10 — Purchase and activation endpoints are live.** URLs, TLS, timeout, offline errors, and retry behavior are production-correct. **Proof:** clean-machine network test and failure simulation.
- [ ] **LIC-11 — Native cutover includes complete licensing UI.** Processor enforcement cannot ship without the matching overlay/settings path. **Proof:** release UI state matrix. **Prevents:** gated product with no activation route. **Learned from:** Manta 1.1.0.
- [ ] **LIC-12 — License audio policy preserves timing safety.** Trial expiry/mute does not poison latency-compensated bypass, delay priming, tails, or state. **Proof:** transition render. **Prevents:** pops and PDC jumps.
- [ ] **LIC-13 — Modal key handlers do not accumulate.** Reopening purchase/activation overlays installs exactly one handler/listener and removes it on close. **Proof:** listener count and repeated flow.
- [ ] **LIC-14 — Flavor separation is explicit.** Beta/Release license bypasses, branding, endpoints, bundle IDs, and support paths follow policy without contaminating user licenses. **Proof:** flavor comparison.

## 14. Plug-in-host/scanner products (when applicable)

- [ ] **HOSTER-01 — Scanner cancellation is bounded.** Scanner owns/joins workers, polls cancellation, terminates child processes, and cannot keep the app alive. **Proof:** cancel during a hung plug-in scan. **Learned from:** Shard 0.7.4.
- [ ] **HOSTER-02 — Delayed scan callbacks are weak.** Automatic/rescan work cannot target a destroyed editor/model. **Proof:** schedule then immediately close. **Prevents:** UAF.
- [ ] **HOSTER-03 — Child plug-in creation is split phase.** Expensive construction/prepare happens outside callback locks; pointer/graph commit is short and atomic. **Proof:** slow child plug-in under playback/UI stress. **Prevents:** deadlock. **Learned from:** Shard 0.9.2.
- [ ] **HOSTER-04 — Structural mutation is audio-safe.** Suspend or emit silence while changing graph; audio thread never takes a structure lock and never observes partial topology. **Proof:** add/remove/reorder under playback. **Prevents:** crash/buzz.
- [ ] **HOSTER-05 — Third-party destruction occurs outside callback lock.** **Proof:** lock trace with child that calls UI synchronously during destruction. **Prevents:** reentrant deadlock.
- [ ] **HOSTER-06 — State capture has defined locking.** Hosted state reads occur under the correct structure ownership without blocking realtime indefinitely. **Proof:** save session during processing and UI callbacks.
- [ ] **HOSTER-07 — Detached editors close before processors.** Stale indices are rejected and wrappers do not steal keys. **Proof:** multiple detached-window close orders. **Prevents:** UAF and host focus theft.
- [ ] **HOSTER-08 — Broken third-party plug-ins are contained.** Crash/hang/invalid state during scan/load produces a recoverable quarantine/error path. **Proof:** adversarial fixture plug-ins.

## 15. Installation, signing, notarization, and loaded-artifact truth

- [ ] **INSTALL-01 — Hosts are closed before replacement.** Installer blocks or clearly requires closing Ableton and other supported DAWs; validation confirms no target host process remains. **Proof:** attempt install with host open. **Prevents:** testing old in-memory binary. **Learned from:** Tether/Aegis install feedback.
- [ ] **INSTALL-02 — Existing bundle is removed before copy.** Upgrade does not merge into a stale VST3/AU directory. **Proof:** seed obsolete file, upgrade, confirm removal. **Prevents:** stale metadata/code.
- [ ] **INSTALL-03 — Correct system locations and permissions.** VST3/AU/Standalone and support files install to declared platform paths for the intended scope. **Proof:** clean-user/system install and uninstall.
- [ ] **INSTALL-04 — Built artifacts are signed.** Every nested executable/library and final bundle has the intended Developer ID/Windows certificate, hardened runtime/timestamp policy, and strict/deep verification. **Proof:** platform signature tools.
- [ ] **INSTALL-05 — Installed artifacts remain signed and hash-correct.** Compare built and installed executable hashes and verify signatures again. **Proof:** hash/sign report. **Prevents:** packaging mutation or wrong copy.
- [ ] **INSTALL-06 — Distribution installer is signed/notarized/stapled.** macOS package passes Gatekeeper offline; Windows installer reputation/signature is inspectable. **Proof:** notarization/staple/Gatekeeper or Windows signature logs.
- [ ] **INSTALL-07 — macOS installer domain is intentional.** Package uses correct local-system/user domain and component selection. **Proof:** installer simulation and receipt inspection. **Learned from:** Scepter.
- [ ] **INSTALL-08 — Host caches are refreshed deliberately.** AU cache/AudioComponentRegistrar and VST3 rescans settle; actual loaded module path/version/hash is verified after restart. **Proof:** host/module inspection. **Prevents:** false old-version bug reports.
- [ ] **INSTALL-09 — Upgrade and clean install both pass.** Test previous public version→candidate, candidate reinstall, and clean machine/account. **Proof:** matrix with preserved/migrated state.
- [ ] **INSTALL-10 — Uninstall is scoped.** Removes product binaries/receipts without deleting user presets/licenses unless explicitly selected. **Proof:** uninstall fixture.
- [ ] **INSTALL-11 — Beta and Release coexistence follows policy.** IDs, names, locations, state, and license files either coexist or intentionally replace one another. **Proof:** install-order matrix.
- [ ] **INSTALL-12 — Packaging contains no dev residue.** No symbols, temp files, private keys, logs, source paths, unrelated products, or test fixtures unless intentionally shipped. **Proof:** package inventory.

## 16. Validators and real-host compatibility matrix

- [ ] **VALID-01 — Official format validators pass.** Current official `vstvalidator`, `pluginval`, and `auval` run at the required strictness on installed artifacts. **Proof:** full logs with tool versions. **Prevents:** outdated-validator ambiguity.
- [ ] **VALID-02 — Validator/tool artifacts are isolated, not assumed.** If a validator appears wrong, reproduce with current version, minimal plug-in/API contract, and real host before waiver. **Proof:** documented isolation. **Learned from:** Janggo boolean fuzz, Vanguard old pluginval.
- [ ] **VALID-03 — Host matrix is declared before testing.** Include every advertised host/OS/format; at minimum regress the historically relevant Ableton Live, FL Studio, Logic Pro, REAPER, Studio One, Cubase, and Bitwig cells where supported. **Proof:** matrix with host versions.
- [ ] **VALID-04 — Each host loads, creates editor, processes, saves, restores, bypasses, closes, and rescans.** **Proof:** per-cell smoke artifacts. **Prevents:** validator-only confidence.
- [ ] **VALID-05 — Sample-rate matrix passes.** Exercise all supported rates, at least 44.1/48/88.2/96/192 kHz when advertised, including live rate changes if host allows. **Proof:** audio/state/latency results.
- [ ] **VALID-06 — Block-size matrix passes.** Include 1, non-power-of-two, very small, prepared size, changing, and larger-than-prepared blocks. **Proof:** invariance/adversarial runner.
- [ ] **VALID-07 — Multi-instance matrix passes.** At least two active audio instances and two visible editors under automation, resize, presets, and quality changes. **Proof:** CPU/UI/host responsiveness log.
- [ ] **VALID-08 — Lifecycle matrix passes.** Repeated create/destroy, show/hide, suspend/resume, release/prepare, sample-rate change, project close, and host shutdown. **Proof:** sanitizer/host run.
- [ ] **VALID-09 — Automation matrix passes.** Every parameter automates at min/default/max and rapid/fuzz values without notification storms, NaNs, or lost gestures. **Proof:** parameter runner.
- [ ] **VALID-10 — State matrix passes in every format.** Cross-format compatibility follows policy; current/legacy/corrupt state restores with correct latency/UI/DSP. **Proof:** fixtures and host projects.
- [ ] **VALID-11 — Real-time CPU and UI budgets pass.** Measure average and tail latency with editor closed, one open, two open, and pressure mode. **Proof:** repeatable benchmark, not visual impression.
- [ ] **VALID-12 — No regression outside intended scope.** Null/reference renders, UI snapshots, identity, parameters, presets, licensing, installers, and performance are compared with the previous release. **Proof:** release delta report.

## 17. Release close and long-term hygiene

- [ ] **RELEASE-01 — Product-specific gates also pass.** Run every repository release validator, self-test, UI snapshot, conductor/harness, null/reference, state, focus, and installer test. **Proof:** command transcript.
- [ ] **RELEASE-02 — Release and Beta are installed and smoke-tested.** Do not stop at compilation. **Proof:** installed paths/hashes and host results.
- [ ] **RELEASE-03 — Changelog validation section is complete.** Include exact commands, hosts, artifacts, versions, limitations, and intentionally unchanged behavior in established project format. **Proof:** reviewed entry.
- [ ] **RELEASE-04 — Documentation matches UI and behavior.** Tooltips, mode explanations, manuals, screenshots, target OS/hosts, paths, and license steps are current. **Proof:** doc/UI comparison.
- [ ] **RELEASE-05 — No known red gate is deferred silently.** Every deviation has owner, issue, impact, workaround, and explicit release authority. **Proof:** exception register.
- [ ] **RELEASE-06 — Commit history is reviewable.** Tests and behavior changes are grouped with meaningful messages; generated packaging is clearly identified. **Proof:** log review.
- [ ] **RELEASE-07 — Remote and tag identity are verified.** Commit is pushed to intended repository, annotated tag/version points to it, and CI artifacts match. **Proof:** remote/tag/hash comparison.
- [ ] **RELEASE-08 — Rollback is possible.** Previous installer/artifacts, migration policy, and user-state compatibility allow safe rollback or explicitly document why not. **Proof:** rollback rehearsal for stateful changes.
- [ ] **RELEASE-09 — Post-install user path is clean.** Fresh user can discover the plug-in, open it, understand first screen, hear correct audio, use presets, resize, license, save, and reopen without developer knowledge. **Proof:** clean-account end-to-end recording.
- [ ] **RELEASE-10 — Regression knowledge is retained.** Every new escaped defect adds a minimal test and a new/updated checklist gate with cause and proof. **Proof:** bug-close template. **Prevents:** fixing the same class in every product.

## 18. Historical source corpus

The catalog was synthesized on 2026-07-11 from the complete canonical root changelog in each native product repository below, then cross-checked against current tests, CMake, release validators, installers, and relevant source mechanisms. Large repositories contain mirrored/copied plug-in changelogs; the root product changelog is treated as the canonical history and unique product-local material is captured by that product's gates.

| Repository | Root changelog lines | Bytes | SHA-256 |
|---|---:|---:|---|
| Aegis | 2,936 | 294,452 | `15d8a165f7af2944bbadbb2238e96e59518bfa21afd613530928042efe761608` |
| dagon | 3,927 | 376,506 | `ca5a332ce49d6206a5a3ecf1bae01281277812b2b01a832b2ed21eea51e19eb5` |
| golem | 143 | 11,921 | `ecfc43d9fcc1d44fd33f76d316232f2b9f92f0607ba4561c4aa5bd7f59aad073` |
| host | 226 | 13,558 | `b1a0076bc8dbc8cbce59ad9e7875caa8fe25e6245e5db2a2ecefa7c097170693` |
| janggonative | 775 | 53,157 | `5891f9cca124ff7b2643394f034857135a881019b63cc3fba5a8a218deab3ced` |
| mantanative | 14,456 | 957,473 | `8699fcab4498a2740291411fa28617f74c63945c02c17a9215ceb4b66ee9f494` |
| scepternative | 16,862 | 1,633,246 | `becb85070b05040ed067e2cee45402936aee37e1af827152fe9d471cb3054668` |
| splitter (Shard) | 1,489 | 90,375 | `22344f10dd1d193c3ea02cd435a7f379c0578c67feafb5369b53700d986fa45e` |
| tethernative | 169 | 12,144 | `0e39ae6d84eb169420f0e05decba71edc49b69d06a1a66c4a8fcb3fcc5065c82` |
| vanguard | 7,861 | 439,152 | `ad1a9ff008410cbc5ae919a94568ef2fa0aab9ec6ed4218a0328cb7f89f3a38a` |
| vanguardnative | 7,163 | 403,345 | `cb584889460b37e64ed1f78c31ba55113a0f69c43caf628681154d8e42c349c7` |
| wavetable-editor | 43 | 3,582 | `e422341354c95b3763f75ceddbd2528fed2525cacb27137bb988d6fcf50419a7` |
| yashanative | 5,600 | 276,375 | `bd5d16d20dc9adac473b10dcdaaddd94f33c1f9a914104269472a5c63f0f6348` |

### Principal inherited failures by product

- **Aegis:** explicit shortcut focus exceptions; paint/hit geometry drift under resize; replacement of estimated waveform behavior with truthful signal paths; install-while-host-open confusion; semantic/visual/bug-compatibility release validators.
- **Dagon:** drag-time frosted-glass/repaint storms; dirty-driven UI; platform frame budgets; cached audio-thread parameters; no fast-math sound drift; hidden-editor and allocation pressure; release/prepare must not clear editor policy.
- **Golem:** basic identity, build, validation, and release hygiene remain mandatory even when the product history is short.
- **MT Host:** hosted plug-in lifecycle, scan/cache seeding, signing/notarization, standalone host shutdown, and child plug-in containment.
- **Janggo:** zoom provenance and persistence; 0x0 resize guard; debounced/flush-on-close preferences; host notification reentrancy deadlock; safe popup/dialog teardown; multi-editor pressure shedding; path connectivity; validator Default program.
- **Manta:** native zoom geometry/caches; hidden timers; full shutdown ordering and safe async ownership; Web/native cutover; focus retry after real bounds; accidental focus grab regression; mono/transitional buffers; APVTS silent restore; first native license UI omission.
- **Scepter:** WebView and WebView2 focus handoff; child HWND behavior; Retina logical pixels; actual sidechain buffer channels; WebView transport backpressure; WebView2 data/linking; native-only build enforcement; AU cache/version/installer and parameter hint compatibility.
- **Shard:** message/audio callback-lock deadlocks; split-phase hosted plug-in mutation; scanner/thread/window ownership; latency-compensated primed bypass; processor-owned activation; signed offline licenses; preset path safety and notification batching; detached-window focus; truthful renderer fallback.
- **Tether:** stable parameters and block-size invariance; actual wet-vs-dry history; dropdown-only styling scope; selected-mode tooltips; zoom parity; floor/gradient semantics; first-run trial opacity/visibility; host-open reinstall confusion.
- **Vanguard / Vanguard Native:** duplicate refresh loops; revision-driven UI; state/DSP synchronization; popup and native-child teardown; deferred overlay/focus; transient mono/zero-channel safety; panel resize preserving zoom; final zoom persistence; primed bypass; old validator isolation.
- **Wavetable Editor:** usable-display initial sizing, fixed aspect, zoom limits, and standalone/native editor lifecycle.
- **Yasha:** native identity/export and installer workflows; Windows WebView2 focus; sample-based transport timing; monotonic AU parameter hints; native text/help/top-strip/interaction/state/hardening gates; Lite/full coexistence.

## 19. Proof-report skeleton

```markdown
# Native Plugin Proof Report — PRODUCT VERSION

Verdict: RELEASE READY | NOT RELEASE READY
Candidate: COMMIT (clean|dirty), Release|Beta
Artifacts: FORMAT/PATH/HASH/SIGNATURE
Matrix: OS / ARCH / FORMAT / HOST VERSION

## Blockers
- ID — FAIL|BLOCKED — concise cause — evidence path

## Coverage
| Section | Pass | Fail | Blocked | N/A | Total |
|---|---:|---:|---:|---:|---:|

## Results
- ID — STATUS — procedure/command — evidence — notes

## N/A justifications
- ID — structural reason — source/build evidence

## Evidence index
- path — candidate identity — what it proves

## Exceptions
- approved deviation, owner, issue, impact, workaround, expiry
```
