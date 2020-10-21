name = "video_stream_queue"
__all__ = ['my_queue', 'my_thread', 'stream_queue', 'video_queue']
# deprecated to keep older scripts who import this from breaking
from video_stream_queue.stream_queue import StreamQueue
from video_stream_queue.video_queue import VideoQueue
from video_stream_queue.my_queue import MyQueue
from video_stream_queue.my_thread import MyThread