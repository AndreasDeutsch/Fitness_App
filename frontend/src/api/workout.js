import request from './req';
import axios from 'axios';

export const apiGetWorkouts = () => axios.get('/workout?skip=0&limit=100');
export const apiGetSpecificWorkout = (id) => axios.get(`/workout/${id}`);
export const apiPostWorkout = data => axios.post('/workout', data);