import pytest


@pytest.mark.asyncio
async def test_execute_callback_skips_memory_error_when_quality_check_disabled():
    from shadowbotagents.task.task import Task
    from shadowbotagents.main import TaskOutput

    task = Task(description="Test task", quality_check=False)
    output = TaskOutput(description="Test", raw="ok", agent="tester")

    await task.execute_callback(output)

    assert task.non_fatal_errors == []
    assert output.non_fatal_errors is None


@pytest.mark.asyncio
async def test_execute_callback_exposes_callback_error_on_task_output():
    from shadowbotagents.task.task import Task
    from shadowbotagents.main import TaskOutput

    async def failing_callback(_output):
        raise RuntimeError("boom")

    task = Task(description="Test task", on_task_complete=failing_callback, quality_check=False)
    output = TaskOutput(description="Test", raw="ok", agent="tester")

    await task.execute_callback(output)

    assert output.callback_error == "boom"
    assert output.non_fatal_errors == ["callback: boom"]
    assert task.non_fatal_errors == ["callback: boom"]
