<template>
  <div>
    <div class="d-flex justify-content-end">
        <button type="button" class="btn btn-primary" v-on:click="showPopup = true">Add Exercise</button>
    </div>
    <div v-if="workout">
      <h1>{{ workout.name }}</h1>
      <p>{{ workout.description }}</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>

    <div v-if="showPopup" class="modal d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Select an Exercise</h5>
            <button type="button" class="btn-close" v-on:click="showPopup = false"></button>
          </div>
          <div class="modal-body">
            <ul class="list-group">
              <li class="list-group-item" v-for="exercise in availableExercises" :key="exercise.exercise_id" v-on:click="addExerciseToWorkout(exercise.exercise_id)">
                {{ exercise.name }}
              </li>
            </ul>
            <button type="button" class="btn btn-secondary mt-3" v-on:click="showAddNewExercise = true">Add New Exercise</button>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" v-on:click="showPopup = false">Close</button>
          </div>
          <div v-if="showAddNewExercise" class="mt-3">
            <input type="text" class="form-control" v-model="newExerciseName" placeholder="Exercise Name" />
            <button type="button" class="btn btn-primary mt-2" v-on:click="submitNewExercise">Submit</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { apiGetSpecificWorkout } from '../api/workout';
import { apiGetExercise, apiPostExercise } from '../api/exercise';
import { apiPostExerciseWorkout } from '../api/exercise_workout';
import { getCookie } from '../utils/cookies';  

export default {
  name: 'SpecificWorkoutView',
  setup() {
    const route = useRoute();
    const workout = ref(null);
    const showPopup = ref(false);
    const showAddNewExercise = ref(false);
    const availableExercises = ref([]);
    const newExerciseName = ref('');

    const addNewExercise = () => {
      showAddNewExercise.value = true;
    };

    const submitNewExercise = async () => {
      try {
        const userId = getCookie('user_id');
        await apiPostExercise({ name: newExerciseName.value, user_id: userId });
        const exercisesResponse = await apiGetExercise();
        availableExercises.value = exercisesResponse.data;
        newExerciseName.value = '';
        showAddNewExercise.value = false;
      } catch (error) {
        console.error('Error adding new exercise:', error);
      }
    };

    const addExerciseToWorkout = async (exerciseId) => {
      try {
        const workoutId = route.params.id;
        console.log('Adding exercise to workout:', { workout_id: workoutId, exercise_id: exerciseId }); // Debug log
        await apiPostExerciseWorkout({ workout_id: workoutId, exercise_id: exerciseId });
        showPopup.value = false;
      } catch (error) {
        console.error('Error adding workout spot:', error);
      }
    };

    onMounted(async () => {
      const workoutId = route.params.id;
      try {
        const response = await apiGetSpecificWorkout(workoutId);
        workout.value = response.data;

        const exercisesResponse = await apiGetExercise();
        availableExercises.value = exercisesResponse.data;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    });

    return {
      workout,
      showPopup,
      showAddNewExercise,
      availableExercises,
      newExerciseName,
      addNewExercise,
      submitNewExercise,
      addExerciseToWorkout
    };
  },
};
</script>

