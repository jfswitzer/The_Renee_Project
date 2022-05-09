echo '== Basic Fibonacci =='
rm main.zip
cp test_codes/simple/main.zip .
python3.8 send_single.py --zipfile main.zip
echo '== Basic Fibonacci Complete =='

echo '== Persistent Task 1 Minute =='
rm main.zip
cp test_codes/loop/main.zip .
python3.8 send_single.py --zipfile main.zip
echo '== Persistent Task 1 Minute Complete =='

echo '== Write to Bucket =='
rm main.zip
cp test_codes/storage_test/main.zip .
python3.8 send_single.py --zipfile main.zip
echo '== Write to Bucket Complete =='

echo '== Mapper =='
rm main.zip
cp test_codes/mapper/main.zip .
python3.8 send_single.py --zipfile main.zip
echo '== Mapper Complete'

echo '== Reducer =='
rm main.zip
cp test_codes/reducer/main.zip .
python3.8 send_single.py --zipfile main.zip
echo '== Reducer Complete'

rm main.zip
