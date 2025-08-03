import api from './api';

const SUBSCRIPTION_API_URL = '/api/subscription/';

export default {
  // Get current subscription details
  getSubscription() {
    return api.get(SUBSCRIPTION_API_URL);
  },

  // Update subscription plan
  updateSubscription(planData) {
    return api.put(SUBSCRIPTION_API_URL, planData);
  },

  // Cancel subscription
  cancelSubscription() {
    return api.delete(SUBSCRIPTION_API_URL);
  },

  // Get subscription history
  getSubscriptionHistory() {
    return api.get(SUBSCRIPTION_API_URL + 'history/');
  },

  // Upgrade to premium
  upgradeToPremium(paymentData) {
    return api.post(SUBSCRIPTION_API_URL + 'upgrade/', paymentData);
  },

  // Resume cancelled subscription
  resumeSubscription() {
    return api.post(SUBSCRIPTION_API_URL + 'resume/');
  },

  // Get available plans
  getPlans() {
    return api.get(SUBSCRIPTION_API_URL + 'plans/');
  }
};
