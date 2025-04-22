import request from './req';
import axios from 'axios';

export const apiGetWorkouts = (user_id) => axios.get(`/workout/${user_id}?skip=0&limit=100`);
export const apiGetSpecificWorkout = (id) => axios.get(`/workout/workout/${id}`);
export const apiPostWorkout = data => axios.post('/workout', data);
export const apiDeleteWorkout = (id) => axios.delete(`/workout/${id}`);
export const apiEndWorkout = data => axios.post(`/workout/end/`, data);