#!/bin/bash
set -euo pipefail

tmp_file="$(mktemp)"
cleanup() {
  rm -f "$tmp_file"
}
trap cleanup EXIT INT TERM

repo="${1:-.}"
if ! repo="$(cd "$repo" 2>/dev/null && pwd)"; then
  echo "Repository path does not exist: ${1:-.}" >&2
  exit 2
fi

echo "Collecting static native plug-in evidence from $repo" >&2

if command -v rg >/dev/null 2>&1; then
  search() {
    rg -n -i --hidden \
      -g '!build*/**' -g '!Build*/**' -g '!.git/**' -g '!node_modules/**' \
      -g '!JUCE/**' -g '!third_party/**' -g '!vendor/**' \
      -- "$1" "$repo" 2>/dev/null | head -n 8 || true
  }
  file_search() {
    rg --files "$repo" -g '!build*/**' -g '!Build*/**' -g '!.git/**' \
      -g '!node_modules/**' -g '!JUCE/**' -g '!third_party/**' -g '!vendor/**' \
      2>/dev/null | rg -i -- "$1" | head -n 12 || true
  }
else
  echo "ripgrep is unavailable; using a reduced grep/find fallback" >&2
  search() {
    grep -RInE --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=JUCE \
      --exclude-dir=third_party -- "$1" "$repo" 2>/dev/null | head -n 8 || true
  }
  file_search() {
    find "$repo" -type f 2>/dev/null | grep -Ei -- "$1" | head -n 12 || true
  }
fi

sanitize() {
  tr '\t\r\n' '   ' | sed 's/[[:space:]][[:space:]]*/ /g; s/^ //; s/ $//'
}

add() {
  local id="$1"
  local result="$2"
  local evidence="$3"
  local meaning="$4"
  printf '%s\t%s\t%s\t%s\n' \
    "$id" "$result" \
    "$(printf '%s' "$evidence" | sanitize)" \
    "$(printf '%s' "$meaning" | sanitize)" >> "$tmp_file"
}

observe_files() {
  local id="$1"
  local pattern="$2"
  local meaning="$3"
  local found
  found="$(file_search "$pattern")"
  if [ -n "$found" ]; then
    add "$id" "observed" "$found" "$meaning"
  else
    add "$id" "not_detected" "No matching file" "$meaning"
  fi
}

observe_source() {
  local id="$1"
  local pattern="$2"
  local meaning="$3"
  local found
  found="$(search "$pattern")"
  if [ -n "$found" ]; then
    add "$id" "observed" "$found" "$meaning"
  else
    add "$id" "not_detected" "No matching source pattern" "$meaning"
  fi
}

if git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  commit="$(git -C "$repo" rev-parse HEAD)"
  branch="$(git -C "$repo" branch --show-current)"
  dirty="$(git -C "$repo" status --porcelain | wc -l | tr -d ' ')"
  add "EVID-01" "observed" "commit=$commit branch=$branch dirty_entries=$dirty" \
    "Candidate identity was found; a dirty release tree is still a blocker."
else
  commit="unknown"
  branch="unknown"
  dirty="unknown"
  add "EVID-01" "not_detected" "Not a Git worktree" \
    "An immutable candidate identity is required."
fi

changelog="$(file_search '(^|/)CHANGELOG(\.[^.]+)?$|(^|/)CHANGELOG\.md$')"
if [ -n "$changelog" ]; then
  add "HYGIENE-10" "observed" "$changelog" \
    "A changelog exists; its completeness and validation evidence require review."
else
  add "HYGIENE-10" "not_detected" "No changelog found" \
    "A versioned, evidence-bearing changelog is required."
fi

observe_files "HYGIENE-02" '(^|/)VERSION$|CMakeLists\.txt$|Info\.plist|moduleinfo\.json' \
  "Version-bearing files were inventoried; their values still need comparison."
observe_source "HYGIENE-01" 'BUNDLE_ID|PLUGIN_CODE|PLUGIN_MANUFACTURER_CODE|PRODUCT_NAME|COMPANY_NAME|project\(' \
  "Product identity declarations were found; uniqueness still needs proof."
observe_source "HYGIENE-03" 'AudioParameter|ParameterID|parameter.*id|versionHint' \
  "Parameter identifiers were found; stability requires a prior-release manifest comparison."
observe_source "HYGIENE-04" 'versionHint|parameterVersionHint|AudioProcessorParameterWithID' \
  "AU parameter version-hint mechanisms may exist; monotonic history still needs proof."
observe_source "BUILD-01" 'FORMATS[^\n]*(VST3|AU|Standalone)|juce_add_plugin' \
  "Declared formats were found; clean Release and Beta builds remain runtime gates."
observe_files "BUILD-08" 'CMakeLists\.txt$|CMakePresets\.json$|\.gitmodules$|FetchContent|CPM' \
  "Build/dependency declarations were found; reproducibility still needs a clean build."
observe_files "RELEASE-01" '/(tests?|Tests?|tools?)/|test[^/]*\.(cpp|py|sh)$|self.?test|UiPolicyTest|StateCheck' \
  "Product tests were found; the audit must run every applicable suite."
observe_files "VALID-01" 'validate.*release|pluginval|vstvalidator|auval|plugtest' \
  "Release/format validation tooling was found; tool versions and installed artifacts require proof."
observe_files "INSTALL-04" 'sign.*install|notar|package|installer|\.pkgproj$|\.iss$|\.ps1$' \
  "Signing/packaging tooling was found; built and installed signature verification remains required."

observe_source "RT-03" 'setLatencySamples|updateHostDisplay|AsyncUpdater|triggerAsyncUpdate' \
  "Host-notification mechanisms were found; lock/reentrancy ordering needs manual and runtime proof."
observe_source "RT-04" 'processBlock\s*\(|getNumSamples\s*\(' \
  "Audio block processing exists; exact current-length and oversized-block tests are mandatory."
observe_source "RT-07" 'isfinite|isFinite|NaN|Inf|sanitize.*sample|ScopedNoDenormals' \
  "Numerical-safety mechanisms were found; adversarial non-finite tests are still required."
observe_source "BUS-01" 'isBusesLayoutSupported|BusesProperties|AudioChannelSet|BusProperties' \
  "Bus-layout code was found; host negotiation and transitional buffers require runtime proof."
observe_source "BUS-04" 'getBusBuffer|sidechain|side.chain|auxiliary' \
  "Sidechain/auxiliary handling was found; actual channel-count scenarios require proof."
observe_source "LAT-03" 'bypass|Bypass|DryWetMixer|delay.*bypass|latency' \
  "Bypass/latency mechanisms were found; impulse/null and transition proof is still required."

observe_source "STATE-01" 'stateVersion|schemaVersion|getStateInformation|setStateInformation|ValueTree' \
  "State serialization was found; migration and corrupt-state fixtures remain required."
observe_source "STATE-06" 'beginChangeGesture|endChangeGesture|setValueNotifyingHost' \
  "Host automation notification code was found; gesture balancing needs runtime proof."
observe_source "PRESET-03" 'preset|Preset|FileChooser|replaceWithText|createDirectory' \
  "Preset/filesystem code was found; containment, atomic writes, and corrupt input need tests."

observe_source "FOCUS-01" 'grabKeyboardFocus|giveAwayKeyboardFocus|setWantsKeyboardFocus|SetFocus|windowIgnoresKeyPresses' \
  "Focus-handling code was found; every host interaction still needs runtime keyboard proof."
observe_source "FOCUS-10" 'dismissAllActiveMenus|PopupMenu|DialogWindow|AlertWindow|FileChooser' \
  "Transient UI exists; overlap and teardown scenarios require proof."
observe_source "LIFE-01" 'beginShutdown|isShuttingDown|shuttingDown|shutdown' \
  "Shutdown guards were found; teardown order still needs lifecycle testing."
observe_source "LIFE-03" 'SafePointer|WeakReference|callAsync|AsyncUpdater|std::weak_ptr' \
  "Async lifetime mechanisms were found; a complete callback inventory is still required."
observe_source "LIFE-02" 'stopTimer|stopThread|signalThreadShouldExit|join|waitForThreadToExit' \
  "Timer/worker shutdown code was found; bounded completion requires stress proof."
observe_source "PERF-02" 'revision|dirty|invalidate|cache|repaint' \
  "Dirty/cache/repaint mechanisms were found; counters and pressure tests remain required."

observe_source "ZOOM-01" 'zoom|Zoom|scaleFactor|uiScale|windowScale|editorWidth|editorHeight' \
  "Zoom/size code was found; every zoom and persistence precedence must be exercised."
observe_source "ZOOM-09" 'PropertiesFile|ApplicationProperties|flush|saveIfNeeded|Timer.*resize|debounce' \
  "Preference persistence mechanisms may exist; quick-close flush and write cadence require proof."
observe_source "RENDER-06" 'waveform|history|input.*level|output.*level|wet.*signal|dry.*signal' \
  "Signal visualization code was found; source-vs-estimator truth requires an audio comparison."
observe_source "RENDER-12" 'snapshot|rendering.*primitive|pixel|golden|image.*compare' \
  "Visual tests were found; real-renderer and nonblank pixel guards remain required."

observe_source "LIC-01" 'trial|license|activation|activate|purchase' \
  "Licensing/trial code was found; Release first-run and all state transitions require proof."
observe_source "LIC-05" 'signature|verify.*license|canonical|publicKey|Ed25519|RSA' \
  "Signature-verification code was found; canonical adversarial fixtures are required."
observe_source "LIC-08" 'activation.*thread|license.*thread|std::thread|ThreadPoolJob' \
  "Async licensing work may exist; processor ownership and close-during-activation need proof."

observe_source "HOSTER-01" 'KnownPluginList|PluginDirectoryScanner|scanNextFile|ChildProcess' \
  "Hosted plug-in scanning code was found; if applicable, run the full HOSTER section."

echo "Writing machine-readable observation report" >&2
python3 - "$repo" "$commit" "$branch" "$dirty" "$tmp_file" <<'PY'
import json
import pathlib
import sys

repo, commit, branch, dirty, source = sys.argv[1:]
observations = []
for raw in pathlib.Path(source).read_text(encoding="utf-8").splitlines():
    if not raw:
        continue
    fields = raw.split("\t", 3)
    if len(fields) != 4:
        continue
    item_id, result, evidence, meaning = fields
    observations.append({
        "id": item_id,
        "static_result": result,
        "evidence": evidence,
        "meaning": meaning,
        "runtime_pass": False,
    })

counts = {}
for item in observations:
    counts[item["static_result"]] = counts.get(item["static_result"], 0) + 1

print(json.dumps({
    "schema": "mt-native-plugin-static-audit-v1",
    "repository": repo,
    "commit": commit,
    "branch": branch,
    "dirty_entries": dirty,
    "warning": "Static observations are inventory only. They are not checklist PASS results.",
    "counts": counts,
    "observations": observations,
    "next_step": "Read CHECKLIST.md completely, assign applicability, then collect runtime evidence.",
}, indent=2, sort_keys=True))
PY
