import request from './req';
import axios from 'axios';

export const apiFinishSet = data => axios.post('/set/finish/', data);
export const apiAddSet = data => axios.post('/set', data);
export const apiDeleteSet = set_id => axios.delete(`/set/${set_id}`);
