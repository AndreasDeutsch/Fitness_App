<template>
    <div class="row d-flex justify-content-center mx-auto mt-5">
        <div class="col-4 pt-6">
            <form>
                <div class="form-group">
                    <label for="usernameField">Firstname</label>
                    <input v-model="form.firstname" type="text" class="form-control" id="firstnameField">
                </div>
                <div class="form-group">
                    <label for="passwordField">Lastname</label>
                    <input v-model="form.lastname" type="text" class="form-control" id="lastnameField">
                </div>
                <div class="form-group">
                    <label for="birthdayField">Email</label>
                    <input v-model="form.email" type="text" class="form-control" id="emailField">
                </div>
                <div class="form-group">
                    <label for="birthdayField">Password</label>
                    <input v-model="form.password" type="password" class="form-control" id="passwordField">
                </div>
                <div class=" d-flex justify-content-center">
                    <button type="submit" class="btn btn-primary" v-on:click="submit">Register</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { registerUser } from '../store/user';

const form = ref({
    firstname: '',
    lastname: '',
    email: '',
    password: '',
});

const submit = async () => {
    registerUser(form.value);
}

</script>