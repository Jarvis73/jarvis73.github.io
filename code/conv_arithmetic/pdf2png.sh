#! /bin/sh

if [[ ! -d $1 ]]
then
    multiple_space='    '
    echo Require source directory, such as 
    echo 
    echo "${multiple_space}bash pdf2png.sh 201906_conv_v2"
    echo 
    exit
fi

mkdir -p $1_png

shopt -s nullglob
array=($1/fig_*.pdf)
shopt -u nullglob

for file in "${array[@]}"
do
    outfile=$1_png/$(basename $file)
    outfile=${outfile%".pdf"}".png"
    echo $file "->" $outfile
    convert -background white -alpha remove -density 300 -quality 100 $file $outfile
done
