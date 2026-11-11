#!/usr/bin/env bash
set -euo pipefail

# Produces a deliberately synthetic portfolio walkthrough. No customer footage,
# secrets, real endpoints, FileMaker data, or deployment configuration are used.
# Dependencies: ffmpeg (with drawtext and libx264) and Inkscape.

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output_path="$project_dir/media/findit-ai-synthetic-walkthrough.mp4"
work_dir="$(mktemp -d)"
font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

mkdir -p "$project_dir/media"
inkscape "$project_dir/assets/findit-architecture.svg" \
  --export-type=png --export-filename="$work_dir/architecture.png" \
  --export-width=1050 >/dev/null 2>&1

render_card() {
  local filename="$1" duration="$2" filters="$3"
  ffmpeg -hide_banner -loglevel error -f lavfi \
    -i "color=c=0x0c152d:s=1280x720:r=15:d=$duration" \
    -vf "$filters" -c:v libx264 -preset medium -crf 32 \
    -pix_fmt yuv420p -an "$work_dir/$filename.mp4"
}

render_card intro 6 \
  "drawbox=x=72:y=85:w=10:h=115:color=0x5ed1d9:t=fill,\
drawtext=fontfile=$font_bold:text='FindIt AI':fontsize=78:fontcolor=white:x=112:y=91,\
drawtext=fontfile=$font:text='Enterprise assistant - engineering walkthrough':fontsize=31:fontcolor=0xb7cce7:x=112:y=205,\
drawbox=x=93:y=339:w=1094:h=194:color=0x1b304c:t=fill,\
drawtext=fontfile=$font_bold:text='Three answer paths':fontsize=35:fontcolor=0x74d9e1:x=129:y=365,\
drawtext=fontfile=$font:text='Structured facts     Semantic discovery     LLM explanation':fontsize=26:fontcolor=white:x=129:y=430,\
drawtext=fontfile=$font:text='Synthetic public reference  |  No client environments shown':fontsize=22:fontcolor=0xa8bfdc:x=129:y=579"

ffmpeg -hide_banner -loglevel error -loop 1 -framerate 15 \
  -i "$work_dir/architecture.png" -t 8 \
  -vf 'scale=1050:720,pad=1280:720:(ow-iw)/2:0:color=0x0c152d,setsar=1' \
  -c:v libx264 -preset medium -crf 32 -pix_fmt yuv420p \
  -an "$work_dir/architecture.mp4"

render_card structured 6 \
  "drawbox=x=78:y=78:w=10:h=85:color=0x56c8d8:t=fill,\
drawtext=fontfile=$font_bold:text='01  Exact facts':fontsize=53:fontcolor=white:x=112:y=78,\
drawtext=fontfile=$font:text='Question':fontsize=23:fontcolor=0x87b5cf:x=102:y=219,\
drawbox=x=95:y=255:w=1090:h=111:color=0x203d59:t=fill,\
drawtext=fontfile=$font_bold:text='How many open tasks are assigned to me?':fontsize=27:fontcolor=white:x=123:y=286,\
drawbox=x=95:y=406:w=1090:h=142:color=0x18384e:t=fill,\
drawtext=fontfile=$font:text='route = structured':fontsize=30:fontcolor=0x7ddfea:x=124:y=437,\
drawtext=fontfile=$font_bold:text='result = 2 open tasks':fontsize=34:fontcolor=white:x=124:y=485,\
drawtext=fontfile=$font:text='Deterministic scoped query. Illustrative records only.':fontsize=22:fontcolor=0xb2c6e0:x=102:y=588"

render_card semantic 6 \
  "drawbox=x=78:y=78:w=10:h=85:color=0xa6e390:t=fill,\
drawtext=fontfile=$font_bold:text='02  Meaning-based search':fontsize=53:fontcolor=white:x=112:y=78,\
drawtext=fontfile=$font:text='Question':fontsize=23:fontcolor=0x87b5cf:x=102:y=219,\
drawbox=x=95:y=255:w=1090:h=111:color=0x203d59:t=fill,\
drawtext=fontfile=$font_bold:text='Find discussions about approvals':fontsize=29:fontcolor=white:x=123:y=287,\
drawbox=x=95:y=406:w=1090:h=142:color=0x203b37:t=fill,\
drawtext=fontfile=$font:text='route = semantic':fontsize=30:fontcolor=0xb8eda9:x=124:y=437,\
drawtext=fontfile=$font_bold:text='result = 1 verified hit':fontsize=34:fontcolor=white:x=124:y=485,\
drawtext=fontfile=$font:text='Candidates are checked against fresh source content.':fontsize=22:fontcolor=0xb2c6e0:x=102:y=588"

render_card research 6 \
  "drawbox=x=78:y=78:w=10:h=85:color=0xc8a9ff:t=fill,\
drawtext=fontfile=$font_bold:text='03  Laya research boundaries':fontsize=51:fontcolor=white:x=112:y=78,\
drawbox=x=95:y=243:w=1090:h=111:color=0x302949:t=fill,\
drawtext=fontfile=$font_bold:text='v0.8.x   Observation-only shadow':fontsize=30:fontcolor=0xe8d7ff:x=124:y=266,\
drawtext=fontfile=$font:text='Measures and logs. Does not override answers.':fontsize=22:fontcolor=0xb2c6e0:x=124:y=313,\
drawbox=x=95:y=384:w=1090:h=111:color=0x302949:t=fill,\
drawtext=fontfile=$font_bold:text='v0.9.3   Narrow gated pilot':fontsize=30:fontcolor=0xe8d7ff:x=124:y=407,\
drawtext=fontfile=$font:text='Read-only, conditional, with fallback.':fontsize=22:fontcolor=0xb2c6e0:x=124:y=454,\
drawtext=fontfile=$font:text='Universal production routing is NOT claimed.':fontsize=24:fontcolor=0xf5c991:x=102:y=569"

render_card outro 6 \
  "drawbox=x=76:y=79:w=10:h=110:color=0x5ed1d9:t=fill,\
drawtext=fontfile=$font_bold:text='Explore the public reference':fontsize=52:fontcolor=white:x=108:y=90,\
drawtext=fontfile=$font:text='Source code + tests + architecture + honest limitations':fontsize=26:fontcolor=0xb6cbe2:x=108:y=197,\
drawbox=x=99:y=326:w=1078:h=106:color=0x203d59:t=fill,\
drawtext=fontfile=$font_bold:text='github.com/Sh3bh4m/findit-ai':fontsize=38:fontcolor=0x8ce1e7:x=130:y=356,\
drawtext=fontfile=$font:text='14 passing unit tests  |  Synthetic data only  |  No live integrations':fontsize=22:fontcolor=0xb7cce7:x=108:y=505,\
drawtext=fontfile=$font:text='Design and engineering by Shubham Gopale':fontsize=20:fontcolor=0x96adc9:x=108:y=616"

printf "file '%s'\n" "$work_dir/intro.mp4" "$work_dir/architecture.mp4" \
  "$work_dir/structured.mp4" "$work_dir/semantic.mp4" \
  "$work_dir/research.mp4" "$work_dir/outro.mp4" > "$work_dir/concat.txt"

ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i "$work_dir/concat.txt" \
  -c copy -movflags +faststart -y "$output_path"
printf 'Created %s\n' "$output_path"
