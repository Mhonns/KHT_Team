# Change the directory
cd KHT_Team/Src

# Kill old server
pid=$(cat pid_file.txt)
if ps -p $pid > /dev/null; then
    kill $pid
else
    echo "Process $pid not found"
fi

# Starting new server 
rm nohup.out
nohup python3 api_provider2.py &
echo $! > pid_file.txt

# Swith the directory back
cd ../..
exit
