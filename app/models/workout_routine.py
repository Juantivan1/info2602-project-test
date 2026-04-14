from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .routine import Routine
    from .workout import Workout


class RoutineWorkoutBase(SQLModel):
    routine_id: Optional[int] = Field(default=None, foreign_key="routine.id")
    workout_id: Optional[int] = Field(default=None, foreign_key="workout.id")
    order: int = 0
    sets: int = 3
    reps: int = 10


class RoutineWorkout(RoutineWorkoutBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    routine: Optional["Routine"] = Relationship(back_populates="workout_links")
    workout: Optional["Workout"] = Relationship(back_populates="routine_links")
