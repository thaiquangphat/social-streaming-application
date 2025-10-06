from __future__ import annotations

import sys
import os
ROOT_DIR = os.path.abspath(
    os.path.join(__file__, '../..')
)
print(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)


import json
import signal
import sys
from datetime import datetime
from typing import Any, Callable

from confluent_kafka import Consumer, KafkaError, KafkaException
from loguru import logger

from app.clients.schema import RedditCommentEvent, RedditSubmissionEvent
from app.config import load_settings


class KafkaConsumerError(RuntimeError):
    """Raised when Kafka consumer encounters an error."""


class RedditKafkaConsumer:
    """
    Consumer for Reddit events from Kafka topics.
    
    Handles both submissions and comments with proper deserialization
    and error handling.
    """
    
    def __init__(
        self,
        *,
        group_id: str = "reddit-consumer-group",
        auto_offset_reset: str = "earliest",
        enable_auto_commit: bool = True,
    ):
        self.settings = load_settings()
        self.group_id = group_id
        self.running = False
        
        consumer_config = self._build_consumer_config(
            group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            enable_auto_commit=enable_auto_commit,
        )
        
        try:
            self.consumer = Consumer(consumer_config)
            logger.info(f"Kafka consumer initialized with group_id: {group_id}")
        except Exception as e:
            raise KafkaConsumerError(f"Failed to initialize Kafka consumer: {e}") from e
    
    def _build_consumer_config(
        self,
        group_id: str,
        auto_offset_reset: str,
        enable_auto_commit: bool,
    ) -> dict[str, Any]:
        """Build Kafka consumer configuration from settings."""
        config: dict[str, Any] = {
            "bootstrap.servers": self.settings.kafka.KAFKA_BOOTSTRAP_SERVERS,
            "group.id": group_id,
            "auto.offset.reset": auto_offset_reset,
            "enable.auto.commit": enable_auto_commit,
            "client.id": f"{self.settings.kafka.KAFKA_CLIENT_ID}-consumer",
        }
        return config
    
    def _deserialize_message(self, value: bytes) -> dict[str, Any]:
        """Deserialize JSON message from Kafka."""
        try:
            return json.loads(value.decode("utf-8"))
        except Exception as e:
            raise KafkaConsumerError(f"Failed to deserialize message: {e}") from e
    
    def _parse_envelope(self, envelope: dict[str, Any]) -> tuple[str, Any]:
        """
        Parse envelope and return entity_type and parsed payload.
        
        Returns:
            Tuple of (entity_type, parsed_event_object)
        """
        entity_type = envelope.get("entity_type")
        payload = envelope.get("payload", {})
        
        if entity_type == "reddit_submission":
            event = RedditSubmissionEvent(**payload)
        elif entity_type == "reddit_comment":
            event = RedditCommentEvent(**payload)
        else:
            raise KafkaConsumerError(f"Unknown entity_type: {entity_type}")
        
        return entity_type, event
    
    def subscribe(self, topics: list[str]) -> None:
        """Subscribe to one or more Kafka topics."""
        try:
            self.consumer.subscribe(topics)
            logger.info(f"Subscribed to topics: {topics}")
        except Exception as e:
            raise KafkaConsumerError(f"Failed to subscribe to topics: {e}") from e
    
    def consume(
        self,
        *,
        timeout: float = 1.0,
        on_submission: Callable[[RedditSubmissionEvent, dict], None] | None = None,
        on_comment: Callable[[RedditCommentEvent, dict], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> None:
        """
        Consume messages from subscribed topics.
        
        Args:
            timeout: Poll timeout in seconds
            on_submission: Callback for submission events
            on_comment: Callback for comment events
            on_error: Callback for errors
        """
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.info("Starting message consumption...")
        message_count = 0
        
        try:
            while self.running:
                msg = self.consumer.poll(timeout=timeout)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.debug(
                            f"Reached end of partition {msg.partition()} "
                            f"at offset {msg.offset()}"
                        )
                        continue
                    else:
                        error = KafkaConsumerError(f"Kafka error: {msg.error()}")
                        logger.error(str(error))
                        if on_error:
                            on_error(error)
                        continue
                
                try:
                    # Deserialize message
                    envelope = self._deserialize_message(msg.value())
                    
                    # Extract metadata
                    metadata = {
                        "topic": msg.topic(),
                        "partition": msg.partition(),
                        "offset": msg.offset(),
                        "timestamp": msg.timestamp()[1] if msg.timestamp()[0] != -1 else None,
                        "key": msg.key().decode("utf-8") if msg.key() else None,
                    }
                    

                    entity_type, event = self._parse_envelope(envelope)
                    
                    # Route to appropriate callback
                    if entity_type == "reddit_submission" and on_submission:
                        on_submission(event, metadata)
                    elif entity_type == "reddit_comment" and on_comment:
                        on_comment(event, metadata)
                    
                    message_count += 1
                    
                    if message_count % 100 == 0:
                        logger.info(f"Processed {message_count} messages")
                
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    if on_error:
                        on_error(e)
        
        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user")
        except Exception as e:
            logger.error(f"Consumer error: {e}", exc_info=True)
            raise
        finally:
            self.close()
            logger.info(f"Consumer stopped. Total messages processed: {message_count}")
    
    def close(self) -> None:
        """Close the consumer and clean up resources."""
        try:
            self.consumer.close()
            logger.info("Kafka consumer closed successfully")
        except Exception as e:
            logger.warning(f"Error closing consumer: {e}")


def example_submission_handler(event: RedditSubmissionEvent, metadata: dict) -> None:
    """Example handler for submission events."""
    logger.info(
        f"Received submission: {event.title}"
        f"from r/{event.subreddit} by u/{event.author} "
        f"[score: {event.score}, comments: {event.num_comments}]",
        extra=metadata
    )


def example_comment_handler(event: RedditCommentEvent, metadata: dict) -> None:
    """Example handler for comment events."""
    logger.info(
        f"Received comment: {event.body[:50]}... "
        f"from r/{event.subreddit} by u/{event.author} "
        f"[score: {event.score}]",
        extra=metadata
    )


def example_error_handler(error: Exception) -> None:
    """Example handler for errors."""
    logger.error(f"Consumer error: {error}")


def main():
    """Main function to run the consumer."""
    # Configure logging
    logger.add(
        "logs/consumer_{time}.log",
        rotation="500 MB",
        retention="10 days",
        level="INFO",
    )
    
    # Load settings
    settings = load_settings()
    
    # Create consumer
    consumer = RedditKafkaConsumer(
        group_id="reddit-consumer-group",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )
    
    # Subscribe to topics
    topics = [
        settings.topics.TOPIC_REDDIT_COMMENTS,
        settings.topics.TOPIC_REDDIT_SUBMISSIONS,
    ]
    consumer.subscribe(topics)
    
    # Start consuming with handlers
    logger.info("Starting Reddit Kafka consumer...")
    consumer.consume(
        timeout=1.0,
        on_submission=example_submission_handler,
        on_comment=example_comment_handler,
        on_error=example_error_handler,
    )


if __name__ == "__main__":
    main()