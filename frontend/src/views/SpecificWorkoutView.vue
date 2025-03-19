<template>
  <div>
    <div v-if="workout">
      <h1>{{ workout.name }}</h1>
      <p>{{ workout.description }}</p>
      <div v-for="exercise in sortedExerciseWorkout" :key="exercise.exercise_workout_id" class="mt-3" style="border: 1px solid #ccc; padding: 10px;">
        <div class="d-flex justify-content-between align-items-center">
          <h3>{{ getExerciseName(exercise.exercise_id) }}</h3>
          <button v-if="exercise.sets.length === 0" type="button" class="btn btn-danger" v-on:click="deleteExerciseWorkout(exercise.exercise_workout_id)">Delete Exercise</button>
        </div>
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-center" v-for="set in exercise.sets" :key="set.set_id" style="margin: 10px; border: 1px solid #ccc; padding: 10px;">
            <div>
              Set ID: {{ set.set_id }}, Reps: {{ set.reps }}, Weight: {{ set.weight }}, Start Time: {{ formatDate(set.start_time) }}, End Time: {{ formatDate(set.end_time) }}
              <button v-if="!set.reps || !set.weight || !set.end_time" type="button" class="btn btn-primary mt-2" v-on:click="openFinishSetPopup(set.set_id)">Finish Set</button>
            </div>
            <button type="button" class="btn btn-danger" v-on:click="deleteSet(set.set_id)">Delete Set</button>
          </li>
        </ul>
        <button type="button" class="btn btn-success mt-2" v-on:click="addSetToExercise(exercise.exercise_workout_id)">+</button>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
    <div class="d-flex justify-content-center mt-4">
      <button type="button" class="btn btn-primary" v-on:click="showPopup = true">Add Exercise</button>
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

    <div v-if="showFinishSetPopup" class="modal d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Finish Set</h5>
            <button type="button" class="btn-close" v-on:click="showFinishSetPopup = false"></button>
          </div>
          <div class="modal-body">
            <input type="number" class="form-control" v-model="finishSetReps" placeholder="Reps" />
            <input type="number" class="form-control mt-2" v-model="finishSetWeight" placeholder="Weight" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" v-on:click="submitFinishSet">Submit</button>
            <button type="button" class="btn btn-secondary" v-on:click="showFinishSetPopup = false">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { apiGetSpecificWorkout } from '../api/workout';
import { apiGetExercise, apiPostExercise } from '../api/exercise';
import { apiPostExerciseWorkout, apiGetExerciseWorkoutByWorkout, apiDeleteExerciseWorkout } from '../api/exercise_workout';
import { apiFinishSet, apiAddSet, apiDeleteSet } from '../api/set';
import { getCookie } from '../utils/cookies';  

export default {
  name: 'SpecificWorkoutView',
  setup() {
    const route = useRoute();
    const workout = ref(null);
    const showPopup = ref(false);
    const showAddNewExercise = ref(false);
    const showFinishSetPopup = ref(false);
    const availableExercises = ref([]);
    const newExerciseName = ref('');
    const exerciseWorkout = ref([]);
    const finishSetReps = ref(null);
    const finishSetWeight = ref(null);
    const currentSetId = ref(null);

    const sortedExerciseWorkout = computed(() => {
      return exerciseWorkout.value.slice().sort((a, b) => a.workout_spot_number - b.workout_spot_number);
    });

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
        const response = await apiPostExerciseWorkout({ workout_id: workoutId, exercise_id: exerciseId });
        const newExerciseWorkout = response.data;
        exerciseWorkout.value.push(newExerciseWorkout);
        showPopup.value = false;
      } catch (error) {
        console.error('Error adding workout spot:', error);
      }
    };

    const openFinishSetPopup = (setId) => {
      currentSetId.value = setId;
      showFinishSetPopup.value = true;
    };

    const submitFinishSet = async () => {
      try {
        const setId = currentSetId.value;
        const reps = finishSetReps.value;
        const weight = finishSetWeight.value;
        const endTime = new Date().toISOString();
        await apiFinishSet({ set_id: setId, reps, weight, end_time: endTime });
        showFinishSetPopup.value = false;
        finishSetReps.value = null;
        finishSetWeight.value = null;
        currentSetId.value = null;
        const workoutId = route.params.id;
        const exerciseWorkoutResponse = await apiGetExerciseWorkoutByWorkout(workoutId);
        exerciseWorkout.value = exerciseWorkoutResponse.data;
      } catch (error) {
        console.error('Error finishing set:', error);
      }
    };

    const addSetToExercise = async (exerciseWorkoutId) => {
      try {
        const startTime = new Date().toISOString();
        await apiAddSet({ start_time: startTime, exercise_workout_id: exerciseWorkoutId });
        const workoutId = route.params.id;
        const exerciseWorkoutResponse = await apiGetExerciseWorkoutByWorkout(workoutId);
        exerciseWorkout.value = exerciseWorkoutResponse.data;
      } catch (error) {
        console.error('Error adding set:', error);
      }
    };

    const deleteSet = async (setId) => {
      try {
        await apiDeleteSet(setId);
        const workoutId = route.params.id;
        const exerciseWorkoutResponse = await apiGetExerciseWorkoutByWorkout(workoutId);
        exerciseWorkout.value = exerciseWorkoutResponse.data;
      } catch (error) {
        console.error('Error deleting set:', error);
      }
    };

    const deleteExerciseWorkout = async (exerciseWorkoutId) => {
      try {
        await apiDeleteExerciseWorkout(exerciseWorkoutId);
        exerciseWorkout.value = exerciseWorkout.value.filter(ex => ex.exercise_workout_id !== exerciseWorkoutId);
      } catch (error) {
        console.error('Error deleting exercise workout:', error);
      }
    };

    const getExerciseName = (exerciseId) => {
      const exercise = availableExercises.value.find(ex => ex.exercise_id === exerciseId);
      return exercise ? exercise.name : 'Unknown Exercise';
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    onMounted(async () => {
      const workoutId = route.params.id;
      try {
        const response = await apiGetSpecificWorkout(workoutId);
        workout.value = response.data;

        const exercisesResponse = await apiGetExercise();
        availableExercises.value = exercisesResponse.data;

        const exerciseWorkoutResponse = await apiGetExerciseWorkoutByWorkout(workoutId);
        exerciseWorkout.value = exerciseWorkoutResponse.data;
        console.log(exerciseWorkout.value);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    });

    return {
      workout,
      showPopup,
      showAddNewExercise,
      showFinishSetPopup,
      availableExercises,
      newExerciseName,
      addNewExercise,
      submitNewExercise,
      addExerciseToWorkout,
      exerciseWorkout,
      finishSetReps,
      finishSetWeight,
      openFinishSetPopup,
      submitFinishSet,
      addSetToExercise,
      deleteSet,
      deleteExerciseWorkout,
      getExerciseName,
      formatDate,
      sortedExerciseWorkout
    };
  },
};
</script>

