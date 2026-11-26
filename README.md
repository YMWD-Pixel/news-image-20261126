# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/YMWD-Pixel/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/YMWD-Pixel/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-page newspaper front page summing up the world news of Thursday 26 November 2026, drawn from scratch with Python and Pillow. Lead story: Washington's new tariff salvo on 14 trading partners and the market slide; plus the Ukraine war toll, Gaza, Sudan, space firsts, Nvidia's comeback and Colombia's peace-decade anniversary.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the shipped `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. To redraw the image from scratch, run `python3 draw_image.py` (requires Pillow); it writes a deterministic 1024×1024 PNG.

---

<sub>Entered on [make.fun](https://make.fun/?ref=fxcrjdqj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
