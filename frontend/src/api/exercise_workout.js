import request from './req';
import axios from 'axios';

export const apiPostExerciseWorkout = data => axios.post('/exercise_workouts', data);
export const apiGetExerciseWorkoutByWorkout = workout_id => axios.get(`/exercise_workouts/workout/${workout_id}`);
export const apiDeleteExerciseWorkout = exercise_workout_id => axios.delete(`/exercise_workouts/${exercise_workout_id}`);
