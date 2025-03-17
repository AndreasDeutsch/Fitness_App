import request from './req';
import axios from 'axios';

export const apiPostExerciseWorkout = data => axios.post('/exercise_workouts', data);
