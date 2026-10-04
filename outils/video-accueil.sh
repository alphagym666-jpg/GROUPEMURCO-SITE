#!/bin/bash
# Régénérer : outils/video-accueil.sh 1280 720 photos/hero-video  et  FX1=0.14 outils/video-accueil.sh 720 1280 photos/hero-video-mobile
# Usage: make.sh W H out_prefix   — monte la vidéo d'arrière-plan à partir des photos
set -e
W=$1; H=$2; OUT=$3; P=/home/user/GROUPEMURCO-SITE/photos; T=$(dirname $0)/tmp_$W; mkdir -p $T
FPS=30
# scene IMG DUR ZOOM_FROM ZOOM_TO FX FY (FX/FY = point de mire 0..1) -> clip
scene () {
  local img=$1 dur=$2 z0=$3 z1=$4 fx=$5 fy=$6 out=$7
  local N=$(echo "$dur*$FPS" | bc | cut -d. -f1)
  ffmpeg -loglevel error -y -loop 1 -i $img -vf "scale=-2:2160,setsar=1,crop='min(iw,ih*$W/$H)':'min(ih,iw*$H/$W)':'(iw-min(iw,ih*$W/$H))*$fx':'(ih-min(ih,iw*$H/$W))*$fy',scale=${W}*3:${H}*3,zoompan=z='$z0+($z1-$z0)*on/$N':x='(iw-iw/zoom)*$fx':y='(ih-ih/zoom)*$fy':d=1:s=${W}x${H}:fps=$FPS,eq=contrast=1.06:saturation=1.08,vignette=PI/5" -frames:v $N -pix_fmt yuv420p -c:v libx264 -crf 14 -preset veryfast $out
}
scene $P/hero-fond.jpg 4.2 1.0 1.12 ${FX1:-0.18} 0.45 $T/s1.mp4
scene $P/gouttiere-avant.jpg 5.0 1.04 1.16 0.5 0.5 $T/s2a.mp4
scene $P/gouttiere-apres.jpg 5.0 1.04 1.16 0.5 0.5 $T/s2b.mp4
# révélation : un balayage doux fait passer la gouttière d'« avant » à « après »
ffmpeg -loglevel error -y -i $T/s2a.mp4 -i $T/s2b.mp4 -filter_complex "[0][1]blend=all_expr='A*clip((X-W*clip((T-1.3)/2.2\,0\,1))/70+0.5\,0\,1)+B*(1-clip((X-W*clip((T-1.3)/2.2\,0\,1))/70+0.5\,0\,1))',format=yuv420p" -c:v libx264 -crf 14 -preset veryfast $T/s2.mp4
scene $P/protege-gouttieres.jpg 3.8 1.14 1.02 0.3 0.5 $T/s3.mp4
scene $P/hero-fond.jpg 1.2 1.0 1.0 ${FX1:-0.18} 0.45 $T/s5.mp4
X=0.7
ffmpeg -loglevel error -y -i $T/s1.mp4 -i $T/s2.mp4 -i $T/s3.mp4 -i $T/s5.mp4 -filter_complex "\
[0][1]xfade=transition=fade:duration=$X:offset=3.5[a];\
[a][2]xfade=transition=smoothleft:duration=$X:offset=7.8[b];\
[b][3]xfade=transition=fade:duration=$X:offset=10.9,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -profile:v high -crf 27 -preset slow -movflags +faststart $OUT.mp4
ffmpeg -loglevel error -y -i $OUT.mp4 -an -c:v libvpx-vp9 -crf 40 -b:v 0 -row-mt 1 -deadline good -cpu-used 2 $OUT.webm
ffmpeg -loglevel error -y -ss 0.2 -i $OUT.mp4 -frames:v 1 -q:v 4 $OUT-poster.jpg
rm -rf $T
