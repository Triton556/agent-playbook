# Causal state and interaction

## One model, several views

Separate three kinds of state:

```text
Domain input: selected entity, physical parameters, dataset version, scenario
Derived result: solver revision, geometry/paths, measurements, validity
Presentation: camera, selected annotation, effects, playback, panel layout
```

Define `derive(input)` independently of rendering where practical. The renderer, charts, detector, labels and explanation consume the same result revision. Keep units at the boundary. A paused animation stops time; it must still recompute after an input edit. If a computation is pending, retain the previous result with an explicit pending status or clear it—do not silently combine a new input label with an old output.

For asynchronous solvers, attach an increasing revision to requests and accept only the latest matching response. Bound work and report incomplete/failed results. Animation can interpolate appearance between committed states; it must not present interpolated numbers as settled measurements. A queued transition that has been superseded must be cancelled or rebased.

## Guided presets and direct control

A useful preset is a question with a visible answer: “What changes near resonance?”, “What happens when this route fails?”, “Why does the spectrum reunite?” Ensure presets are valid and reset all inputs they depend on. Include at least one revealing contrast and one way back.

Direct manipulation, DOM sliders, buttons and keyboard shortcuts call the same commands. A draggable ring can be discovered through its label and an equivalent slider. Input feedback needs three parts: selected object, changing value, visible consequence. Preserve object identity across data sorting and topology changes: key by domain ID rather than sorted index; retain color/symbol and selection, including links between spatial marks, chart and detail card.

Treat drag as a transaction when edits persist:

```text
begin → capture baseline + ownership
preview → derive bounded results
commit → record one history item
cancel → restore baseline and derived output
```

Handle pointer cancellation, lost capture, escape, invalid values and interrupted workers according to the product's semantics. Reset should restore a documented baseline. Undo/redo includes all causal input state, while camera-only moves usually remain separate.

## Explain a process through time

Use a trace of events with stable IDs, time or sequence, input/output and status. Derive the active chapter, object emphasis, timeline cursor and text from that trace. Keep “simulation time”, “playback speed” and “wall clock” distinct. A duration displayed as measured needs measurement provenance; synthetic timings are scenarios.

Represent three useful levels without requiring every project to use all three:

- **Overview:** where does the input go and what returns?
- **Mechanism:** which state changes and which dependency carries it?
- **Inspection:** the exact event, value or record behind the picture.

In deterministic replays, scrubbing and revisiting a time should reproduce the same state. Use checkpoints for costly simulations rather than rerunning an unbounded history every pointer move. Log-ratio or time warping can make a rapid event visible, but label the displayed time scale.

## Compare deliberately

Store a complete A snapshot: inputs, data/solver version, camera, relevant visual settings, seed and time. B varies the intended factor. A frozen trace or ghost helps only if users know what is frozen. Prevent animation, auto-quality changes and data refresh from altering one side unnoticed. If camera/lighting is the experimental variable, keep the model state fixed.

References: [Cube Graph](https://sael.net/cube-graph/) links cube and sticker graph; [Prompt](https://sael.net/prompt/) links chapters, token inspection and a timeline; [Prismatic](https://sael.net/prismatic/) exposes authored optical experiments. The shared-state design here is a recommended independent implementation, not a claim that every reference implements all safeguards.
