import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from loguru import logger
import os

Base = declarative_base()


class TaskExecution(Base):
    """Stores task execution history"""

    __tablename__ = "task_executions"

    id = Column(Integer, primary_key=True)
    task_description = Column(Text, nullable=False)
    plan = Column(Text)
    results = Column(Text)
    success = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    steps_count = Column(Integer, default=0)


class LearnedPattern(Base):
    """Stores lightweight reusable patterns"""

    __tablename__ = "learned_patterns"

    id = Column(Integer, primary_key=True)
    task_type = Column(String(200))
    pattern_data = Column(Text)
    success_count = Column(Integer, default=1)
    last_used = Column(DateTime, default=datetime.utcnow)



class AgentMemory:
    """Persistent agent memory using SQLite"""

    def __init__(self, db_path: str = "data/agent_memory.db"):
        os.makedirs("data", exist_ok=True)

        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        logger.info(f"Agent memory initialized at {db_path}")


    def save_task(self, task: str, plan: Dict, results: List[Dict]) -> int:
        try:
            success = all(r.get("success", False) for r in results)

            execution = TaskExecution(
                task_description=task,
                plan=json.dumps(plan),
                results=json.dumps(results),
                success=success,
                steps_count=len(results),
            )

            self.session.add(execution)
            self.session.commit()

            if success:
                self._learn_pattern(task, plan)

            return execution.id

        except Exception as e:
            logger.error(f"Failed to save task: {e}")
            self.session.rollback()
            return -1


    def get_similar_tasks(self, task: str, limit: int = 5) -> List[Dict]:
        try:
            past = (
                self.session.query(TaskExecution)
                .filter(TaskExecution.success == True)
                .order_by(TaskExecution.timestamp.desc())
                .limit(20)
                .all()
            )

            task_words = set(task.lower().split())
            scored = []

            for e in past:
                words = set(e.task_description.lower().split())
                score = len(task_words & words)
                if score > 0:
                    scored.append(
                        {
                            "task": e.task_description,
                            "plan": json.loads(e.plan),
                            "score": score,
                        }
                    )

            scored.sort(key=lambda x: x["score"], reverse=True)
            return scored[:limit]

        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []


    def _learn_pattern(self, task: str, plan: Dict):
        try:
            task_lower = task.lower()

            if "whatsapp" in task_lower or "message" in task_lower:
                task_type = "messaging"
            elif "gmail" in task_lower or "email" in task_lower:
                task_type = "email"
            elif "search" in task_lower:
                task_type = "search"
            else:
                task_type = "generic"

            pattern = (
                self.session.query(LearnedPattern)
                .filter(LearnedPattern.task_type == task_type)
                .first()
            )

            if pattern:
                pattern.success_count += 1
                pattern.last_used = datetime.utcnow()
            else:
                pattern = LearnedPattern(
                    task_type=task_type,
                    pattern_data=json.dumps(plan),
                )
                self.session.add(pattern)

            self.session.commit()

        except Exception as e:
            logger.error(f"Pattern learning failed: {e}")
            self.session.rollback()


    def get_success_rate(self) -> float:
        try:
            total = self.session.query(TaskExecution).count()
            if total == 0:
                return 0.0

            success = (
                self.session.query(TaskExecution)
                .filter(TaskExecution.success == True)
                .count()
            )

            return success / total

        except Exception as e:
            logger.error(f"Success rate calculation failed: {e}")
            return 0.0

    def get_recent_tasks(self, limit: int = 10) -> List[Dict]:
        try:
            rows = (
                self.session.query(TaskExecution)
                .order_by(TaskExecution.timestamp.desc())
                .limit(limit)
                .all()
            )

            return [
                {
                    "task": r.task_description,
                    "success": r.success,
                    "timestamp": r.timestamp.isoformat(),
                }
                for r in rows
            ]

        except Exception as e:
            logger.error(f"Fetching recent tasks failed: {e}")
            return []
        

    def clear_old_data(self, days: int = 30):
        try:
            cutoff = datetime.utcnow() - timedelta(days=days)
            deleted = (
                self.session.query(TaskExecution)
                .filter(TaskExecution.timestamp < cutoff)
                .delete()
            )

            self.session.commit()
            logger.info(f"Deleted {deleted} old task records")

        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            self.session.rollback()