# Media Samples

This directory stores outputs generated with the CLI. The repository keeps only this README so the folder stays visible online.

To create an example slideshow locally, run:

```bash
python -m app.cli \
  --prompt "manga girl in neon city" \
  --mode video \
  --frame-count 8 \
  --fps 4 \
  --output media/sample.avi
```

The command writes `sample.avi` into this directory. Because binary files make pull requests harder to review, the generated video is not tracked by Git—feel free to delete or regenerate it whenever needed.
