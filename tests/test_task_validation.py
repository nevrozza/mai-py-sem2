import datetime

import pytest

from src.tasks.exceptions import BusinessLogicError
from src.tasks.exceptions import ValidationError
from src.tasks.models.models import Task
from src.tasks.models.utils import TaskStatus


def test_task_creation_success():
    task = Task(
        id_="meow",
        payload="test",
        description_="Test",
        priority_=50
    )
    assert task.id == "meow"
    assert task.priority == 50
    assert task.status == TaskStatus.NEW
    assert isinstance(task.created_at, datetime.datetime)

    for p in [0, 100]:
        Task(
            id_="", payload="", description_="", priority_=p
        )


def test_task_creation_failure():
    with pytest.raises(ValidationError, match="_id must be str, got int"):
        Task(
            id_=13,
            payload="test",
            description_="Test",
            priority_=50
        )
    with pytest.raises(ValidationError, match="_description must be str, got int"):
        Task(
            id_="13",
            payload="test",
            description_=13,
            priority_=50
        )
    with pytest.raises(ValidationError, match="[0-100]"):
        Task(
            id_="13",
            payload="test",
            description_="123",
            priority_=150
        )
    with pytest.raises(ValidationError, match="[0-100]"):
        Task(
            id_="13",
            payload="test",
            description_="123",
            priority_=-50
        )


def test_task_validation():
    task = Task("1", "data", "desc", 10)

    with pytest.raises(ValidationError, match="Priority must be int"):
        task.priority = 150

    with pytest.raises(ValidationError, match="[0-100]"):
        task.priority = -5

    task.priority = 99
    task.status = TaskStatus.IN_PROGRESS

    with pytest.raises(BusinessLogicError, match="Change order: NEW -> IN_PROGRESS -> DONE"):
        task.status = TaskStatus.NEW

    task.status = TaskStatus.DONE

    with pytest.raises(BusinessLogicError, match="Change order: NEW -> IN_PROGRESS -> DONE"):
        task.status = TaskStatus.IN_PROGRESS


def test_task_immutability():
    task = Task("1", "data", "desc", 10)

    with pytest.raises(AttributeError, match="read-only"):
        task.id = "meow"

    with pytest.raises(AttributeError, match="has no setter"):
        task.description = "test"

    with pytest.raises(AttributeError, match="read-only"):
        task.created_at = datetime.datetime.now()

    task.payload = "test"  # Пока ещё мутабельно!
