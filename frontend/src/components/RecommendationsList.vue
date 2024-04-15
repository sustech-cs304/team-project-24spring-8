<template>
  <div class="recommendationsList">
    <h2>个性化推荐活动</h2>
    <ul>\
      <li v-for="activity in recommendedActivities" :key="activity.id">
        {{ activity.title }}
        <button @click="goToInfoDisplay(activity)">查看详情</button>
      </li>
    </ul>

    <InfoDisplay :activity="selectedActivity" v-if="selectedActivity" />
  </div>
</template>

<script>
import InfoDisplay from './InfoDisplay.vue';

export default {
  name: 'RecommendationsListComponent',
  components: {
    InfoDisplay
  },
  data() {
    return {
      recommendedActivities: [
        {
          id: 1,
          title: '示例活动 1',
          category: '演出',
          date: '2024-04-15',
          location: '示例地点 1',
          description: '描述1'
        },
        {
          id: 2,
          title: '示例活动 2',
          category: '展览',
          date: '2024-04-16',
          location: '示例地点 2',
          description: '描述2'
        },
      ],
      selectedActivity: null
    };
  },
  methods: {
    goToInfoDisplay(activity) {
      this.selectedActivity = activity;
    },
    fetchRecommendedActivities() {
    }
  },
  mounted() {
    this.fetchRecommendedActivities();
  }
};
</script>