<template>
    <div class="container mt-5">
        <div class="search-filter mb-4">
            <input v-model="searchQuery" type="text" placeholder="Search workouts..." class="form-control mb-2">
            <div class="d-flex justify-content-between">
                <input v-model="dateRange.start" type="date" class="form-control me-2">
                <input v-model="dateRange.end" type="date" class="form-control">
            </div>
        </div>
        <ul class="list-group">
            <li v-for="workout in filteredWorkouts" :key="workout.id" class="list-group-item d-flex justify-content-between align-items-center">
                <router-link :to="{ name: 'SpecificWorkoutView', params: { id: workout.workout_id } }" class="text-decoration-none">
                    {{ workout.name }}
                </router-link>
                <span class="badge bg-light text-dark">{{ formatDate(workout.start_datetime) }}</span>
            </li>
        </ul>
        <div class="form-group mt-4">
            <label for="name">Name</label>
            <input v-model="form.name" type="text" class="form-control" id="name">
        </div>
        <div class="d-flex justify-content-center mt-3">
            <button type="submit" class="btn btn-primary" @click="add_workout">Start Workout</button>
        </div>
    </div>
</template>

<script setup>
import { apiGetWorkouts, apiPostWorkout } from '../api/workout';
import { onMounted, ref, computed } from 'vue';

const getCookie = (name) => {
    const match = document.cookie.split('; ').find(row => row.startsWith(name + '='));
    return match ? match.split('=')[1] : null;
};

const workouts = ref([]);
const searchQuery = ref('');
const dateRange = ref({ start: '', end: '' });

const form = ref({
    name: '',
    user_id: getCookie('user_id'), 
    start_datetime: new Date().toISOString()
});

onMounted(async () => {
    try {
        const response = await apiGetWorkouts();
        workouts.value = response.data;
    } catch (error) {
        console.error('Error fetching workouts:', error);
    }
});

const add_workout = async () => {
    try {
        const response = await apiPostWorkout(form.value); 
        if (response.status === 200){
            const response_get = await apiGetWorkouts();
            workouts.value = response_get.data;
        }
        else {
            console.error('Route did not work', response);
        }
    } catch (error) {
        console.error('Error adding workout:', error);
    }
};

const filteredWorkouts = computed(() => {
    return workouts.value.filter(workout => {
        const matchesSearch = workout.name.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesDateRange = (!dateRange.value.start || new Date(workout.start_datetime) >= new Date(dateRange.value.start)) &&
                                 (!dateRange.value.end || new Date(workout.start_datetime) <= new Date(dateRange.value.end));
        return matchesSearch && matchesDateRange;
    });
});

const formatDate = (datetime) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(datetime).toLocaleDateString(undefined, options);
};
</script>

