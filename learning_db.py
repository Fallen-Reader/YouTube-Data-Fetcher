from __future__ import annotations
import os
import sys
from datetime import datetime,timezone
from typing import Optional, List
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint, text
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

load_dotenv()

#DB Setup

DB_PATH = os.getenv("DB_PATH",default="Learning_lib.db")

print(f"{DB_PATH}") 
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


#Models

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False, index=True)
    description = Column(String(512), nullable=True)
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    # relationships
    video_topics = relationship("VideoTopic", back_populates="topic", cascade="all, delete-orphan")
    playlist_topics = relationship("PlaylistTopic", back_populates="topic", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Topic(id={self.id}, name={self.name})>"


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    youtube_id = Column(String(64), nullable=False, index=True)
    title = Column(String(512), nullable=False)
    channel = Column(String(256), nullable=False)
    url = Column(String(1024), nullable=False)
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_checked_at = Column(DateTime, nullable=True)

    views = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    comments = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    uploaded_at = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint("youtube_id", name="uq_videos_youtube_id"),)

    video_topics = relationship("VideoTopic", back_populates="video", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Video(id={self.id}, youtube_id={self.youtube_id}, title={self.title[:30]})>"


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    youtube_id = Column(String(64), nullable=False, index=True)
    title = Column(String(512), nullable=False)
    channel = Column(String(256), nullable=False)
    url = Column(String(1024), nullable=False)
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_checked_at = Column(DateTime, nullable=True)

    item_count = Column(Integer, nullable=True)

    __table_args__ = (UniqueConstraint("youtube_id", name="uq_playlists_youtube_id"),)

    playlist_topics = relationship("PlaylistTopic", back_populates="playlist", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Playlist(id={self.id}, youtube_id={self.youtube_id}, title={self.title[:30]})>"


# Link tables

class VideoTopic(Base):
    __tablename__ = "video_topics"

    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    primary = Column(Boolean, default=False, nullable=False)
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    __table_args__ = (UniqueConstraint("video_id", "topic_id", name="uq_video_topic"),)

    video = relationship("Video", back_populates="video_topics")
    topic = relationship("Topic", back_populates="video_topics")


class PlaylistTopic(Base):
    __tablename__ = "playlist_topics"

    id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    primary = Column(Boolean, default=False, nullable=False)
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    __table_args__ = (UniqueConstraint("playlist_id", "topic_id", name="uq_playlist_topic"),)

    playlist = relationship("Playlist", back_populates="playlist_topics")
    topic = relationship("Topic", back_populates="playlist_topics")


def init_db() -> None:
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return SessionLocal()


def upsert_video(
    youtube_id: str,
    title: str,
    channel: str,
    url: str,
    topics: Optional[List[str]] = None,
    is_verified: bool = False,
    views: Optional[int] = None,
    likes: Optional[int] = None,
    comments: Optional[int] = None,
    duration_seconds: Optional[int] = None,
    uploaded_at: Optional[datetime] = None,
) -> Video:
    sess = get_session()
    try:
        existing = sess.query(Video).filter(Video.youtube_id == youtube_id).first()
        if existing:
            existing.title = title
            existing.channel = channel
            existing.url = url
            existing.is_verified = is_verified or existing.is_verified
            existing.views = views or existing.views
            existing.likes = likes or existing.likes
            existing.comments = comments or existing.comments
            existing.duration_seconds = duration_seconds or existing.duration_seconds
            existing.uploaded_at = uploaded_at or existing.uploaded_at
            existing.last_checked_at = datetime.now(timezone.utc)
        else:
            existing = Video(
                youtube_id=youtube_id,
                title=title,
                channel=channel,
                url=url,
                is_verified=is_verified,
                views=views,
                likes=likes,
                comments=comments,
                duration_seconds=duration_seconds,
                uploaded_at=uploaded_at,
            )
            sess.add(existing)

        # link topics
        if topics:
            for tname in topics:
                topic = sess.query(Topic).filter(Topic.name == tname).first()
                if not topic:
                    topic = Topic(name=tname)
                    sess.add(topic)
                    sess.flush()
                link = sess.query(VideoTopic).filter(
                    VideoTopic.video_id == existing.id, VideoTopic.topic_id == topic.id
                ).first()
                if not link:
                    link = VideoTopic(video_id=existing.id, topic_id=topic.id, primary=False)
                    sess.add(link)

        sess.commit()
        sess.refresh(existing)
        return existing
    except Exception:
        sess.rollback()
        raise
    finally:
        sess.close()


def upsert_playlist(
    youtube_id: str,
    title: str,
    channel: str,
    url: str,
    topics: Optional[List[str]] = None,
    is_verified: bool = False,
    item_count: Optional[int] = None,
) -> Playlist:
    sess = get_session()
    try:
        existing = sess.query(Playlist).filter(Playlist.youtube_id == youtube_id).first()
        if existing:
            existing.title = title
            existing.channel = channel
            existing.url = url
            existing.is_verified = is_verified or existing.is_verified
            existing.item_count = item_count or existing.item_count
            existing.last_checked_at = datetime.now(timezone.utc)
        else:
            existing = Playlist(
                youtube_id=youtube_id,
                title=title,
                channel=channel,
                url=url,
                is_verified=is_verified,
                item_count=item_count,
            )
            sess.add(existing)

        # link topics
        if topics:
            for tname in topics:
                topic = sess.query(Topic).filter(Topic.name == tname).first()
                if not topic:
                    topic = Topic(name=tname)
                    sess.add(topic)
                    sess.flush()
                link = sess.query(PlaylistTopic).filter(
                    PlaylistTopic.playlist_id == existing.id, PlaylistTopic.topic_id == topic.id
                ).first()
                if not link:
                    link = PlaylistTopic(playlist_id=existing.id, topic_id=topic.id, primary=False)
                    sess.add(link)

        sess.commit()
        sess.refresh(existing)
        return existing
    except Exception:
        sess.rollback()
        raise
    finally:
        sess.close()


#CLI

def cli_add_video(youtube_id: str, title: str, channel: str, url: str, topics_str: str) -> None:
    topics = [t.strip() for t in topics_str.split(",") if t.strip()]
    video = upsert_video(youtube_id, title, channel, url, topics=topics)
    print(f"[OK] Video added/updated: {video.id} | {video.title} | topics: {topics}")


def cli_add_playlist(youtube_id: str, title: str, channel: str, url: str, topics_str: str) -> None:
    topics = [t.strip() for t in topics_str.split(",") if t.strip()]
    playlist = upsert_playlist(youtube_id, title, channel, url, topics=topics)
    print(f"[OK] Playlist added/updated: {playlist.id} | {playlist.title} | topics: {topics}")


def cli_list_videos_by_topic(topic_name: str, limit: int = 20) -> None:
    sess = get_session()
    try:
        topic = sess.query(Topic).filter(Topic.name == topic_name).first()
        if not topic:
            print(f"No topic found: {topic_name}")
            return
        videos = (
            sess.query(Video)
            .join(VideoTopic)
            .filter(VideoTopic.topic_id == topic.id)
            .order_by(Video.added_at.desc())
            .limit(limit)
            .all()
        )
        if not videos:
            print(f"No videos for topic: {topic_name}")
            return
        print(f"\n=== Videos for topic '{topic_name}' ({len(videos)}) ===")
        for v in videos:
            print(f"{v.id}. [{v.title}] — {v.channel}")
            print(f"   -> {v.url}")
        print()
    finally:
        sess.close()


def cli_list_playlists_by_topic(topic_name: str, limit: int = 20) -> None:
    sess = get_session()
    try:
        topic = sess.query(Topic).filter(Topic.name == topic_name).first()
        if not topic:
            print(f"No topic found: {topic_name}")
            return
        playlists = (
            sess.query(Playlist)
            .join(PlaylistTopic)
            .filter(PlaylistTopic.topic_id == topic.id)
            .order_by(Playlist.added_at.desc())
            .limit(limit)
            .all()
        )
        if not playlists:
            print(f"No playlists for topic: {topic_name}")
            return
        print(f"\n=== Playlists for topic '{topic_name}' ({len(playlists)}) ===")
        for p in playlists:
            print(f"{p.id}. [{p.title}] — {p.channel}")
            print(f"   -> {p.url}")
        print()
    finally:
        sess.close()


def cli_add_topic(name: str, description: str = "") -> None:
    sess = get_session()
    try:
        topic = sess.query(Topic).filter(Topic.name == name).first()
        if topic:
            print(f"[OK] Topic already exists: {topic.id} | {topic.name}")
        else:
            topic = Topic(name=name, description=description)
            sess.add(topic)
            sess.commit()
            print(f"[OK] Topic created: {topic.id} | {topic.name}")
    finally:
        sess.close()


def cli_main() -> None:
    init_db()
    if len(sys.argv) < 2:
        print("Usage (examples):")
        print("  python learning_db.py add-video <yt_id> <title> <channel> <url> <topic1,topic2>")
        print("  python learning_db.py add-playlist <yt_id> <title> <channel> <url> <topic1,topic2>")
        print("  python learning_db.py list-videos <topic_name>")
        print("  python learning_db.py list-playlists <topic_name>")
        print("  python learning_db.py add-topic <topic_name>")
        return

    cmd = sys.argv[1]

    if cmd == "add-video":
        if len(sys.argv) < 7:
            print("Missing args for add-video")
            return
        cli_add_video(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

    elif cmd == "add-playlist":
        if len(sys.argv) < 7:
            print("Missing args for add-playlist")
            return
        cli_add_playlist(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

    elif cmd == "list-videos":
        if len(sys.argv) < 3:
            print("Missing topic name for list-videos")
            return
        cli_list_videos_by_topic(sys.argv[2])

    elif cmd == "list-playlists":
        if len(sys.argv) < 3:
            print("Missing topic name for list-playlists")
            return
        cli_list_playlists_by_topic(sys.argv[2])

    elif cmd == "add-topic":
        if len(sys.argv) < 3:
            print("Missing topic name for add-topic")
            return
        cli_add_topic(sys.argv[2])

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    cli_main()