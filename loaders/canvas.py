from typing import Any
import logs
from exceptions import *

from loaders import DataEntry, Loader, CompositeLoader
from connections import connection_manager

logger = logs.get('loader')
class AnnouncementLoader(Loader):
    def __init__(self):
        super().__init__('announcement')

    def load(self, settings: dict[str, Any]) -> list[DataEntry]:
        # Get canvas connection
        canvas_conn_id = settings.get('connection')
        if canvas_conn_id is None:
            logger.error(f"Canvas loader '{settings['id']}' is missing connection id")
            raise LoaderError(f"Canvas loader '{settings['id']}' is missing connection id")
        canvas_conn = connection_manager.getConnection(canvas_conn_id, 'canvas')
        if canvas_conn is None:
            logger.error(f"Canvas loader '{settings['id']}' has connection id which does not correspond to any Canvas connection")
            raise LoaderError(f"Canvas loader '{settings['id']}' has connection id which does not correspond to any Canvas connection")
        canvas = canvas_conn.getCanvas()

        # Get course
        course_id = settings['course_id']
        course = canvas.get_course(course_id)

        # Load announcements
        topic_ids = settings['topic_ids']
        if type(topic_ids) is str:
            if topic_ids == "*":
                topics = course.get_discussion_topics(only_announcements=True)
                topic_ids = [str(t.id) for t in topics]
            else:
                topic_ids = [topic_ids]

        res = []
        for topic_id in topic_ids:
            topic = course.get_discussion_topic(topic_id)
            res.append(DataEntry(topic.message, topic_id))

        return res

class CanvasLoader(CompositeLoader):
    def __init__(self):
        super().__init__('canvas')

        self.registerChild(AnnouncementLoader())

