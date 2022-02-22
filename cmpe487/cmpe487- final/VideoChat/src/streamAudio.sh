HOST=$1
PORT=$2
gst-launch-1.0 -v autoaudiosrc ! audioconvert ! rtpL24pay ! udpsink host=$HOST  port=$PORT > /dev/null &
echo $! # pid of the last backgrounded task, gstreamer in this case
