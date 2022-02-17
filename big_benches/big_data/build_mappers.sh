split -b10M meta_input.txt
for f in x*
do
    echo $f
    mv $f input.txt
    cp -r mr_services main
    mv input.txt main/
    cp mapper.sh main/main.sh
    zip -r mr_$f.zip main
    rm -rf main
done
