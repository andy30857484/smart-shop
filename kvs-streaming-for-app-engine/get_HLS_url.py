from flask import Flask, render_template, session, request, redirect, url_for, Response, jsonify
import boto3
import datetime,time
from datetime import timedelta
import kvsconfig
import shadowProxy

app = Flask(__name__)

@app.route("/kvslive")
def hls():
    #STREAM_NAME = request.args['device']
    STREAM_NAME = 'monitor'
    kinesisVideoClient = boto3.client("kinesisvideo",aws_access_key_id = kvsconfig.aws_access_key , 
                      aws_secret_access_key = kvsconfig.aws_secret_key , 
                      region_name = kvsconfig.aws_region_name)
    endpoint = kinesisVideoClient.get_data_endpoint(
    APIName="GET_HLS_STREAMING_SESSION_URL",
    StreamARN = kvsconfig.hls_stream_ARN
    )['DataEndpoint']
    # Grab the HLS Stream URL from the endpoint
    kinesisVideoArchivedMediaClient = boto3.client("kinesis-video-archived-media",aws_access_key_id = kvsconfig.aws_access_key, 
                      aws_secret_access_key = kvsconfig.aws_secret_key , 
                      region_name = kvsconfig.aws_region_name,endpoint_url=endpoint)
    url = kinesisVideoArchivedMediaClient.get_hls_streaming_session_url(
        StreamName = STREAM_NAME,
        PlaybackMode="LIVE",
        HLSFragmentSelector={
            'FragmentSelectorType': 'PRODUCER_TIMESTAMP',
        },
        ContainerFormat='FRAGMENTED_MP4',
        DiscontinuityMode='NEVER',
        DisplayFragmentTimestamp='NEVER',
    )['HLSStreamingSessionURL']
    print("HLS URL:", url)
    
    
    return render_template('HLS.html',url=url)
    
    
@app.route("/playback",methods=['GET', 'POST'])
def hlsplayback():
    #STREAM_NAME = request.args['device']
    STREAM_NAME = 'monitor'
    kinesisVideoClient = boto3.client("kinesisvideo",aws_access_key_id = kvsconfig.aws_access_key , 
                      aws_secret_access_key = kvsconfig.aws_secret_key , 
                      region_name = kvsconfig.aws_region_name)
    
    playBackSecond = shadowProxy.get(STREAM_NAME)
    
    com = 0
    if (playBackSecond % 2) == 0:
        com = 0
    else:
        com = 1
    playBackSecondBefore=int(playBackSecond)/2
    playBackSecondBefore=int(playBackSecondBefore)
    
    playBackSecondAfter=int(playBackSecond)/2
    playBackSecondAfter=int(playBackSecondAfter)
    
    playBackSecondAfter=playBackSecondAfter+com

    utc=8
    
    timestamp = request.args['timestamp']
    timestamp = str(datetime.datetime.utcfromtimestamp(int(timestamp) + 28800).strftime('%Y-%m-%d %H:%M:%S'))

    startTime = timestamp
    endTime = timestamp
    
    startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
    startTime = startTime + datetime.timedelta(hours=-utc)
    startTime = startTime + datetime.timedelta(seconds=-playBackSecondBefore)
    startTime = datetime.datetime.strftime(startTime,'%Y-%m-%d %H:%M:%S')
    
    endTime = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
    endTime = endTime + datetime.timedelta(hours=-utc)
    endTime = endTime + datetime.timedelta(seconds=+playBackSecondAfter)
    endTime = datetime.datetime.strftime(endTime,'%Y-%m-%d %H:%M:%S')
    
    
    
    endpoint = kinesisVideoClient.get_data_endpoint(
    APIName="GET_HLS_STREAMING_SESSION_URL",
    StreamARN = kvsconfig.hls_stream_ARN
    )['DataEndpoint']
    # Grab the HLS Stream URL from the endpoint
    kinesisVideoArchivedMediaClient = boto3.client("kinesis-video-archived-media",aws_access_key_id = kvsconfig.aws_access_key, 
                      aws_secret_access_key = kvsconfig.aws_secret_key , 
                      region_name = kvsconfig.aws_region_name,endpoint_url=endpoint)
    url = kinesisVideoArchivedMediaClient.get_hls_streaming_session_url(
        StreamName=STREAM_NAME,
        PlaybackMode="ON_DEMAND",
        HLSFragmentSelector={
            'FragmentSelectorType': 'PRODUCER_TIMESTAMP',
            'TimestampRange': {
                'StartTimestamp': startTime,
                'EndTimestamp': endTime
            }
        },
        ContainerFormat='FRAGMENTED_MP4',
        DiscontinuityMode='NEVER',
        DisplayFragmentTimestamp='NEVER',
        Expires=3600,
        MaxMediaPlaylistFragmentResults=1000
    )['HLSStreamingSessionURL']
    print("HLS URL:", url)

    
    return render_template('HLS.html',url=url)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)