# Sanitized FindIt AI walkthrough

[Watch the 38-second MP4](findit-ai-synthetic-walkthrough.mp4).

This is a silent, captioned technical explainer assembled entirely from **synthetic examples** and the architecture illustration in this repository. It does not contain recordings, screenshots, audio, endpoints, configuration, customer data, or credentials from any company deployment.

The sample counts and search result correspond to the runnable examples in this repository, not production measurements. The Laya frames distinguish observation-only shadow mode from a narrow conditional pilot; universal ML-driven production routing is not claimed.

## Rebuild

On Linux with `ffmpeg` (libx264 and drawtext enabled) and Inkscape installed:

```bash
bash scripts/build_synthetic_video.sh
```

The script regenerates `media/findit-ai-synthetic-walkthrough.mp4` from authored graphics and explanatory text. It does not read client files or contact external services. It uses the standard DejaVu Sans fonts; adapt the font paths if needed on other systems.

The original internal demonstration recordings were deliberately excluded from public release because some frames show deployment configuration and network identifiers.
