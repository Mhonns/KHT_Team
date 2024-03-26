# Change the directory
cd KHT_Team/Src

# Kill old server
pid=$(cat pid_file.txt)
if ps -p $pid > /dev/null; then
    kill $pid
else
    echo "Process $pid not found"
fi
echo "--Successfully kill old server--"

# Starting new server 
rm -f nohup.out
nohup python3 api_provider2.py &
echo $! > pid_file.txt
echo "--Successfully create server--"
echo "Start the server at host 0.0.0.0 port 443"

# Kill old local server
local_pid=$(cat local_pid_file.txt)
if ps -p $local_pid > /dev/null; then
    kill $local_pid
else
    echo "Process $local_pid not found"
fi
echo "--Successfully kill old local server--"

# Starting new local server
rm -f local_nohup.out
nohup python3 api_provider2.py '127.0.0.3' '2546' &> local_nohup.out &
echo $! > local_pid_file.txt
echo "--Successfully create local server--"
echo "Start the local server at host 127.0.0.3 port 2546"

# Swith the directory back
cd ../..
exit
