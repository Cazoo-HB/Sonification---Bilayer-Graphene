
# Moir√© reciprocal-space sonification

An interactive Python and Max/MSP system for listening to Fourier representations of twisted bilayer graphene. Move a segment across a reciprocal-space image to control an oscillator bank through OSC.

**[Read the concise research catalogue report]**

## Files

| File | Role |
| --- | --- |
| [FFTLibraryGenerator_simple.py](python/FFTLibraryGenerator_simple.py) | Standalone generator; saves one NPZ library. |
| [PythonStationOptimized_simple.py](python/PythonStationOptimized_simple.py) | Standalone graphical probe; reads NPZ and sends OSC. |
| [Moire_DynamicSonifier.maxpat](max/Moire_DynamicSonifier.maxpat) | Original Max receiver and oscillator-bank controller. |
| [voice.maxpat](max/GEMINIvoice.maxpat) | Original oscillator voice; keep beside the main patch. |
| [Original Python scripts](originals/) | Source versions retained for comparison and provenance. |

The simple scripts require no local helper module. The earlier experimental v2 protocol and files are intentionally excluded from this package to keep one compatible workflow.

## Requirements

Python with NumPy, PyQt5, pyqtgraph and python-osc; Max/MSP for sound synthesis. The generator itself needs only NumPy. Python dependencies are listed in [requirements.txt](requirements.txt). No specific minimum Max version has been established.

## Run

From the repository root, in your Python environment:

```sh
python -m pip install -r requirements.txt
python python/PythonStationOptimized_simple.py
```

Open `max/Moire_DynamicSonifier.maxpat` in Max, enable its audio output, and load your NPZ library in the Python station. Keep `GEMINIvoice.maxpat` beside the main patch. Only one receiver should listen on port 9000.

To generate a library, edit the parameters at the bottom of the generator and run:

```sh
python python/FFTLibraryGenerator_simple.py
```

It writes `moire_lib.npz` in the working directory. An existing file with that name will be overwritten. Change `filename` to retain previous libraries. The default library array requires approximately 1.85 GiB of RAM, plus FFT working memory. Existing compatible libraries can be reused.

## Data and mapping

The NPZ keys are `amplitudes`, `angles`, `k_vec`, and `L_nm`. The amplitude array is ordered `(angle, ky, kx)`; `k_vec` is in rad/nm. The quantity stored is raw Fourier magnitude.

The station sends `/moire/radius` first, followed by `/moire/intensity`, to `127.0.0.1:9000`. Each list contains one value per oscillator; the default is 400. The transmitted amplitude is:

```text
clip((ln(1 + Fourier magnitude) - Vmin) / (Vmax - Vmin), 0, 1)
```

The original Max patch maps radius 0‚Äì30 to frequency 0‚Äì7000 Hz, with an adjustable upper frequency. This mapping extrapolates outside that radius interval. The default amplitude gate rejects values below 0.05. Each voice has a 20 ms ramp. There is no adaptive bank normalization.

Probe width defaults to one reciprocal pixel sample. Larger widths select the brightest transverse sample and its radius. The displayed line marks the center of the aperture. The revised station samples directly at the requested partial count, so it can differ slightly from the original intermediate resampling.

## Validation and known limitations

Small even- and odd-grid comparisons against the original generator matched the NPZ schema, reciprocal coordinates and amplitudes within floating-point tolerance. Offscreen GUI tests exercised isolated startup without helper files, coordinate entry, caching, 400/2048 partials, width, invalid-mapping handling and stop/close messages. Live OSC reception and audio rendering in Max have not been verified for this revision. No listening study is claimed.

The original Max patches are unchanged. Their `t f b` ‚Üí counter ‚Üí `pack` ordering can emit the previously stored amplitude/frequency value. Sending radius first ensures that the voice-count message is sent before the amplitude list, but does not correct that internal ordering. The bank has no stream-loss watchdog or voice-count normalization. Normal station shutdown requests silence; an application crash can leave a sustained sound. Two UDP messages are not an atomic frame and delivery is not guaranteed.

The finite disk, atom rasterization and chosen probe all influence the audible result. This is a geometric sonification, not a simulation of graphene's acoustic or electronic spectrum.

## Provenance and publication

Original scripts and Max patches were supplied by C√©dric Cazorla. The standalone Python revisions and documentation were prepared with AI assistance during project review. See [PROVENANCE.md](PROVENANCE.md) for the file associations.

Large NPZ libraries are not included and are ignored by Git. Use GitHub Releases or a research-data repository for datasets, and link them here when available. Choose a software license before public distribution; no license has been assigned on the author's behalf. This folder is prepared for upload and has not been published to GitHub.
