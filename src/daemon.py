import logging
from abc import ABCMeta, abstractmethod

from pub import Publisher

logger = logging.getLogger('run.daemon')


class VideoDaemon(metaclass=ABCMeta):
    def __init__(self, user_config):
        super().__init__()
        self.user_config = user_config
        self.target_id = user_config['target_id']
        self.current_live = None
        self.pub = Publisher()

    def run(self) -> None:
        try:
            self.check()
        except KeyboardInterrupt:
            exit(0)

    @abstractmethod
    def check(self):
        pass

    def set_live(self, video_dict: dict) -> None:
        if not video_dict['Target'] == self.current_live:
            self.current_live = video_dict['Target']
            logger.info(f'Find a live {video_dict}')
            self.pub.do_publish(video_dict)
        else:
            logger.info(f'drop the same live {video_dict}')