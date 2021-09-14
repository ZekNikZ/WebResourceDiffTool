from typing import Any
from canvasapi import Canvas

from loaders import DataEntry, Loader, CompositeLoader

class AnnouncementLoader(Loader):
    def __init__(self):
        super().__init__('announcement')

    def load(self, settings: dict[str, Any]) -> list[DataEntry]:
        course_id = settings['course_id']
        course = canvas.get_course(course_id)

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

