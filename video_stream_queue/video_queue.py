import cv2
import time
from threading import Lock
from video_stream_queue.my_queue import MyQueue


class VideoQueue(MyQueue):
    # class to read videos using threads

    def __init__(self, queue_size=1, path=0, clear_queue=False, fps=None):
        MyQueue.__init__(self, queue_size)
        self.cap = self.get_video_cap(path)
        self.path = path
        self.fps = int(self.cap.get(5)) if fps is None else fps
        self.clear_queue = clear_queue
        self.is_finished_lock = Lock()
        self.is_finished = False
        
    
    @property
    def is_finished(self):
        self.is_finished_lock.acquire(True)
        val = self.__is_finished
        self.is_finished_lock.release()
        return val

    @is_finished.setter
    def is_finished(self, val):
        self.is_finished_lock.acquire(True)
        self.__is_finished = val
        self.is_finished_lock.release()
        
    def get_video_cap(self, path):
        # check if video capture works
        cap = cv2.VideoCapture(path)
        if cap.isOpened() is False:
            raise FileNotFoundError(
                'Video stream or file not found at {}'.format(path))
        else:
            return cap

    def run(self):
        last_added_frame_time = 0
        while self.thread.is_running:
            if not self.full():
                # read current frame from capture
                ret, frame = self.cap.read()
                if not ret:
                    self.logger.log(30, 'Thread has stopped due to not ret')
                    self.is_stopped = True
                else:
                    # self.logger.debug('Added frame to queue')
                    self.logger.log(
                        0, 'Last frame was added {} s ago'.format(
                            time.time() - last_added_frame_time))
                    last_added_frame_time = time.time()
                    self.put(frame)
                    self.logger.log(0, 'Current size of queue: {}'.format(
                        self.qsize()))
            # If the queue is full, clear it and reset. Only for streams
            else:
                if self.clear_queue:
                    self.clear()
                    self.logger.log(10,
                        'Queue reached maximum capacity '
                        '({}). Cleared'.format(self.maxsize))
                else:
                    # self.logger.debug('SLEEPING for {:.3f}'.format(
                    #   timespace_frames))
                    time.sleep(1/self.fps)
            if self.is_stopped:
                break
        self.logger.log(20, 'videoThread not running')
        self.thread.is_running = False
