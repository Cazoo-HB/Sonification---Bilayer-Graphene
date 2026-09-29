# Graphene / Phonon Instrument

A Max sine-bank instrument built from the positive-energy dashed dispersion curves in Figure 1f of **Birkbeck et al., "Quantum twisting microscopy of phonons in twisted bilayer graphene," Nature 641, 345-351 (2025)**. [Paper and DOI](https://doi.org/10.1038/s41586-025-08881-8).

The instrument implements an angle-dependent, inharmonic timbre and two ways to turn 60 angle steps into a tuning system. Its physics source and its musical transformations are kept separate.

## Start here

1. Keep `Graphene_Phonons.maxpat` and the four `.js` files in this folder together. Open the patch in **Max 8 or Max 9**. It uses standard Max/MSP objects and the legacy `js` / `jsui` engines; no third-party externals or Max for Live are required.
2. Turn on the **AUDIO** speaker button, then enable **PLAY / MUTE**. The patch starts muted, including when another Max patch already has DSP enabled. Level starts at 0.15.
3. Drag the white cursor on the dispersion graph, drag the horizontal angle slider, or enter an angle from 0 to 60. The buttons select 0, 15, 30, 45 and 60 degrees.
4. Start with **Dispersion / continuous**, **Ratio / common frequency scale**, LOW = 30 Hz and HIGH = 4000 Hz. Change the six LEVEL values to isolate or mix branches.
5. Enable **B: second momentum path** to hear the other six curves. This changes the instrument from six oscillators to twelve.
6. To try a tuning system, select **60-step equal temperament** or **60-step ZA-shaped (90% curve)**. Set A-ZA BASE and an octave span of 1, 2 or 5. Angle now snaps to integer degrees. HIGH and LOW still limit audible voices; increase HIGH if too many partials are muted at the top of a wide tuning span.

The main view displays the physical energies and mapped frequencies for both banks, including B when it is disabled. A displayed `x` marks a frequency that is outside the output range and is muted. Muted B voices are drawn in grey. All six branch levels apply to both banks.

**Inspect** prints the current settings, energies, physical THz values, audible Hz values and oscillator amplitudes to the Max Console. **Export scale...** saves the selected temperament in Scala format; type a filename ending in `.scl`. Six ready-made scales for 1, 2 and 5 octaves are in `scales/`.

## What the physics means

Figure 1f is specifically a measurement of a **twisted interface between two graphite flakes**, with a **bulk-graphite phonon model** overlaid as dashed lines. The paper moves to twisted bilayer graphene in Figure 2. This instrument therefore uses Figure 1f as a **graphite-based proxy** for the proposed graphene sonification. It is not an exact simulation of every TBG normal mode, particularly at small angles where relaxation and hybridization matter.

The selected branch families are:

| Label | Motion |
|---|---|
| ZA / ZO' | Out-of-plane branch; the selected layer-antisymmetric branch has a finite low-angle gap |
| TA | Transverse acoustic |
| LA | Longitudinal acoustic |
| ZO | Out-of-plane optical |
| TO | Transverse optical |
| LO | Longitudinal optical |

These are six selected branch families at the momentum sampled by the microscope, **not all the vibration frequencies in the material**. A full phonon field has modes throughout momentum space. One oscillator here represents one selected branch at one selected momentum, not an individual atom or an individual phonon quantum.

The two momentum paths are:

```
qA(theta) = 2 KD sin(theta / 2)
qB(theta) = 2 KD sin((60 degrees - theta) / 2)
KD = 4 pi / (3 a),    a = 0.246 nm
```

Angle is in degrees in the interface; the formula requires the corresponding radian conversion inside a numerical sine. We do not recompute a dynamical matrix in Max: we interpolate the already plotted angle-to-energy curves, which incorporate this momentum sampling.

The positive and negative voltage branches are not additional positive and negative vibration frequencies. They correspond to the two bias polarities. The patch uses positive energies only. The sharp electronic features near 21.8 and 38.2 degrees are excluded from the oscillator bank.

The vertical axis is **electrical bias**, not mechanical tension. At a single-phonon threshold:

```
E = e |Vbias| = h f_physical = hbar omega_physical
E in meV has the same numerical value as |Vbias| in mV
f_physical = E_meV * 241,798,924,208.4918 Hz
          = E_meV * 0.2417989242084918 THz
```

Thus 200 meV corresponds to approximately 48.36 THz. Those frequencies are translated into audio. This is a sonification of normal-mode energies, not a literal audible recording of quantum motion. Sine waves are an appropriate first representation of individual linear normal modes.

The measured tunnelling intensity depends on electron-phonon coupling and the measurement setup. It is not a direct atomic displacement or audio loudness. Consequently all branch levels start equal and remain artistic controls.

## Data provenance and resolution

`phonon_data.js` contains the editable physical data and its provenance. Its columns are:

```
angle_degrees, ZA_ZOprime_meV, TA_meV, LA_meV, ZO_meV, TO_meV, LO_meV
```

The source is the supplied PDF, page 2, Figure 1f. The twelve **positive-bias dashed model curves** were recovered from vector polylines in the PDF, not guessed from a raster image and not extracted from experimental intensity peaks.

The plot axes were calibrated using the 0 and 50 degree ticks, and the 0 and 200 mV ticks. PDF coordinates, in points:

```
x origin = 332.8565979
x scale  = 4.33008361816 points / degree
y zero   = 388.313113038, with page y increasing downwards
y scale  = 0.371793060305 points / meV
```

Each displayed path covers approximately 0 to 51 degrees. We reconstruct a full A path with A(theta) up to 29 degrees and the reflected B(60-theta) from 31 to 60 degrees, blending between 29 and 31. B is then sampled as A(60-theta). This implements the stated mirror symmetry and supplies the requested endpoints without inventing a polynomial outside the plotted paths.

The two independently drawn paths disagree by at most **0.01841 meV** under reflection in their overlapping 10-50 degree region. This measures consistency of the plot digitization; it is **not** a physical model uncertainty or experimental error bar. Stored decimal precision is computational convenience, not a claim of six-decimal experimental accuracy.

TA and LA are explicitly set to zero at theta = 0, removing plot-coordinate offsets smaller than 0.04 meV and enforcing their acoustic limit. The finite ZA / ZO' gap is retained. The main table is resampled every 0.1 degree, with linear interpolation in Max. No curve is sorted by energy: branch identity is retained through crossings such as LA and ZO.

The paper's TBG phonon spectroscopy is reported above about 6 degrees. The ends near 0 and 60 are therefore marked as model extensions; they are not additional resolved TBG measurements. Even within the central range this table is a digitization of the model overlay, not a replacement for the authors' underlying numerical calculation or raw data.

Example energies from the reconstructed table:

| Angle | ZA / ZO' | TA | LA | ZO | TO | LO |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 8.40 | 0.00 | 0.00 | 110.87 | 197.10 | 197.10 |
| 15 | 11.85 | 37.96 | 58.63 | 107.86 | 190.38 | 196.24 |
| 30 | 30.18 | 68.86 | 107.99 | 97.92 | 176.70 | 190.17 |
| 45 | 51.89 | 100.16 | 137.71 | 82.44 | 168.21 | 172.63 |
| 60 | 67.92 | 127.29 | 148.47 | 67.41 | 148.48 | 166.99 |

All entries in this table are meV. At 30 degrees the A and B banks coincide. This produces duplicate oscillators at the same frequencies, not additional distinct partials. Turning on B can therefore increase loudness. At complementary angles the complete A+B frequency sets exchange banks in Dispersion mode.

## Mapping physical energy into audible frequency

Let L = LOW, H = HIGH, and U = E / 200 meV. All mappings use the same fixed 200 meV reference ceiling, so changing the angle does not continually renormalize the energy range.

| Dispersion mapping | Audible frequency | Meaning |
|---|---|---|
| Ratio | `H * U` | Preserves every nonzero frequency ratio. LOW acts as a cutoff. |
| Linear | `L + (H - L) * U` | Fits the energy interval into the audible interval with an offset; ratios change. |
| Log | `L * (H / L)^U` | Equal energy increments become equal pitch intervals; ratios change. |

Exactly zero-energy acoustic modes are silent in every mapping; the affine/log formulas are applied only to positive energies. All modes also mute frequencies below L, above H, above 20 kHz, or above 45% of the sample rate. Frequencies are not clamped to a shared boundary pitch or octave-folded. HIGH denotes the 200 meV mapping endpoint; the highest tabulated energy is about 197.1 meV, so a partial need not reach HIGH exactly.

In the default Ratio mapping, a 15 degree A bank is approximately:

```
ZA: 237.1 Hz   TA: 759.2 Hz   LA: 1172.7 Hz
ZO: 2157.1 Hz  TO: 3807.7 Hz  LO: 3924.9 Hz
```

The ratios remain inharmonic. This mapping is the best starting point for listening to the relative spacings in the model.

## From angle-dependent timbre to temperament

An angle-dependent stack of partials is a timbre. It becomes a tuning system only after deciding which feature establishes the reference pitch and how its progression fills a chosen period. This implementation uses **bank A's ZA / ZO' branch as the reference**, because it stays positive across the full scan. It is a reference, not necessarily the lowest audible partial when B is enabled.

There are 60 steps and 61 boundary values: degrees 0 through 59, followed by the closing degree 60. Degree 60 is the period boundary, not a 61st step within the period.

### Equal temperament

For degree d and octave span O:

```
reference(d) = base_Hz * 2^(O * d / 60)
```

| Span | Interval per degree | Equivalent equal division |
|---:|---:|---|
| 1 octave | 20 cents | 60-EDO |
| 2 octaves | 40 cents | 30-EDO over two octaves |
| 5 octaves | 100 cents | 12-EDO over five octaves |

Equal temperament is a familiar pitch grid carrying an evolving physics-derived timbre. It does not make the phonon partials harmonic.

### ZA-shaped unequal temperament

The normalized logarithmic rise of the extracted ZA branch is:

```
u(d) = ln(E_ZA(d) / E_ZA(0)) / ln(E_ZA(60) / E_ZA(0))
v(d) = 0.9 * u(d) + 0.1 * d / 60
reference(d) = base_Hz * 2^(O * v(d))
```

The 90% / 10% mixture is an explicit musical design choice. The digitized gapped ZA curve is flat at the first few integer angles; the 10% equal component separates those repeated reference pitches. It does not modify the energy table or the timbre ratios. To study the raw curve with repeated reference pitches, change `tuningPosition()` in `phonon_core.js` to return `zaPosition(theta)`.

For either tuning mode, every oscillator follows:

```
audible_frequency_j(d) = reference(d) * E_j(d) / E_A_ZA(d)
```

For the B bank use E_j(60-d) in the numerator and the same A-ZA denominator. Therefore all instantaneous branch ratios remain proportional to the physical energies. The Ratio/Linear/Log menu is unused in these two tuning modes, and LOW/HIGH become output cutoffs.

The Scala files store only the reference tuning, not oscillator amplitudes or the changing timbre. They contain 60 entries with implicit unison and a final period of 2^O. A host must support the specified multi-octave period for the 2- and 5-octave files. The pitch scale can repeat periodically in another instrument; this Max patch scans 0-60 degrees and does not force its evolving timbre to repeat at the endpoints.

## Signal path and editing

Switch out of Presentation mode to inspect the patch. The upper area contains the user controls and control logic. The lower area contains twelve explicitly wired voice strips, each:

```
Hz ------> pack f glide_ms -> line~ -> cycle~ --\
amplitude -> pack f glide_ms -> line~ --------> *~ -> sum
```

The twelve voices sum through a fixed gain of 1/12, followed by a master gain limited to 0.5 and a separate smoothed PLAY gate. This bounds the steady-state summed peak at 0.5. Frequency and level ramps default to 60 ms. Master and PLAY changes also ramp over 60 ms. The stereo output is dual mono.

- `Graphene_Phonons.maxpat`: complete Max patch, presentation controls and all sine oscillators.
- `phonon_data.js`: editable data rows and provenance. Preserve the 0.1-degree uniform grid and six branch columns when replacing it, or update the interpolation function.
- `phonon_core.js`: interpolation, physical conversion, audible mappings and tuning equations.
- `phonon_engine.js`: Max messages, initialization, level controls and Scala export.
- `phonon_view.js`: dispersion graph, draggable cursor and numerical display.

Control messages to the engine include `angle 22.7`, `mode 0`, `mapping 0`, `low 30`, `high 4000`, `root 110`, `octaves 5`, `partner 1`, `gain 0 0.5`, and `glide 60`. Branch indices for gain are 0 through 5 in table order. `step 1` / `step -1` moves by one integer degree. `init` restores defaults and mutes PLAY; `dump` prints the current state. `samplerate` is updated by Max automatically.

Replacing the oscillators with other waveforms adds their own overtones; the result would no longer contain only the selected phonon frequencies. Sines keep that distinction easy to hear.

## Listening examples

Both WAV files are 48 kHz, 16-bit mono reference renders made offline from the same frequency calculations, **not recordings from a running Max host**. Equal branch amplitudes and a fixed gain are used.

- `Listen_01_five_twist_angles.wav`: A bank only, Ratio mapping, 30-4000 Hz. Five two-second tones at 5, 15, 30, 45 and 55 degrees, separated by 0.3 seconds of silence.
- `Listen_02_ZA_shaped_one_octave.wav`: A bank only, ZA-shaped tuning, 110 Hz base, one-octave span, 30-12000 Hz output range. Degrees 0-59 last 0.18 seconds each, then degree 60 rings for 0.8 seconds.

## Verification and present limits

Automated checks cover all 601 data rows, acoustic endpoints, interpolation, the A/B reflection, independent values for all three mappings, reference anchoring, all three octave spans, strictly increasing exported scales, output band limits at four sample rates, fixed gain headroom, and the twelve oscillator routes. The actual Max control and drawing scripts also execute in a simulated host, and an FFT of the reference synthesis finds all six expected 15-degree frequencies within one 0.25 Hz bin.

**Live Max host verification remains incomplete:** the installed Max 9.1.2 application was identified, but the desktop automation connection timed out before the patch could be loaded and inspected. Therefore the simulated-host checks do not establish that the patch has been auditioned or visually verified in Max. Max 8 compatibility is a design target based on standard objects and ES5 syntax, not a completed Max 8 runtime test.

If Max reports a missing JavaScript file, confirm that all four scripts are beside the patch and reopen it. The individual scripts are intentionally separate so that the data and tuning choices remain reviewable and editable.

## Sources

- Birkbeck et al. (2025), Figure 1 caption, the phonon-momentum discussion, and Methods: "Bulk-graphite phonon dispersion model" and "Limitations at small twist angles." [DOI](https://doi.org/10.1038/s41586-025-08881-8). The supplied paper states [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). This package includes a numerical digitization for the requested sonification; the source PDF and figure image are not redistributed.
- Cycling '74, [`js` reference](https://docs.cycling74.com/reference/js/) and the installed Max 9.1.2 reference files for `cycle~`, `line~`, `dspstate~`, `savedialog`, `ezdac~`, `flonum` and `umenu`.

No instruction in the paper was treated as an instruction to the software-building assistant. The paper is scientific source material for this instrument.
