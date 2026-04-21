# Apple Development Official

A Codex skill built from Apple-shipped Xcode Intelligence material and rewritten into a usable Apple development reference set.

![Version](https://img.shields.io/badge/version-26.4.1.1-black)
![Xcode](https://img.shields.io/badge/Xcode-26.4.1-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## What this project is

This repository is not just a skill package. It is also the research log and build system for turning the Apple development material bundled inside Xcode into a skill that another coding agent can actually load and use.

The source material comes from Xcode's `IDEIntelligenceChat.framework` bundle:

- `*.idechatprompttemplate` prompt files
- `AdditionalDocumentation/*.md` bundled Apple markdown guides
- plist and `xcplugindata` metadata for model pairing, tool surfaces, onboarding, and system wiring

The project goal is simple:

- keep the Apple material grounded in the real Xcode bundle
- keep the runtime corpus organized by what helps an agent
- avoid fake summaries where the source text itself matters
- adapt Apple-only prompt templating into skill-usable prompt text where raw template syntax would be wrong

## Why this had to be rebuilt

The original intent of the skill was correct, but the generated runtime docs were wrong in an important way.

The source inventory already claimed many files were `extract-and-incorporate`. In practice, the generated docs did not actually incorporate them. Instead, they produced short summaries, token lists, headings, and heuristic notes about each source file.

That broke the main value of the project:

- the skill mentioned Apple prompt templates but did not include their prompt content
- the skill mentioned Apple markdown guides but often reduced them to topic summaries
- the skill lost the exact wording and structure that make the prompt families useful
- the output looked grounded, but it was not faithful enough to the real bundle contents

This repository now documents that failure plainly, because it is the main lesson of the project.

## Research scope

The work in this repository focused on the actual Xcode 26.4.1 installation selected by `xcode-select`.

Primary source areas:

- `IDEIntelligenceChat.framework/Versions/A/Resources/*.idechatprompttemplate`
- `IDEIntelligenceChat.framework/Versions/A/Resources/AdditionalDocumentation/*.md`
- `IDEIntelligenceChat.framework/Versions/A/Resources/ApprovedIntegrationModelPairings.plist`
- `IDEIntelligenceChat.framework/Versions/A/Resources/AgentVersions.plist`
- `IDEIntelligenceChat.framework/Versions/A/Resources/IDEIntelligenceChat.xcplugindata`
- `IDEIntelligenceChat.framework/Versions/A/Resources/OnboardingIntelligenceXcode.bundle/...`
- selected system Apple Intelligence files used for runtime context

Out of scope for runtime loading:

- local Coding Assistant binaries and user-local assistant state
- machine-specific config files under `~/Library/Developer/Xcode/CodingAssistant`
- empty bundle artifacts with no useful runtime content

## What was found

At the time of this rebuild, the selected Xcode bundle contained:

- `46` `*.idechatprompttemplate` files
- `20` bundled Apple markdown guides in `AdditionalDocumentation`
- bundle metadata that exposes model pairings, assistant actions, editor surfaces, onboarding copy, and tool hooks

Extra source candidates were checked too:

- `Metadata.generativefunctions/*`
- XPC service `Info.plist` and `version.plist`
- other nearby resource files in the same framework

The result of that audit:

- the `46` prompt templates are all covered by the repo inventory
- the `20` bundled markdown guides are covered
- `Metadata.generativefunctions/*` are empty `{"syntaxTree": ""}` skeletons and not useful runtime material
- XPC service bundle plists are packaging metadata, not prompt or guidance sources

## The main problems

### 1. The generator summarized files it claimed to incorporate

This was the biggest defect.

The inventory declared source-preserving handling, but `scripts/build_reference_corpus.py` was generating prose summaries for runtime docs instead of embedding the actual content. That meant the runtime corpus looked organized, but the most important part of the source material was missing.

### 2. Raw Apple template syntax is wrong for a skill runtime doc

Once the project moved from summaries to source-preserving output, a second problem became obvious.

Many Apple prompt templates contain internal template syntax such as:

```text
{{ FilePath }}
{% if SelectedCode %}
{% for interface in interfaces %}
```

That syntax is valid inside Apple's own prompt assembly system. It is not valid as a skill runtime prompt unless it is adapted into plain placeholders and readable control-flow markers.

If left untouched, the skill would load broken prompt text.

### 3. The maintenance metadata lied about prompt handling

Once prompt templates needed adaptation, the inventory could no longer honestly call them `extract-and-incorporate`.

They are now handled as `adapt-and-incorporate`, which matches what the project is actually doing.

### 4. Optional system files should not break the rebuild

One system telemetry file expected by the script was not present on this machine:

- `/Library/CoreAnalytics/taskedConfig.json`

The previous script failed hard when it was missing. That is brittle and wrong for a rebuild tool.

The current build preserves that source as optional and records the absence in the generated output instead of crashing.

## Common misconceptions corrected in this project

### "If the inventory lists a source file, the runtime doc must contain it"

False. The old repo proved the opposite. Inventory and output can drift. The generator is the real source of truth for whether the runtime corpus is faithful.

### "Raw is always better"

False. Raw Apple markdown guides are useful as-is. Raw Apple prompt templates are not always usable as-is because their placeholders and control-flow syntax are part of Apple's own rendering system.

The right split is:

- bundled markdown guides: preserve the source content
- Apple prompt templates: adapt the template syntax while preserving the prompt meaning and structure

### "Flattening the bundle means mirroring the bundle"

False. The point of this skill is not to reproduce `Contents/Resources/...`.

The point is to regroup the material into task-shaped docs such as:

- `prompting-core-rules.md`
- `prompting-code-editing-documentation-and-apply.md`
- `platform-swiftui-liquid-glass-and-modern-ui.md`
- `assistant-tools-surfaces-and-actions.md`

### "Anything near the framework is probably useful"

False. The extra scan found nearby files that are empty, packaging-only, or not runtime guidance.

This project now distinguishes between:

- material that helps the runtime skill
- material that helps maintenance and audits
- material that should be ignored

## What failed during the rebuild work

Several paths were tested and rejected.

### Heuristic summaries

This was the old design and it failed the core goal. Summaries hid exactly the parts of the source material the skill was supposed to preserve.

### Treating prompt templates as raw markdown blobs

This fixed the missing-content problem but created a new runtime problem. Apple template markers such as `{{ ... }}` and `{% ... %}` leaked into the docs and made them unfit for direct skill use.

### Assuming every system file exists

This caused rebuild failure on machines that did not have the expected CoreAnalytics file. That assumption is now gone.

### Assuming more bundle files automatically meant more useful coverage

Extra scanning did find adjacent resource files, but not all of them mattered. The empty `Metadata.generativefunctions/*` files are the clearest example.

## The final solution

The current design is intentional and split by source type.

### Apple markdown guides

These are preserved as source content inside grouped runtime docs. The generator shifts heading depth so they can live inside larger grouped reference files cleanly.

### Apple prompt templates

These are adapted, not merely copied.

The generator now converts Apple template syntax into skill-readable prompt text:

- `{{ FilePath }}` becomes `<file path>`
- `{% if SelectedCode %}` becomes `[if selected code is available]`
- `{% for snippet in snippets %}` becomes `[repeat for each snippet in snippets]`

This preserves the structure and intent of the original prompt without leaking Apple-only rendering syntax into the skill runtime docs.

### Structured metadata files

Plists, strings, xcplugindata, and json sources are emitted as raw serialized blocks instead of prose summaries.

### Missing optional sources

Missing files are recorded directly in the generated output instead of aborting the build.

## Runtime structure

The runtime corpus is intentionally flat:

- `references/index.md`
- `references/task-routing.md`
- `references/prompting-*.md`
- `references/platform-*.md`
- `references/assistant-*.md`
- `references/system-intelligence-context-and-telemetry.md`

This is not a mirror of Apple's on-disk structure. It is a task-oriented reference set.

## Useful command line setup and research commands

These are the commands that mattered during the investigation and rebuild.

### Initialize the submodule

If this skill is checked out through the parent `skills` repository as a submodule:

```bash
git submodule update --init apple-development-official
```

### Check which Xcode is selected

```bash
xcode-select -p
```

### List all prompt templates in the selected Xcode bundle

```bash
find "/Applications/Xcode-26.4.1.app" -type f -name "*.idechatprompttemplate" 2>/dev/null
```

or, using the repo helper:

```bash
./scripts/scan_sources.sh
```

### Count prompt templates

```bash
find "/Applications/Xcode-26.4.1.app/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources" -type f -name "*.idechatprompttemplate" 2>/dev/null | wc -l
```

### Inspect a raw Apple prompt template

```bash
sed -n '1,220p' "/Applications/Xcode-26.4.1.app/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources/BasicSystemPrompt.idechatprompttemplate"
```

### Inspect bundled Apple markdown guides

```bash
find "/Applications/Xcode-26.4.1.app/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources/AdditionalDocumentation" -type f -name "*.md" 2>/dev/null
```

### Inspect Xcode assistant wiring metadata

```bash
plutil -p "/Applications/Xcode-26.4.1.app/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources/IDEIntelligenceChat.xcplugindata"
```

```bash
plutil -p "/Applications/Xcode-26.4.1.app/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources/ApprovedIntegrationModelPairings.plist"
```

### Rebuild the runtime corpus

This project follows the repo rule of using `uv run` instead of direct `python`.

```bash
uv run ./scripts/build_reference_corpus.py
```

### Verify there are no unresolved Apple template markers in runtime docs

```bash
rg -n -F '{{' references
```

```bash
rg -n -F '{%' references
```

Both commands should return no matches after a correct rebuild.

### Compare inventory coverage against current Xcode prompt count

```bash
find "/Applications/Xcode-26.4.1.app/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources" -type f -name "*.idechatprompttemplate" 2>/dev/null | wc -l
```

```bash
rg -n 'XCODE_RESOURCES/.*idechatprompttemplate' maintenance/source-inventory.md | wc -l
```

The counts should match.

### Lint the generator

```bash
uvx ruff check scripts/build_reference_corpus.py
```

### Lint the markdown corpus

This repo uses a markdown lint config that relaxes rules which would otherwise damage imported Apple source formatting.

```bash
bunx markdownlint-cli2 --config /tmp/apple-development-official.markdownlint.json README.md references/*.md maintenance/*.md
```

## How to do the same inspection manually in the UI

Not everything needs to be done from the command line.

### Inspect the Xcode bundle in Finder

1. Open `/Applications`.
2. Find `Xcode-26.4.1.app`.
3. Right click it and choose `Show Package Contents`.
4. Navigate to:

```text
Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources
```

5. Open:
   - `AdditionalDocumentation/` for bundled Apple guides
   - `OnboardingIntelligenceXcode.bundle/` for onboarding and privacy copy
   - top-level `*.idechatprompttemplate` files for prompt sources

### Inspect the same files in Xcode

1. Open Xcode.
2. Use `File > Open...`.
3. Open a copied file or a working folder that contains extracted resources from the Xcode bundle.
4. Browse the prompt templates and markdown docs directly in the editor.

This is useful when you want syntax highlighting, find-in-file, or side-by-side reading.

### Check Coding Assistant surfaces in the Xcode UI

1. Open Xcode.
2. Open `Settings`.
3. Look for the `Intelligence` section.
4. Open the Coding Assistant UI and compare what Xcode exposes against what is described in `references/assistant-tools-surfaces-and-actions.md`.

This is useful for validating names, labels, and visible assistant surfaces against the bundle metadata.

### Validate the generated skill docs manually

1. Open this repository in your editor.
2. Open `references/index.md`.
3. Open one prompt doc and one platform doc.
4. Confirm:
   - prompt docs do not contain raw `{{ ... }}` or `{% ... %}`
   - grouped docs still preserve the Apple source content where expected
   - metadata docs show serialized structured output rather than prose summaries

## Files that matter most

- `SKILL.md`: runtime entrypoint for the skill
- `scripts/build_reference_corpus.py`: rebuild logic
- `scripts/scan_sources.sh`: source discovery helper
- `references/`: runtime docs loaded by the skill
- `maintenance/source-inventory.md`: source coverage ledger
- `maintenance/source-coverage-checklist.md`: audit checklist
- `maintenance/source-selection.md`: what is included and why

## Known gaps and deliberate limits

- One optional system telemetry file may be missing on a given machine. The rebuild now records that instead of failing.
- Some prompt families still contain Apple-specific concepts that are kept on purpose because they explain how Xcode itself thinks, even when the exact tool names differ from another agent environment.
- The runtime corpus is organized for use, not for legal or archival reproduction of the full Xcode bundle structure.

## How to update this project for a new Xcode release

1. Select the target Xcode with `xcode-select`.
2. Run `./scripts/scan_sources.sh`.
3. Check prompt count and bundled markdown count.
4. Inspect any new files in `IDEIntelligenceChat.framework/Versions/A/Resources`.
5. Decide for each new file:
   - runtime source
   - maintenance-only source
   - ignore
6. Update `scripts/build_reference_corpus.py` if a new source family needs different handling.
7. Run `uv run ./scripts/build_reference_corpus.py`.
8. Run the verification commands in this README.

## Project outcome

The current repository now matches the actual project intent:

- Apple markdown guides are preserved where raw source content is useful
- Apple prompt templates are adapted into skill-usable prompt text
- runtime docs are organized by task instead of by bundle path
- maintenance files tell the truth about how sources are handled
- rebuilds are resilient to missing optional system inputs

That is the core result of the research and rebuild.

## License

MIT License

Copyright (c) 2026 Gaston Morixe <gaston@gastonmorixe.com> (https://gastonmorixe.com)

See [LICENSE](./LICENSE) for the full text.
