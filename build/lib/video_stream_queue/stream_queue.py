import cv2
import time
from video_stream_queue.my_queue import MyQueue


class StreamQueue(MyQueue):
    # class to read streams using threads

    def __init__(self, queue_size=1, path=0, fps=30, clear_queue=False):
        MyQueue.__init__(self, queue_size)
        self.cap = self.get_video_cap(path)
        self.path = path
        self.fps = fps
        self.clear_queue = clear_queue

    def get_video_cap(self, path):
        # check if video capture works
        cap = cv2.VideoCapture(path)
        if cap.isOpened() is False:
            raise FileNotFoundError(
                'Video stream or file not found at {}'.format(path))
        else:
            return cap

    def run(self):
        last_fps_time = time.time()
        timespace_frames = 1 / self.fps
        while self.thread.is_running:
            if (time.time() - last_fps_time) > timespace_frames:
                if not self.full():
                    # read current frame from capture
                    ret, frame = self.cap.read()
                    last_fps_time = time.time()
                    if not ret:
                        self.logger.log(30, 'Thread has stopped due to not ret')
                        self.is_stopped = True
                    self.logger.log(10, 'Added frame to queue')
                    self.put(frame)
                    self.logger.log(10, 'Current size of queue: {}'.format(
                        self.qsize()))
                    self.logger.log(10, 'SLEEPING for {:.2f}'.format(
                        timespace_frames))
                # If the queue is full, clear it and reset if not buffer.
                else:
                    if self.clear_queue:
                        self.clear()
                        self.logger.log(10, 
                            'Queue reached maximum capacity '
                            '({}). Cleared'.format(self.maxsize))
                    else:
                        # self.logger.debug('SLEEPING for {:.3f}'.format(
                        #   timespace_frames))
                        time.sleep(timespace_frames)
            if self.is_stopped:
                break
        self.logger.info('videoThread not running')
        self.thread.is_running = False
        self.is_running = False
