HOST=$1
PORT=$2
gst-launch-1.0 -v udpsrc address=$HOST port=$PORT caps="application/x-rtp,channels=(int)2,format=(string)S16LE,media=(string)audio,payload=(int)96,clock-rate=(int)44100,encoding-name=(string)L24" ! rtpL24depay ! audioconvert ! autoaudiosink sync=false > /dev/null &
echo $! # pid of last background process, gstreamer process in this case
