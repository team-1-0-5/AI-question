<template>
  <div class="audience-profile">
    <header class="top-bar">
      <button class="back-btn" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      <span class="bar-title">个人中心</span>
    </header>
    <div class="profile-content">
      <div class="profile-avatar">
        <svg viewBox="0 0 48 48" width="80" height="80" fill="none">
          <circle cx="24" cy="24" r="22" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" />
          <circle cx="24" cy="20" r="8" fill="#90caf9" />
          <ellipse cx="24" cy="36" rx="12" ry="7" fill="#bbdefb" />
        </svg>
      </div>
      <div class="profile-info">
        <div class="profile-name">听众用户</div>
        <div class="profile-desc">个人中心功能开发中...</div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 预留后续功能
</script>

<style scoped>
.audience-profile {
  max-width: 500px;
  margin: 40px auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 32px 18px 24px 18px;
}
.top-bar {
  display: flex;
  align-items: center;
  height: 56px;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 20;
}
.back-btn {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 1rem;
  color: #4caf50;
  display: flex;
  align-items: center;
}
.bar-title {
  font-size: 1.18rem;
  color: #1a1a1a;
  font-weight: 600;
}
.profile-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 32px;
}
.profile-avatar {
  margin-bottom: 18px;
}
.profile-name {
  font-size: 1.2rem;
  color: #2e7d32;
  font-weight: 700;
  margin-bottom: 8px;
}
.profile-desc {
  color: #888;
  font-size: 1.05rem;
}
</style>
