<template>
  <div
    class="flex justify-center items-center bg-gradient-to-br from-blue-50 dark:from-gray-900 to-indigo-100 dark:to-gray-800 p-4">
    <div class="w-full max-w-md">
      <!-- Header -->
      <div class="mb-6 text-center">
        <div class="flex justify-center mb-4">
          <div class="bg-gradient-to-br from-green-500 to-blue-600 shadow-lg p-3 rounded-2xl">
            <UserPlusIcon class="w-10 h-10 text-white" />
          </div>
        </div>
        <h2 class="mb-2 font-bold text-primary-light dark:text-primary-dark text-2xl">
          Create Account
        </h2>
        <p class="text-secondary-light dark:text-secondary-dark text-sm">
          Join us today and start your journey
        </p>
      </div>

      <!-- Registration Form -->
      <div class="bg-white dark:bg-gray-800 shadow-2xl p-6 border border-gray-200 dark:border-gray-700 rounded-2xl">
        <form class="space-y-4" @submit.prevent="handleRegister">
          <!-- Username Input -->
          <div class="group">
            <label for="username" class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
              <UserIcon class="inline mr-2 w-4 h-4" />
              Username
            </label>
            <input id="username" v-model="username" type="text"
              class="bg-gray-50 dark:bg-gray-700 p-3 border-2 border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full text-primary-light dark:text-primary-dark transition-all duration-200"
              placeholder="Choose a username" required />
          </div>

          <!-- Email Input -->
          <div class="group">
            <label for="email" class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
              <EnvelopeIcon class="inline mr-2 w-4 h-4" />
              Email Address
            </label>
            <input id="email" v-model="email" type="email"
              class="bg-gray-50 dark:bg-gray-700 p-3 border-2 border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full text-primary-light dark:text-primary-dark transition-all duration-200"
              placeholder="Enter your email address" required />
          </div>

          <!-- Password Input -->
          <div class="group">
            <label for="password1" class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
              <LockClosedIcon class="inline mr-2 w-4 h-4" />
              Password
            </label>
            <div class="relative">
              <input id="password1" v-model="password1" :type="showPassword ? 'text' : 'password'"
                class="bg-gray-50 dark:bg-gray-700 p-3 pr-12 border-2 border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full text-primary-light dark:text-primary-dark transition-all duration-200"
                placeholder="Create a password" required />
              <button type="button" @click="showPassword = !showPassword"
                class="right-0 absolute inset-y-0 flex items-center pr-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200">
                <EyeIcon v-if="!showPassword" class="w-4 h-4" />
                <EyeSlashIcon v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Confirm Password Input -->
          <div class="group">
            <label for="password2" class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
              <ShieldCheckIcon class="inline mr-2 w-4 h-4" />
              Confirm Password
            </label>
            <div class="relative">
              <input id="password2" v-model="password2" :type="showConfirmPassword ? 'text' : 'password'"
                class="bg-gray-50 dark:bg-gray-700 p-3 pr-12 border-2 border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full text-primary-light dark:text-primary-dark transition-all duration-200"
                placeholder="Confirm your password" required />
              <button type="button" @click="showConfirmPassword = !showConfirmPassword"
                class="right-0 absolute inset-y-0 flex items-center pr-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200">
                <EyeIcon v-if="!showConfirmPassword" class="w-4 h-4" />
                <EyeSlashIcon v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Password Strength Indicator -->
          <div v-if="password1" class="space-y-1">
            <div class="flex justify-between text-xs">
              <span class="text-gray-600 dark:text-gray-400">Password strength:</span>
              <span :class="passwordStrengthColor" class="font-medium">{{ passwordStrengthText }}</span>
            </div>
            <div class="bg-gray-200 dark:bg-gray-700 rounded-full w-full h-1.5">
              <div class="rounded-full h-1.5 transition-all duration-300"
                :class="passwordStrengthColor.replace('text-', 'bg-')" :style="`width: ${passwordStrengthWidth}%`">
              </div>
            </div>
          </div>

          <!-- Terms Agreement -->
          <div class="flex items-start pt-2">
            <input id="terms" v-model="agreeToTerms" type="checkbox"
              class="bg-gray-100 dark:bg-gray-700 mt-0.5 border-gray-300 dark:border-gray-600 rounded focus:ring-2 focus:ring-indigo-500 w-4 h-4 text-indigo-600"
              required />
            <label for="terms" class="ml-2 text-gray-600 dark:text-gray-400 text-xs">
              I agree to the
              <a href="#" class="text-indigo-600 dark:text-indigo-400 hover:underline">Terms of Service</a>
              and
              <a href="#" class="text-indigo-600 dark:text-indigo-400 hover:underline">Privacy Policy</a>
            </label>
          </div>

          <!-- Submit Button -->
          <button type="submit" :disabled="isLoading || !agreeToTerms"
            class="flex justify-center items-center bg-gradient-to-r from-green-600 hover:from-green-500 disabled:from-gray-400 to-blue-600 hover:to-blue-500 disabled:to-gray-500 shadow-lg disabled:shadow-none px-6 py-3 rounded-xl w-full font-semibold text-white disabled:transform-none hover:scale-105 transition-all duration-200 transform">
            <ArrowPathIcon v-if="isLoading" class="mr-2 w-4 h-4 animate-spin" />
            <span v-if="isLoading">Creating Account...</span>
            <span v-else>
              <CheckIcon class="inline mr-2 w-4 h-4" />
              Create Account
            </span>
          </button>

          <!-- Divider -->
          <div class="relative my-4">
            <div class="absolute inset-0 flex items-center">
              <div class="border-gray-300 dark:border-gray-600 border-t w-full"></div>
            </div>
            <div class="relative flex justify-center text-xs">
              <span class="bg-white dark:bg-gray-800 px-3 text-gray-500 dark:text-gray-400">
                Already have an account?
              </span>
            </div>
          </div>

          <!-- Login Link -->
          <router-link to="/login"
            class="block bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 px-4 py-3 rounded-xl w-full font-medium text-gray-700 dark:text-gray-300 text-sm text-center transition-all duration-200">
            <ArrowRightOnRectangleIcon class="inline mr-2 w-4 h-4" />
            Sign In Instead
          </router-link>

          <!-- Error Messages -->
          <div v-if="authError"
            class="bg-red-50 dark:bg-red-900/20 p-3 border border-red-200 dark:border-red-800 rounded-xl">
            <div class="flex items-start">
              <ExclamationTriangleIcon class="flex-shrink-0 mt-0.5 mr-2 w-4 h-4 text-red-400" />
              <div class="text-xs">
                <p v-for="(error, index) in formattedErrors" :key="index" class="text-red-700 dark:text-red-400">
                  {{ error }}
                </p>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>



<script>
import { mapActions, mapGetters } from 'vuex';
import {
  UserPlusIcon,
  UserIcon,
  EnvelopeIcon,
  LockClosedIcon,
  ShieldCheckIcon,
  EyeIcon,
  EyeSlashIcon,
  ArrowPathIcon,
  CheckIcon,
  ArrowRightOnRectangleIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline';

export default {
  components: {
    UserPlusIcon,
    UserIcon,
    EnvelopeIcon,
    LockClosedIcon,
    ShieldCheckIcon,
    EyeIcon,
    EyeSlashIcon,
    ArrowPathIcon,
    CheckIcon,
    ArrowRightOnRectangleIcon,
    ExclamationTriangleIcon
  },
  data() {
    return {
      username: '',
      email: '',
      password1: '',
      password2: '',
      showPassword: false,
      showConfirmPassword: false,
      agreeToTerms: false,
      isLoading: false,
    };
  },
  computed: {
    ...mapGetters('auth', ['authError']),
    formattedErrors() {
      return this.authError ? this.authError.split('\n') : [];
    },
    passwordStrength() {
      if (!this.password1) return 0;
      let strength = 0;
      if (this.password1.length >= 8) strength += 1;
      if (/[a-z]/.test(this.password1)) strength += 1;
      if (/[A-Z]/.test(this.password1)) strength += 1;
      if (/[0-9]/.test(this.password1)) strength += 1;
      if (/[^A-Za-z0-9]/.test(this.password1)) strength += 1;
      return strength;
    },
    passwordStrengthText() {
      switch (this.passwordStrength) {
        case 0:
        case 1: return 'Very Weak';
        case 2: return 'Weak';
        case 3: return 'Fair';
        case 4: return 'Good';
        case 5: return 'Strong';
        default: return 'Very Weak';
      }
    },
    passwordStrengthColor() {
      switch (this.passwordStrength) {
        case 0:
        case 1: return 'text-red-500';
        case 2: return 'text-orange-500';
        case 3: return 'text-yellow-500';
        case 4: return 'text-blue-600';
        case 5: return 'text-green-500';
        default: return 'text-red-500';
      }
    },
    passwordStrengthWidth() {
      return (this.passwordStrength / 5) * 100;
    }
  },
  methods: {
    ...mapActions('auth', ['register']),
    async handleRegister() {
      this.isLoading = true;
      try {
        await this.register({
          username: this.username,
          email: this.email,
          password1: this.password1,
          password2: this.password2,
        });
        this.$router.push('/login'); // Redirect on success
      } catch (error) {
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
