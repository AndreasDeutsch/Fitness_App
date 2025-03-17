import request from './req';
import axios from 'axios';

export const apiGetExercise = () => axios.get('/exercises?skip=0&limit=100');
export const apiPostExercise = data => axios.post('/exercises', data);